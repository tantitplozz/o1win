import numpy as np
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Demo App", page_icon="🤖", layout="wide")

# หัวข้อหลัก
st.title("🤖 ตัวอย่าง AI Web App ด้วย Streamlit")
st.markdown("---")

# แสดงข้อความต้อนรับ
st.markdown(
    """
## ยินดีต้อนรับสู่ AI Web App

แอปพลิเคชันนี้เป็นตัวอย่างการใช้งาน Streamlit สำหรับสร้าง AI Web App
คุณสามารถปรับแต่งและพัฒนาต่อยอดได้ตามต้องการ
"""
)

# แบ่งหน้าจอเป็น sidebar และ main content
with st.sidebar:
    st.header("ตัวเลือก")

    # สร้าง slider สำหรับปรับค่า
    data_size = st.slider("จำนวนข้อมูล", 10, 100, 50)

    # สร้าง checkbox
    show_data = st.checkbox("แสดงตารางข้อมูล", True)
    show_chart = st.checkbox("แสดงกราฟ", True)

    # ปุ่มสำหรับสร้างข้อมูลใหม่
    if st.button("สร้างข้อมูลใหม่"):
        st.session_state.data = pd.DataFrame(
            {"x": np.random.randn(data_size), "y": np.random.randn(data_size)}
        )
        st.success("สร้างข้อมูลใหม่แล้ว!")

# สร้างข้อมูลเริ่มต้นถ้ายังไม่มี
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        {"x": np.random.randn(data_size), "y": np.random.randn(data_size)}
    )

# แสดงข้อมูลตาม checkbox
if show_data:
    st.subheader("ข้อมูล")
    st.dataframe(st.session_state.data)

if show_chart:
    st.subheader("กราฟแสดงข้อมูล")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(st.session_state.data["x"], st.session_state.data["y"], alpha=0.7)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    st.pyplot(fig)

# เพิ่มส่วนสำหรับใส่ข้อความและได้รับการวิเคราะห์
st.markdown("---")
st.subheader("วิเคราะห์ข้อความ")

user_input = st.text_area("ป้อนข้อความที่ต้องการวิเคราะห์", "ฉันรู้สึกดีมากกับผลิตภัณฑ์นี้!")

if st.button("วิเคราะห์"):
    with st.spinner("กำลังวิเคราะห์..."):
        # จำลองการวิเคราะห์ด้วย AI (ในที่นี้เป็นแค่ตัวอย่าง)
        import time

        time.sleep(1)  # จำลองการประมวลผล

        # แสดงผลลัพธ์
        st.success("วิเคราะห์เสร็จสิ้น!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="ความเป็นบวก", value="85%", delta="+5%")
        with col2:
            st.metric(label="ความเป็นลบ", value="15%", delta="-5%")

        st.info("ข้อความนี้มีแนวโน้มเป็นบวก แสดงถึงความพึงพอใจต่อผลิตภัณฑ์")

# เพิ่ม footer
st.markdown("---")
st.markdown("**ตัวอย่าง AI Web App** | สร้างด้วย Streamlit และ OpenHands AI")
