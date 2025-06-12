# MongoDB Example - Document Database
import json
from datetime import datetime

from pymongo import MongoClient

# เชื่อมต่อกับ MongoDB
client = MongoClient("mongodb://localhost:27017/")

# สร้างหรือใช้ฐานข้อมูล
db = client["transaction_history"]

# สร้างหรือใช้ Collection
transactions = db["transactions"]
logs = db["activity_logs"]


# ฟังก์ชันบันทึกธุรกรรม
def save_transaction(merchant_name, amount, card_type, status_code, details=None):
    """บันทึกข้อมูลธุรกรรมลงใน MongoDB"""
    transaction = {
        "merchant": merchant_name,
        "amount": amount,
        "card_type": card_type,
        "status": status_code,
        "timestamp": datetime.now(),
        "details": details or {},
    }

    insert_result = transactions.insert_one(transaction)
    print(f"บันทึกธุรกรรมเรียบร้อย ID: {insert_result.inserted_id}")
    return str(insert_result.inserted_id)


# ฟังก์ชันบันทึก Activity Log
def log_activity(activity_type, user, description, metadata=None):
    """บันทึกกิจกรรมของผู้ใช้"""
    log_entry = {
        "activity_type": activity_type,
        "user": user,
        "description": description,
        "timestamp": datetime.now(),
        "metadata": metadata or {},
    }

    logs.insert_one(log_entry)
    print(f"บันทึกกิจกรรม: {activity_type} โดย {user}")


# ฟังก์ชันค้นหาธุรกรรม
def find_transactions(query=None, limit=10):
    """ค้นหาธุรกรรมตามเงื่อนไข"""
    query = query or {}
    query_result = list(transactions.find(query).limit(limit))

    # แปลง ObjectId เป็น string เพื่อให้แสดงผลได้
    for item in query_result:
        item["_id"] = str(item["_id"])
        if "timestamp" in item:
            item["timestamp"] = item["timestamp"].isoformat()

    return query_result


# ฟังก์ชันวิเคราะห์ธุรกรรม
def analyze_transactions(merchant_filter=None):
    """วิเคราะห์ข้อมูลธุรกรรม"""
    pipeline = []

    # ถ้าระบุร้านค้า ให้กรองเฉพาะร้านค้านั้น
    if merchant_filter:
        pipeline.append({"$match": {"merchant": merchant_filter}})

    # กลุ่มตามสถานะและนับจำนวน
    pipeline.append(
        {
            "$group": {
                "_id": {"merchant": "$merchant", "status": "$status"},
                "count": {"$sum": 1},
                "total_amount": {"$sum": "$amount"},
            }
        }
    )

    # เรียงลำดับ
    pipeline.append({"$sort": {"_id.merchant": 1, "_id.status": 1}})

    analysis_result = list(transactions.aggregate(pipeline))
    return analysis_result


# ทดสอบการใช้งาน
if __name__ == "__main__":
    print("=== ทดสอบระบบบันทึกธุรกรรมด้วย MongoDB ===")

    # ทดสอบบันทึกข้อมูล
    save_transaction(
        "ร้านค้า A", 1500.50, "Visa", "success", {"items": ["สินค้า1", "สินค้า2"]}
    )
    save_transaction("ร้านค้า B", 750.25, "Mastercard", "pending")
    save_transaction("ร้านค้า A", 2000.00, "Amex", "success")
    save_transaction(
        "ร้านค้า C", 3500.75, "Visa", "failed", {"error_code": "CVV_INVALID"}
    )

    # บันทึกกิจกรรม
    log_activity("login", "user123", "ผู้ใช้เข้าสู่ระบบ")
    log_activity("payment", "user123", "ผู้ใช้ทำการชำระเงิน", {"payment_id": "PAY12345"})

    # ทดสอบค้นหาข้อมูล
    print("\n=== ค้นหาธุรกรรมทั้งหมด ===")
    all_transactions = find_transactions()
    print(json.dumps(all_transactions, indent=2, ensure_ascii=False))

    print("\n=== ค้นหาธุรกรรมที่สำเร็จ ===")
    successful = find_transactions({"status": "success"})
    print(json.dumps(successful, indent=2, ensure_ascii=False))

    # ทดสอบวิเคราะห์ข้อมูล
    print("\n=== วิเคราะห์ธุรกรรมตามร้านค้าและสถานะ ===")
    analysis = analyze_transactions()
    for result in analysis:
        merchant = result["_id"]["merchant"]
        status = result["_id"]["status"]
        count = result["count"]
        total = result["total_amount"]
        print(
            f"ร้านค้า: {merchant}, สถานะ: {status}, จำนวน: {count}, ยอดรวม: {total:.2f} บาท"
        )
