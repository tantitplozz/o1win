#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI + WebSocket Example - Real-time Dashboard
ตัวอย่างการสร้าง API และ WebSocket สำหรับแอปพลิเคชัน Dashboard แบบ Real-time
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Set

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# สร้างแอป FastAPI
app = FastAPI(title="Real-time Dashboard API")

# เพิ่ม CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในการใช้งานจริงควรระบุ origin ที่อนุญาตเท่านั้น
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# โครงสร้างข้อมูลสำหรับเก็บสถานะ
class TransactionData(BaseModel):
    merchant_id: str
    amount: float
    card_type: str
    status: str
    timestamp: str


# Connection Manager สำหรับจัดการ WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


# สร้างอินสแตนซ์ของ Connection Manager
manager = ConnectionManager()

# เก็บข้อมูลจำลอง
transactions: List[TransactionData] = []
merchants = ["ร้านค้า A", "ร้านค้า B", "ร้านค้า C", "ร้านค้า D"]
card_types = ["Visa", "Mastercard", "JCB", "Amex"]
statuses = ["success", "pending", "failed"]

# กำหนด static files
# app.mount("/static", StaticFiles(directory="static"), name="static")


# API routes
@app.get("/", response_class=HTMLResponse)
async def get_dashboard_page():
    """หน้า Dashboard HTML พื้นฐาน"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-time Transaction Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { font-family: 'Arial', sans-serif; }
            .transaction-row { transition: background-color 0.3s; }
            .transaction-row.new { background-color: #4ADE80; animation: fadeout 2s forwards; }
            @keyframes fadeout { from { background-color: #4ADE80; } to { background-color: transparent; } }
            .chart-container { height: 300px; }
        </style>
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold text-center mb-8">Real-time Transaction Dashboard</h1>
            
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div class="bg-white rounded-lg shadow p-4">
                    <h2 class="text-sm text-gray-500">รายการทั้งหมด</h2>
                    <p class="text-2xl font-bold" id="total-transactions">0</p>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <h2 class="text-sm text-gray-500">ยอดเงินรวม</h2>
                    <p class="text-2xl font-bold" id="total-amount">฿0.00</p>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <h2 class="text-sm text-gray-500">อัตราความสำเร็จ</h2>
                    <p class="text-2xl font-bold" id="success-rate">0%</p>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <h2 class="text-sm text-gray-500">สถานะการเชื่อมต่อ</h2>
                    <p class="text-2xl font-bold text-green-500" id="connection-status">เชื่อมต่อแล้ว</p>
                </div>
            </div>
            
            <!-- Transaction Table -->
            <div class="bg-white rounded-lg shadow overflow-hidden mb-8">
                <h2 class="p-4 border-b text-lg font-semibold">รายการล่าสุด</h2>
                <div class="overflow-x-auto">
                    <table class="min-w-full">
                        <thead>
                            <tr class="bg-gray-100">
                                <th class="p-3 text-left">เวลา</th>
                                <th class="p-3 text-left">ร้านค้า</th>
                                <th class="p-3 text-left">จำนวนเงิน</th>
                                <th class="p-3 text-left">บัตร</th>
                                <th class="p-3 text-left">สถานะ</th>
                            </tr>
                        </thead>
                        <tbody id="transactions-table">
                            <!-- ข้อมูลจะถูกเพิ่มด้วย JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Control Panel -->
            <div class="bg-white rounded-lg shadow p-4 mb-8">
                <h2 class="text-lg font-semibold mb-4">Control Panel</h2>
                <div class="flex flex-wrap gap-4">
                    <button id="generate-btn" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                        สร้างรายการสุ่ม
                    </button>
                    <button id="clear-btn" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
                        ล้างข้อมูลทั้งหมด
                    </button>
                </div>
            </div>
        </div>

        <script>
            // WebSocket connection
            const socket = new WebSocket(`ws://${window.location.host}/ws`);
            let transactions = [];
            
            // Connection event handlers
            socket.onopen = function(e) {
                console.log("WebSocket connection established");
                document.getElementById('connection-status').textContent = "เชื่อมต่อแล้ว";
                document.getElementById('connection-status').classList.remove('text-red-500');
                document.getElementById('connection-status').classList.add('text-green-500');
            };
            
            socket.onclose = function(e) {
                console.log("WebSocket connection closed");
                document.getElementById('connection-status').textContent = "ขาดการเชื่อมต่อ";
                document.getElementById('connection-status').classList.remove('text-green-500');
                document.getElementById('connection-status').classList.add('text-red-500');
            };
            
            socket.onerror = function(error) {
                console.error("WebSocket error:", error);
            };
            
            // Message event handler
            socket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'transaction') {
                    // Add new transaction to the list
                    transactions.unshift(data.data);
                    if (transactions.length > 100) {
                        transactions.pop(); // Keep only latest 100 transactions
                    }
                    updateDashboard();
                } else if (data.type === 'clear') {
                    transactions = [];
                    updateDashboard();
                }
            };
            
            // Update dashboard with latest data
            function updateDashboard() {
                // Update stats
                document.getElementById('total-transactions').textContent = transactions.length;
                
                const totalAmount = transactions.reduce((sum, t) => sum + t.amount, 0);
                document.getElementById('total-amount').textContent = `฿${totalAmount.toLocaleString('th-TH', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                
                const successCount = transactions.filter(t => t.status === 'success').length;
                const successRate = transactions.length > 0 ? (successCount / transactions.length) * 100 : 0;
                document.getElementById('success-rate').textContent = `${successRate.toFixed(1)}%`;
                
                // Update transactions table
                const tableBody = document.getElementById('transactions-table');
                tableBody.innerHTML = '';
                
                transactions.slice(0, 10).forEach((transaction, index) => {
                    const row = document.createElement('tr');
                    row.className = 'transaction-row border-b';
                    if (index === 0) row.classList.add('new');
                    
                    // Format timestamp
                    const date = new Date(transaction.timestamp);
                    const formattedTime = date.toLocaleTimeString('th-TH');
                    
                    // Status color
                    let statusColor = 'text-gray-500';
                    if (transaction.status === 'success') statusColor = 'text-green-500';
                    if (transaction.status === 'failed') statusColor = 'text-red-500';
                    
                    row.innerHTML = `
                        <td class="p-3">${formattedTime}</td>
                        <td class="p-3">${transaction.merchant_id}</td>
                        <td class="p-3">฿${transaction.amount.toLocaleString('th-TH', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                        <td class="p-3">${transaction.card_type}</td>
                        <td class="p-3 font-medium ${statusColor}">${transaction.status}</td>
                    `;
                    
                    tableBody.appendChild(row);
                });
            }
            
            // Button event handlers
            document.getElementById('generate-btn').addEventListener('click', function() {
                fetch('/api/generate-transaction', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => console.log('Generated:', data))
                    .catch(error => console.error('Error:', error));
            });
            
            document.getElementById('clear-btn').addEventListener('click', function() {
                fetch('/api/clear-transactions', { method: 'POST' })
                    .then(() => console.log('Cleared all transactions'))
                    .catch(error => console.error('Error:', error));
            });
        </script>
    </body>
    </html>
    """
    return html_content


@app.get("/api/transactions")
async def get_transactions():
    """ดึงข้อมูลธุรกรรมทั้งหมด"""
    return transactions


@app.post("/api/generate-transaction")
async def generate_transaction():
    """สร้างธุรกรรมจำลอง"""
    # สร้างข้อมูลสุ่ม
    new_transaction = TransactionData(
        merchant_id=random.choice(merchants),
        amount=round(random.uniform(100, 10000), 2),
        card_type=random.choice(card_types),
        status=random.choice(statuses),
        timestamp=datetime.now().isoformat(),
    )

    # เพิ่มลงในรายการ
    transactions.append(new_transaction)

    # ส่งข้อมูลไปยัง WebSocket clients
    await manager.broadcast(
        json.dumps({"type": "transaction", "data": new_transaction.dict()})
    )

    return {"status": "success", "data": new_transaction}


@app.post("/api/clear-transactions")
async def clear_transactions():
    """ล้างข้อมูลธุรกรรมทั้งหมด"""
    transactions.clear()

    # แจ้ง WebSocket clients
    await manager.broadcast(json.dumps({"type": "clear"}))

    return {"status": "success", "message": "All transactions cleared"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint สำหรับการอัปเดตแบบ real-time"""
    await manager.connect(websocket)
    try:
        while True:
            # รอรับข้อความจาก client (ถ้ามี)
            data = await websocket.receive_text()
            # ในตัวอย่างนี้เราไม่ได้ทำอะไรกับข้อความที่ได้รับ
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def generate_random_transactions():
    """สร้างธุรกรรมสุ่มทุก 3-8 วินาที"""
    while True:
        # สุ่มระยะเวลารอ
        wait_time = random.uniform(3, 8)
        await asyncio.sleep(wait_time)

        # สร้างธุรกรรมใหม่
        new_transaction = TransactionData(
            merchant_id=random.choice(merchants),
            amount=round(random.uniform(100, 10000), 2),
            card_type=random.choice(card_types),
            status=random.choice(statuses),
            timestamp=datetime.now().isoformat(),
        )

        # เพิ่มลงในรายการ
        transactions.append(new_transaction)

        # ส่งข้อมูลไปยัง WebSocket clients
        await manager.broadcast(
            json.dumps({"type": "transaction", "data": new_transaction.dict()})
        )

        print(
            f"สร้างธุรกรรมใหม่: {new_transaction.merchant_id} - ฿{new_transaction.amount} - {new_transaction.status}"
        )


# สร้างงานพื้นหลังสำหรับการสร้างข้อมูล
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_random_transactions())


# รัน server ถ้าเรียกใช้โดยตรง
if __name__ == "__main__":
    uvicorn.run("fastapi_websocket_example:app", host="0.0.0.0", port=8000, reload=True)
