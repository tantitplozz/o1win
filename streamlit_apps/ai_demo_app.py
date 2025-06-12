import random
import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเพจ
st.set_page_config(
    page_title="AI ระบบวิเคราะห์ธุรกรรมการเงิน", 
    page_icon="💰",
    layout="wide"
)

# ฟังก์ชันสร้างข้อมูลจำลองธุรกรรม
def generate_transactions(n=100):
    merchants = ["ร้านค้า A", "ร้านค้า B", "ร้านค้า C", "ร้านค้า D", "ร้านค้า E"]
    card_types = ["Visa", "Mastercard", "JCB", "UnionPay", "American Express"]
    categories = ["อาหารและเครื่องดื่ม", "เสื้อผ้า", "อิเล็กทรอนิกส์", "บันเทิง", "ท่องเที่ยว"]
    statuses = ["สำเร็จ", "กำลังดำเนินการ", "ล้มเหลว"]
    
    now = datetime.now()
    
    data = []
    for i in range(n):
        timestamp = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        amount = round(random.uniform(100, 10000), 2)
        status = random.choices(statuses, weights=[0.8, 0.1, 0.1])[0]
        
        data.append({
            "id": f"T{1000 + i}",
            "timestamp": timestamp,
            "merchant": random.choice(merchants),
            "category": random.choice(categories),
            "amount": amount,
            "card_type": random.choice(card_types),
            "status": status,
        })
    
    return pd.DataFrame(data)

# ฟังก์ชันวิเคราะห์ความเสี่ยง
def analyze_risk(transactions_df):
    # จำลองการวิเคราะห์ความเสี่ยง
    high_risk = []
    medium_risk = []
    low_risk = []
    
    for idx, row in transactions_df.iterrows():
        risk_score = random.random()
        
        # จำลองเงื่อนไขความเสี่ยง
        if row['amount'] > 5000 or risk_score > 0.9:
            high_risk.append(row['id'])
        elif row['amount'] > 2000 or risk_score > 0.7:
            medium_risk.append(row['id'])
        else:
            low_risk.append(row['id'])
    
    return {
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
    }

# ฟังก์ชันแนะนำบัตรเครดิตสำหรับแต่ละร้านค้า
def recommend_card(merchant):
    recommendations = {
        "ร้านค้า A": ["Visa", "JCB"],
        "ร้านค้า B": ["Mastercard", "American Express"],
        "ร้านค้า C": ["Visa", "Mastercard"],
        "ร้านค้า D": ["JCB", "UnionPay"],
        "ร้านค้า E": ["American Express", "Visa"],
    }
    
    return recommendations.get(merchant, ["ไม่มีข้อมูล"])

# ฟังก์ชันวิเคราะห์แนวโน้มรายวัน
def analyze_daily_trends(transactions_df):
    transactions_df['date'] = transactions_df['timestamp'].dt.date
    daily_sum = transactions_df.groupby('date')['amount'].sum().reset_index()
    daily_count = transactions_df.groupby('date')['id'].count().reset_index()
    daily_count.rename(columns={'id': 'count'}, inplace=True)
    
    result = pd.merge(daily_sum, daily_count, on='date')
    return result

# ------ ส่วนการแสดงผล UI ------
st.title("🧠 ระบบวิเคราะห์ธุรกรรมการเงินด้วย AI")
st.write("เครื่องมืออัจฉริยะสำหรับวิเคราะห์และติดตามธุรกรรมทางการเงิน")

# สร้างข้อมูลจำลอง
if 'transactions' not in st.session_state:
    st.session_state.transactions = generate_transactions(200)
    st.session_state.risk_analysis = analyze_risk(st.session_state.transactions)
    
transactions = st.session_state.transactions
risk_analysis = st.session_state.risk_analysis

# แสดงแทป
tab1, tab2, tab3, tab4 = st.tabs(["📊 ภาพรวม", "🔍 รายการธุรกรรม", "⚠️ การวิเคราะห์ความเสี่ยง", "💡 คำแนะนำ"])

with tab1:
    st.header("ภาพรวมธุรกรรม")
    
    # แสดงสถิติสำคัญ
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("จำนวนธุรกรรมทั้งหมด", f"{len(transactions):,}")
    with col2:
        successful = len(transactions[transactions['status'] == 'สำเร็จ'])
        st.metric("ธุรกรรมสำเร็จ", f"{successful:,}", f"{successful/len(transactions):.1%}")
    with col3:
        total_amount = transactions['amount'].sum()
        st.metric("มูลค่ารวม", f"฿{total_amount:,.2f}")
    with col4:
        high_risk_count = len(risk_analysis['high_risk'])
        st.metric("ธุรกรรมความเสี่ยงสูง", f"{high_risk_count}", f"{high_risk_count/len(transactions):.1%}")
    
    # แสดงกราฟแนวโน้มรายวัน
    st.subheader("แนวโน้มธุรกรรมรายวัน")
    daily_trends = analyze_daily_trends(transactions)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_trends['date'], daily_trends['amount'], marker='o', linewidth=2, color='#1f77b4')
    ax.set_xlabel('วันที่')
    ax.set_ylabel('มูลค่ารวม (บาท)')
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.autofmt_xdate()
    st.pyplot(fig)
    
    # แสดงกราฟแยกตามประเภทบัตร
    st.subheader("การกระจายตัวตามประเภทบัตร")
    card_distribution = transactions.groupby('card_type')['amount'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(card_distribution, labels=card_distribution.index, autopct='%1.1f%%', startangle=90, 
           shadow=True, explode=[0.05]*len(card_distribution))
    ax.axis('equal')
    st.pyplot(fig)

with tab2:
    st.header("รายการธุรกรรมทั้งหมด")
    
    # ตัวกรองข้อมูล
    col1, col2, col3 = st.columns(3)
    with col1:
        merchants = ['ทั้งหมด'] + list(transactions['merchant'].unique())
        selected_merchant = st.selectbox("เลือกร้านค้า", merchants)
    
    with col2:
        statuses = ['ทั้งหมด'] + list(transactions['status'].unique())
        selected_status = st.selectbox("เลือกสถานะ", statuses)
    
    with col3:
        card_types = ['ทั้งหมด'] + list(transactions['card_type'].unique())
        selected_card = st.selectbox("เลือกประเภทบัตร", card_types)
    
    # กรองข้อมูล
    filtered_transactions = transactions.copy()
    if selected_merchant != 'ทั้งหมด':
        filtered_transactions = filtered_transactions[filtered_transactions['merchant'] == selected_merchant]
    if selected_status != 'ทั้งหมด':
        filtered_transactions = filtered_transactions[filtered_transactions['status'] == selected_status]
    if selected_card != 'ทั้งหมด':
        filtered_transactions = filtered_transactions[filtered_transactions['card_type'] == selected_card]
    
    # แสดงตาราง
    st.dataframe(
        filtered_transactions.sort_values('timestamp', ascending=False),
        column_config={
            "id": "รหัสธุรกรรม",
            "timestamp": st.column_config.DatetimeColumn("เวลา", format="DD/MM/YYYY HH:mm"),
            "merchant": "ร้านค้า",
            "category": "หมวดหมู่",
            "amount": st.column_config.NumberColumn("จำนวนเงิน", format="฿%.2f"),
            "card_type": "ประเภทบัตร",
            "status": st.column_config.Column("สถานะ", help="สถานะของธุรกรรม"),
        },
        hide_index=True,
        use_container_width=True,
    )

with tab3:
    st.header("การวิเคราะห์ความเสี่ยง")
    
    # แสดงสถิติความเสี่ยง
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ความเสี่ยงสูง", len(risk_analysis['high_risk']))
        if len(risk_analysis['high_risk']) > 0:
            high_risk_txns = transactions[transactions['id'].isin(risk_analysis['high_risk'])]
            st.dataframe(
                high_risk_txns[['id', 'merchant', 'amount', 'status']],
                hide_index=True,
                use_container_width=True
            )
    with col2:
        st.metric("ความเสี่ยงปานกลาง", len(risk_analysis['medium_risk']))
    with col3:
        st.metric("ความเสี่ยงต่ำ", len(risk_analysis['low_risk']))
    
    # กราฟแสดงการกระจายความเสี่ยง
    risk_distribution = {
        'สูง': len(risk_analysis['high_risk']),
        'ปานกลาง': len(risk_analysis['medium_risk']),
        'ต่ำ': len(risk_analysis['low_risk'])
    }
    
    st.subheader("สัดส่วนความเสี่ยงของธุรกรรม")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(risk_distribution.keys(), risk_distribution.values(), color=['#d62728', '#ff7f0e', '#2ca02c'])
    
    # เพิ่มป้ายกำกับบนแท่ง
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height}', 
                ha='center', va='bottom')
    
    ax.set_xlabel('ระดับความเสี่ยง')
    ax.set_ylabel('จำนวนธุรกรรม')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with tab4:
    st.header("คำแนะนำสำหรับการทำธุรกรรม")
    
    # เลือกร้านค้าเพื่อรับคำแนะนำ
    selected_merchant_rec = st.selectbox(
        "เลือกร้านค้าเพื่อรับคำแนะนำ", 
        list(transactions['merchant'].unique()),
        key="recommendation_merchant"
    )
    
    # แสดงคำแนะนำ
    st.subheader(f"คำแนะนำสำหรับ {selected_merchant_rec}")
    
    recommended_cards = recommend_card(selected_merchant_rec)
    
    for card in recommended_cards:
        st.success(f"💳 แนะนำให้ใช้บัตร {card} กับร้านค้านี้เพื่อสิทธิประโยชน์สูงสุด")
    
    # แสดงข้อมูลร้านค้า
    merchant_txns = transactions[transactions['merchant'] == selected_merchant_rec]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("จำนวนธุรกรรมกับร้านค้านี้", len(merchant_txns))
        st.metric("มูลค่าเฉลี่ยต่อรายการ", f"฿{merchant_txns['amount'].mean():,.2f}")
    
    with col2:
        # สร้างกราฟวงกลมแสดงสัดส่วนบัตรที่ใช้กับร้านค้านี้
        card_counts = merchant_txns['card_type'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(card_counts, labels=card_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title(f"บัตรที่ใช้กับ {selected_merchant_rec}")
        st.pyplot(fig)

# แสดงข้อมูลเพิ่มเติมในแถบข้าง
with st.sidebar:
    st.header("รายละเอียดการวิเคราะห์")
    st.info("ระบบนี้ใช้ AI วิเคราะห์ธุรกรรมการเงินอัตโนมัติเพื่อช่วยในการตัดสินใจ")
    
    # ปุ่มสร้างข้อมูลใหม่
    if st.button("สร้างข้อมูลจำลองใหม่"):
        st.session_state.transactions = generate_transactions(200)
        st.session_state.risk_analysis = analyze_risk(st.session_state.transactions)
        st.rerun()
    
    # ข้อมูลล่าสุด
    st.subheader("ข้อมูลล่าสุด")
    latest_txn = transactions.sort_values('timestamp', ascending=False).iloc[0]
    
    st.write(f"**ธุรกรรมล่าสุด:** {latest_txn['id']}")
    st.write(f"**ร้านค้า:** {latest_txn['merchant']}")
    st.write(f"**จำนวนเงิน:** ฿{latest_txn['amount']:,.2f}")
    st.write(f"**สถานะ:** {latest_txn['status']}")
    
    # แสดงเวลาปัจจุบัน
    st.caption(f"อัปเดตล่าสุด: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")