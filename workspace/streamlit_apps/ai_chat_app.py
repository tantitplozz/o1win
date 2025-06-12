import json
import time
from datetime import datetime

import requests
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="OpenHands - AI Chat",
    page_icon="👐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# สไตล์ CSS เพิ่มเติม
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        padding-top: 0.5rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #E3F2FD;
    }
    .chat-message.assistant {
        background-color: #F5F5F5;
    }
    .chat-message .avatar {
        width: 50px;
    }
    .chat-message .avatar img {
        max-width: 40px;
        max-height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .content {
        width: calc(100% - 50px);
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #616161;
    }
</style>
""",
    unsafe_allow_html=True,
)

# หัวข้อ
st.markdown(
    "<h1 class='main-header'>👐 OpenHands - AI Chat</h1>", unsafe_allow_html=True
)
st.markdown("---")


# ฟังก์ชันสำหรับแสดงข้อความแชท
def display_chat(msg_content, role):
    with st.chat_message(role):
        st.write(msg_content)


# สร้าง sidebar สำหรับการตั้งค่า
with st.sidebar:
    st.header("⚙️ ตั้งค่า")

    # เลือกโมเดล AI
    ai_model = st.selectbox(
        "เลือกโมเดล AI:",
        ["GPT-4", "Claude 3 Opus", "Gemini Pro", "Mistral Large", "OpenRouter"],
    )

    # ตั้งค่าระดับความคิดสร้างสรรค์
    creativity_level = st.slider("ความคิดสร้างสรรค์:", 0.0, 1.0, 0.7)

    # ตั้งค่าความยาวของคำตอบ
    max_token_length = st.slider("ความยาวสูงสุด:", 100, 2000, 500)

    st.markdown("---")

    # ข้อมูลแอปพลิเคชัน
    st.caption(f"วันที่: {datetime.now().strftime('%d/%m/%Y')}")
    st.caption("สร้างโดย OpenHands")

# เริ่มต้นประวัติแชทหากยังไม่มี
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติแชทที่ผ่านมา
for msg in st.session_state.messages:
    display_chat(msg["content"], msg["role"])

# รับข้อความจากผู้ใช้
user_prompt = st.chat_input("พิมพ์ข้อความที่นี่...")


# ฟังก์ชันจำลองการเรียก API
def get_ai_response(user_input, model, creativity, max_length):
    # จำลองการโหลด
    with st.spinner("AI กำลังคิด..."):
        time.sleep(1.5)

    # สร้างคำตอบจำลอง
    if "สวัสดี" in user_input or "hello" in user_input.lower():
        return "สวัสดีครับ! มีอะไรให้ช่วยไหมครับวันนี้?"
    elif "ชื่อ" in user_input:
        return "ผมคือ OpenHands AI Assistant ยินดีที่ได้รู้จักครับ"
    elif "ทำอะไรได้" in user_input or "ความสามารถ" in user_input:
        return """ผมสามารถช่วยคุณได้หลายอย่าง เช่น:
1. ตอบคำถามทั่วไป
2. วิเคราะห์ข้อมูล
3. แปลภาษา
4. เขียนโค้ดและให้คำแนะนำทางเทคนิค
5. สรุปข้อมูลและเนื้อหา

คุณสามารถถามคำถามใดๆ และผมจะพยายามช่วยเหลืออย่างดีที่สุดครับ"""
    else:
        return f"คุณถามว่า: '{user_input}'\n\nนี่คือคำตอบจาก {model} (ความคิดสร้างสรรค์: {creativity}, ความยาวสูงสุด: {max_length} ตัวอักษร)\n\nขอบคุณที่ใช้บริการ OpenHands AI Assistant ครับ"


# เมื่อผู้ใช้ส่งข้อความ
if user_prompt:
    # เพิ่มข้อความของผู้ใช้เข้าไปในประวัติ
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    display_chat(user_prompt, "user")

    # รับคำตอบจาก AI
    response = get_ai_response(
        user_prompt, ai_model, creativity_level, max_token_length
    )

    # เพิ่มคำตอบลงในประวัติ
    st.session_state.messages.append({"role": "assistant", "content": response})
    display_chat(response, "assistant")

# ปุ่มล้างประวัติแชท
if st.button("ล้างประวัติแชท"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p class='footer'>© 2023 OpenHands AI Assistant | เวอร์ชัน 1.0.0 | สงวนลิขสิทธิ์</p>",
    unsafe_allow_html=True,
)
