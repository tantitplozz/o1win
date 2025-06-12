import random
import time
from datetime import datetime

import chromadb
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="OpenHands Real-World Demo", page_icon="👐", layout="wide"
)

# หัวข้อหลัก
st.title("👐 OpenHands AI ตัวอย่างการใช้งานจริง")
st.markdown("---")


# ฟังก์ชันสำหรับจัดการ ChromaDB
@st.cache_resource
def get_chroma_client():
    client = chromadb.Client()

    # ตรวจสอบว่ามี collection หรือไม่ ถ้าไม่มีให้สร้างใหม่
    try:
        collection = client.get_collection("merchant_transactions")
    except:
        collection = client.create_collection("merchant_transactions")

        # เพิ่มข้อมูลตัวอย่าง
        collection.add(
            documents=[
                "Amazon - Visa - 4532XXXXXXXX1234 - Success",
                "Shopify - Mastercard - 5421XXXXXXXX6789 - Failed",
                "Walmart - Visa - 4111XXXXXXXX1111 - Success",
                "eBay - Amex - 3782XXXXXXXX1000 - Failed",
                "Etsy - Discover - 6011XXXXXXXX2012 - Success",
            ],
            metadatas=[
                {
                    "merchant": "Amazon",
                    "card_type": "Visa",
                    "bin": "453212",
                    "result": "Success",
                },
                {
                    "merchant": "Shopify",
                    "card_type": "Mastercard",
                    "bin": "542101",
                    "result": "Failed",
                },
                {
                    "merchant": "Walmart",
                    "card_type": "Visa",
                    "bin": "411111",
                    "result": "Success",
                },
                {
                    "merchant": "eBay",
                    "card_type": "Amex",
                    "bin": "378282",
                    "result": "Failed",
                },
                {
                    "merchant": "Etsy",
                    "card_type": "Discover",
                    "bin": "601112",
                    "result": "Success",
                },
            ],
            ids=["trans1", "trans2", "trans3", "trans4", "trans5"],
        )

    return client


# เรียกใช้ฟังก์ชันเพื่อเตรียม ChromaDB
client = get_chroma_client()
collection = client.get_collection("merchant_transactions")

# สร้าง sidebar สำหรับควบคุม
with st.sidebar:
    st.header("การควบคุม")

    # เลือกร้านค้า
    merchant = st.selectbox(
        "เลือกร้านค้า",
        ["Amazon", "Shopify", "Walmart", "eBay", "Etsy", "Alibaba", "Lazada"],
    )

    # เลือกประเภทบัตร
    card_type = st.selectbox("ประเภทบัตร", ["Visa", "Mastercard", "Amex", "Discover"])

    # ใส่ BIN
    bin_number = st.text_input("BIN (6 หลัก)", "451234")

    # ตัวเลือกเพิ่มเติม
    use_ai = st.checkbox("ใช้ AI แนะนำบัตรที่เหมาะสม", True)

    # ปุ่มดำเนินการ
    process_button = st.button("เริ่มกระบวนการ", type="primary")

# แสดงแดชบอร์ดหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 ประวัติการทำธุรกรรม")

    # ดึงข้อมูลจาก ChromaDB และแสดงเป็นตาราง
    results = collection.get()
    if results["ids"]:
        df = pd.DataFrame(
            {
                "Merchant": [meta["merchant"] for meta in results["metadatas"]],
                "Card Type": [meta["card_type"] for meta in results["metadatas"]],
                "BIN": [meta["bin"] for meta in results["metadatas"]],
                "Result": [meta["result"] for meta in results["metadatas"]],
            }
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลการทำธุรกรรม")

with col2:
    st.subheader("📝 สถิติการทำธุรกรรม")

    # สร้างกราฟแสดงสถิติ
    if results["ids"]:
        # นับจำนวนธุรกรรมที่สำเร็จและล้มเหลว
        success_count = sum(
            1 for meta in results["metadatas"] if meta["result"] == "Success"
        )
        failed_count = len(results["ids"]) - success_count

        # แสดงตัวเลขสรุป
        st.metric("อัตราความสำเร็จ", f"{success_count / len(results['ids']) * 100:.1f}%")
    else:
        st.info("ไม่มีข้อมูลสำหรับแสดงกราฟ")

# ส่วนดำเนินการ
st.markdown("---")
st.subheader("🚀 ดำเนินการ")


# ฟังก์ชันแนะนำบัตรที่เหมาะสม
def recommend_card(merchant_name):
    # ค้นหาข้อมูลความสำเร็จในร้านค้านี้
    merchant_results = collection.get(
        where={
            "$and": [
                {"merchant": {"$eq": merchant_name}},
                {"result": {"$eq": "Success"}},
            ]
        }
    )

    if not merchant_results["ids"]:
        return None, None

    # ถ้ามีข้อมูล ให้แนะนำบัตรที่เคยใช้สำเร็จ
    card_types = [meta["card_type"] for meta in merchant_results["metadatas"]]
    bins = [meta["bin"] for meta in merchant_results["metadatas"]]

    if card_types and bins:
        return random.choice(card_types), random.choice(bins)
    return None, None


# เมื่อกดปุ่มดำเนินการ
if process_button:
    # ถ้าใช้ AI แนะนำบัตร
    if use_ai:
        recommended_card, recommended_bin = recommend_card(merchant)
        if recommended_card:
            st.info(
                f"AI แนะนำให้ใช้บัตร {recommended_card} กับ BIN {recommended_bin} สำหรับร้านค้า {merchant}"
            )
            card_type = recommended_card
            bin_number = recommended_bin

    # แสดงกระบวนการทำงาน
    st.text("กำลังดำเนินการ...")
    progress_bar = st.progress(0)

    # จำลองกระบวนการทำงาน
    for i in range(101):
        progress_bar.progress(i)
        time.sleep(0.02)

    # สุ่มผลลัพธ์
    result = random.choice(["Success", "Failed"])

    # แสดงผลลัพธ์
    if result == "Success":
        st.success(
            f"ดำเนินการสำเร็จ! ร้านค้า {merchant} ยอมรับบัตร {card_type} กับ BIN {bin_number}"
        )
    else:
        st.error(
            f"ดำเนินการล้มเหลว! ร้านค้า {merchant} ปฏิเสธบัตร {card_type} กับ BIN {bin_number}"
        )

    # บันทึกผลลงใน ChromaDB
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    collection.add(
        documents=[f"{merchant} - {card_type} - {bin_number} - {result}"],
        metadatas=[
            {
                "merchant": merchant,
                "card_type": card_type,
                "bin": bin_number,
                "result": result,
            }
        ],
        ids=[f"trans{current_time}"],
    )

    # อัปเดตหน้าเว็บ
    st.rerun()

# เพิ่ม footer
st.markdown("---")
st.markdown(
    "**OpenHands AI Real-World Demo** | สร้างด้วย Streamlit, ChromaDB และ OpenHands AI"
)
