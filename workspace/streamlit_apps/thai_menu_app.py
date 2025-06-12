import time
from datetime import datetime

import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="OpenHands - เมนูภาษาไทย",
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
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .highlight {
        color: #1E88E5;
        font-weight: bold;
    }
    .menu-button {
        text-align: center;
        padding: 0.75rem;
        background-color: #1E88E5;
        color: white;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
    }
    .menu-button:hover {
        background-color: #0D47A1;
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
    "<h1 class='main-header'>👐 OpenHands - เมนูภาษาไทย</h1>", unsafe_allow_html=True
)
st.markdown("---")

# สร้าง sidebar สำหรับเมนูหลัก
with st.sidebar:
    st.header("📋 เมนูหลัก")

    # เมนูหลัก
    menu_selection = st.radio(
        "เลือกเมนู:", ["หน้าหลัก", "เครื่องมือ AI", "วิเคราะห์ข้อมูล", "จัดการธุรกรรม", "ตั้งค่า"]
    )

    st.markdown("---")

    # ข้อมูลเวอร์ชัน
    st.caption("เวอร์ชัน: 1.0.0")
    st.caption(f"วันที่: {datetime.now().strftime('%d/%m/%Y')}")

    # ปุ่มเชื่อมต่อ API
    st.markdown("### ตั้งค่า API")
    api_key = st.text_input("API Key:", type="password")
    if st.button("เชื่อมต่อ API"):
        with st.spinner("กำลังเชื่อมต่อ..."):
            time.sleep(1)
            st.success("เชื่อมต่อ API สำเร็จ!")

# แสดงเนื้อหาตามเมนูที่เลือก
if menu_selection == "หน้าหลัก":
    st.markdown(
        "<h2 class='sub-header'>🏠 ยินดีต้อนรับสู่ OpenHands</h2>", unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        <div class='card'>
            <h3>เริ่มต้นใช้งาน OpenHands</h3>
            <p>OpenHands เป็นระบบ AI Assistant ที่ช่วยให้คุณทำงานได้อย่างมีประสิทธิภาพมากขึ้น ด้วยความสามารถในการวิเคราะห์ข้อมูล, ตอบคำถาม, และช่วยจัดการงานต่างๆ</p>
            <p>คุณสามารถเริ่มต้นใช้งานได้ง่ายๆ โดยเลือกเมนูที่คุณต้องการจากแถบด้านซ้าย</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class='card'>
            <h3>ข่าวสารและอัปเดตล่าสุด</h3>
            <ul>
                <li><span class='highlight'>ใหม่!</span> ระบบวิเคราะห์ธุรกรรมอัตโนมัติด้วย AI</li>
                <li><span class='highlight'>ใหม่!</span> รองรับการใช้งานภาษาไทยอย่างเต็มรูปแบบ</li>
                <li>อัปเดตระบบความปลอดภัยเพื่อปกป้องข้อมูลของคุณ</li>
                <li>เพิ่มเครื่องมือวิเคราะห์ข้อมูลใหม่</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class='card'>
            <h3>เมนูลัด</h3>
            <div class='menu-button'>🤖 เริ่มใช้งาน AI</div>
            <div class='menu-button'>📊 วิเคราะห์ข้อมูล</div>
            <div class='menu-button'>💳 จัดการธุรกรรม</div>
            <div class='menu-button'>⚙️ ตั้งค่าระบบ</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class='card'>
            <h3>สถิติการใช้งาน</h3>
            <p>จำนวนธุรกรรม: <span class='highlight'>256</span></p>
            <p>คำขอ AI ที่ใช้: <span class='highlight'>1,024</span></p>
            <p>เครดิตคงเหลือ: <span class='highlight'>10,000</span></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

elif menu_selection == "เครื่องมือ AI":
    st.markdown("<h2 class='sub-header'>🤖 เครื่องมือ AI</h2>", unsafe_allow_html=True)

    tools = [
        {
            "ชื่อ": "ChatBot ภาษาไทย",
            "คำอธิบาย": "โต้ตอบกับ AI ด้วยภาษาไทยที่เข้าใจบริบทและวัฒนธรรมไทย",
            "หมวดหมู่": "สนทนา",
        },
        {
            "ชื่อ": "วิเคราะห์เอกสาร",
            "คำอธิบาย": "สกัดข้อมูลสำคัญจากเอกสารภาษาไทยโดยอัตโนมัติ",
            "หมวดหมู่": "เอกสาร",
        },
        {
            "ชื่อ": "แปลภาษา AI",
            "คำอธิบาย": "แปลภาษาอังกฤษเป็นไทยและไทยเป็นอังกฤษอย่างเป็นธรรมชาติ",
            "หมวดหมู่": "ภาษา",
        },
        {
            "ชื่อ": "สรุปเนื้อหา",
            "คำอธิบาย": "สรุปเนื้อหาข้อความยาวๆ ให้กระชับและได้ใจความสำคัญ",
            "หมวดหมู่": "เนื้อหา",
        },
        {
            "ชื่อ": "ตรวจสอบไวยากรณ์",
            "คำอธิบาย": "ตรวจสอบและแก้ไขไวยากรณ์ภาษาไทยให้ถูกต้อง",
            "หมวดหมู่": "ภาษา",
        },
        {
            "ชื่อ": "วิเคราะห์ความรู้สึก",
            "คำอธิบาย": "วิเคราะห์ความรู้สึกจากข้อความภาษาไทย",
            "หมวดหมู่": "วิเคราะห์",
        },
    ]

    # แสดงเครื่องมือ AI ในรูปแบบตาราง
    st.dataframe(
        pd.DataFrame(tools),
        use_container_width=True,
        column_config={
            "ชื่อ": st.column_config.TextColumn(
                "ชื่อเครื่องมือ",
                width="medium",
            ),
            "คำอธิบาย": st.column_config.TextColumn(
                "รายละเอียด",
                width="large",
            ),
            "หมวดหมู่": st.column_config.TextColumn(
                "หมวดหมู่",
                width="small",
            ),
        },
        hide_index=True,
    )

    # ส่วนทดลองใช้งาน AI
    st.markdown(
        "<h3 class='sub-header'>ทดลองใช้งาน AI Chat</h3>", unsafe_allow_html=True
    )

    with st.form("ai_chat_form"):
        user_input = st.text_area(
            "พิมพ์ข้อความภาษาไทย:", "สวัสดี ฉันอยากรู้เกี่ยวกับการใช้งาน AI ในธุรกิจ"
        )
        submitted = st.form_submit_button("ส่งข้อความ")

        if submitted:
            with st.spinner("AI กำลังคิด..."):
                time.sleep(1.5)
                st.info(
                    "สวัสดีครับ! การใช้ AI ในธุรกิจมีประโยชน์มากมาย เช่น:\n\n"
                    "1. การวิเคราะห์ข้อมูลลูกค้าเพื่อเข้าใจพฤติกรรมและความต้องการ\n"
                    "2. การใช้ระบบ Chatbot เพื่อให้บริการลูกค้าตลอด 24 ชั่วโมง\n"
                    "3. การทำนายแนวโน้มตลาดและพฤติกรรมผู้บริโภค\n"
                    "4. การเพิ่มประสิทธิภาพในกระบวนการทำงานด้วยระบบอัตโนมัติ\n\n"
                    "คุณสนใจการประยุกต์ใช้ AI ในธุรกิจด้านไหนเป็นพิเศษครับ?"
                )

elif menu_selection == "วิเคราะห์ข้อมูล":
    st.markdown("<h2 class='sub-header'>📊 วิเคราะห์ข้อมูล</h2>", unsafe_allow_html=True)

    # สร้างข้อมูลจำลอง
    import numpy as np

    # ข้อมูลยอดขายรายเดือน
    months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย."]
    sales_data = np.array([120, 150, 140, 180, 210, 240])

    # สร้างกราฟยอดขาย
    st.subheader("📈 ยอดขายรายเดือน")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(months, sales_data, color="#1E88E5")
    ax.set_xlabel("เดือน")
    ax.set_ylabel("ยอดขาย (พันบาท)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for i, v in enumerate(sales_data):
        ax.text(i, v + 5, str(v), ha="center", fontweight="bold")

    st.pyplot(fig)

    # แสดงข้อมูลสรุป
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="ยอดขายรวม", value=f"{sales_data.sum():,} พันบาท", delta="+15.2%"
        )

    with col2:
        st.metric(
            label="ยอดขายเฉลี่ย", value=f"{sales_data.mean():.1f} พันบาท", delta="+8.5%"
        )

    with col3:
        st.metric(
            label="ยอดขายสูงสุด", value=f"{sales_data.max():,} พันบาท", delta="เดือนมิถุนายน"
        )

    # เพิ่มส่วนอัปโหลดข้อมูล
    st.markdown("<h3 class='sub-header'>อัปโหลดข้อมูลของคุณ</h3>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "เลือกไฟล์ CSV หรือ Excel เพื่อวิเคราะห์", type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        st.success("อัปโหลดไฟล์สำเร็จ! ระบบพร้อมวิเคราะห์ข้อมูลของคุณ")

        # จำลองส่วนของการเลือกวิเคราะห์
        analysis_type = st.selectbox(
            "เลือกประเภทการวิเคราะห์:",
            ["การวิเคราะห์แนวโน้ม", "การวิเคราะห์ความสัมพันธ์", "การวิเคราะห์กลุ่ม", "การพยากรณ์"],
        )

        if st.button("เริ่มวิเคราะห์"):
            with st.spinner("กำลังวิเคราะห์ข้อมูล..."):
                time.sleep(2)
                st.info("การวิเคราะห์เสร็จสิ้น! กรุณาดูผลลัพธ์ด้านล่าง")
                st.json(
                    {
                        "ผลการวิเคราะห์": "สำเร็จ",
                        "ประเภทการวิเคราะห์": analysis_type,
                        "จำนวนข้อมูล": 1250,
                        "ความแม่นยำ": "92.5%",
                        "เวลาที่ใช้": "1.2 วินาที",
                    }
                )

elif menu_selection == "จัดการธุรกรรม":
    st.markdown("<h2 class='sub-header'>💳 จัดการธุรกรรม</h2>", unsafe_allow_html=True)

    # แสดงตัวเลือกร้านค้า
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🛒 เลือกร้านค้า")

        merchant = st.selectbox(
            "ร้านค้า:",
            ["Shopee", "Lazada", "Amazon", "eBay", "Alibaba", "JD Central", "Walmart"],
        )

        card_type = st.selectbox(
            "ประเภทบัตร:", ["Visa", "Mastercard", "JCB", "American Express", "UnionPay"]
        )

        bin_number = st.text_input("BIN (6 หลัก):", "451234")

        use_ai = st.checkbox("ใช้ AI แนะนำบัตรที่เหมาะสม", True)

        if st.button("เริ่มดำเนินการ", type="primary"):
            with st.spinner("กำลังดำเนินการ..."):
                progress_bar = st.progress(0)
                for i in range(101):
                    progress_bar.progress(i)
                    time.sleep(0.02)

                # สุ่มผลลัพธ์
                import random

                result = random.choice(["สำเร็จ", "ล้มเหลว"])

                if result == "สำเร็จ":
                    st.success(f"ดำเนินการสำเร็จ! ร้านค้า {merchant} ยอมรับบัตร {card_type}")
                else:
                    st.error(f"ดำเนินการล้มเหลว! ร้านค้า {merchant} ปฏิเสธบัตร {card_type}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 ประวัติการทำธุรกรรม")

        # สร้างข้อมูลประวัติการทำธุรกรรมจำลอง
        transaction_history = [
            {
                "วันที่": "01/05/2023",
                "ร้านค้า": "Shopee",
                "บัตร": "Visa",
                "จำนวนเงิน": "฿1,200",
                "สถานะ": "สำเร็จ",
            },
            {
                "วันที่": "03/05/2023",
                "ร้านค้า": "Lazada",
                "บัตร": "Mastercard",
                "จำนวนเงิน": "฿3,500",
                "สถานะ": "สำเร็จ",
            },
            {
                "วันที่": "07/05/2023",
                "ร้านค้า": "Amazon",
                "บัตร": "Visa",
                "จำนวนเงิน": "฿2,800",
                "สถานะ": "ล้มเหลว",
            },
            {
                "วันที่": "12/05/2023",
                "ร้านค้า": "eBay",
                "บัตร": "JCB",
                "จำนวนเงิน": "฿5,200",
                "สถานะ": "สำเร็จ",
            },
            {
                "วันที่": "15/05/2023",
                "ร้านค้า": "Shopee",
                "บัตร": "UnionPay",
                "จำนวนเงิน": "฿1,800",
                "สถานะ": "สำเร็จ",
            },
        ]

        # แสดงตารางประวัติการทำธุรกรรม
        transaction_df = pd.DataFrame(transaction_history)
        st.dataframe(
            transaction_df,
            use_container_width=True,
            column_config={
                "สถานะ": st.column_config.TextColumn(
                    "สถานะ", width="small", help="สถานะของธุรกรรม"
                )
            },
            hide_index=True,
        )

        # สร้างกราฟแสดงสถิติ
        st.subheader("📊 สถิติการทำธุรกรรม")

        # นับจำนวนธุรกรรมที่สำเร็จและล้มเหลว
        success_count = sum(1 for t in transaction_history if t["สถานะ"] == "สำเร็จ")
        failed_count = sum(1 for t in transaction_history if t["สถานะ"] == "ล้มเหลว")

        # สร้างแผนภูมิวงกลม
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            [success_count, failed_count],
            labels=["สำเร็จ", "ล้มเหลว"],
            autopct="%1.1f%%",
            colors=["#4CAF50", "#F44336"],
            startangle=90,
        )
        ax.set_title("อัตราความสำเร็จ")
        st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

elif menu_selection == "ตั้งค่า":
    st.markdown("<h2 class='sub-header'>⚙️ ตั้งค่าระบบ</h2>", unsafe_allow_html=True)

    tabs = st.tabs(["การแสดงผล", "ภาษา", "การแจ้งเตือน", "API", "ความปลอดภัย"])

    with tabs[0]:
        st.subheader("การแสดงผล")
        theme = st.selectbox("ธีม:", ["สว่าง", "มืด", "อัตโนมัติ (ตามระบบ)"])
        layout = st.selectbox("เค้าโครง:", ["มาตรฐาน", "กะทัดรัด", "กว้าง"])
        font_size = st.slider("ขนาดตัวอักษร:", 12, 24, 16)

        st.button("บันทึกการตั้งค่า")

    with tabs[1]:
        st.subheader("ภาษา")
        language = st.selectbox("ภาษา:", ["ไทย", "อังกฤษ", "จีน", "ญี่ปุ่น"])
        date_format = st.selectbox(
            "รูปแบบวันที่:", ["วว/ดด/ปปปป", "ดด/วว/ปปปป", "ปปปป-ดด-วว"]
        )

        st.button("บันทึกการตั้งค่าภาษา")

    with tabs[2]:
        st.subheader("การแจ้งเตือน")
        email_notify = st.checkbox("แจ้งเตือนทางอีเมล", True)
        sms_notify = st.checkbox("แจ้งเตือนทาง SMS", False)
        push_notify = st.checkbox("แจ้งเตือนผ่านแอป", True)

        st.text_input("อีเมลสำหรับการแจ้งเตือน:", "example@mail.com")
        st.text_input("เบอร์โทรศัพท์:", "+66891234567")

        st.button("บันทึกการตั้งค่าการแจ้งเตือน")

    with tabs[3]:
        st.subheader("API")
        api_provider = st.selectbox(
            "ผู้ให้บริการ API:", ["OpenAI", "Google", "Anthropic", "Mistral", "OpenRouter"]
        )
        api_key = st.text_input("API Key:", type="password")
        api_model = st.selectbox(
            "โมเดล:",
            ["GPT-4", "Claude 3 Opus", "Gemini Pro", "Mistral Large", "Custom"],
        )

        st.button("ทดสอบการเชื่อมต่อ API")
        st.button("บันทึกการตั้งค่า API")

    with tabs[4]:
        st.subheader("ความปลอดภัย")
        st.checkbox("เปิดใช้งานการยืนยันตัวตนสองชั้น (2FA)", True)
        st.checkbox("เข้ารหัสข้อมูลทั้งหมด", True)
        st.checkbox("ล็อกเอาต์อัตโนมัติหลังจากไม่ใช้งาน 30 นาที", True)

        st.button("เปลี่ยนรหัสผ่าน")
        st.button("บันทึกการตั้งค่าความปลอดภัย")

# Footer
st.markdown("---")
st.markdown(
    "<p class='footer'>© 2023 OpenHands AI Assistant | เวอร์ชัน 1.0.0 | สงวนลิขสิทธิ์</p>",
    unsafe_allow_html=True,
)
