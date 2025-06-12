# AutoGen Example
import autogen

# กำหนดค่า API
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": "your-api-key-here",
    }
]

# สร้าง AI Assistant และ User Proxy
assistant = autogen.AssistantAgent(
    name="thai_assistant",
    llm_config={"config_list": config_list},
    system_message="คุณเป็นผู้ช่วย AI ภาษาไทยที่ฉลาดและเป็นมิตร ให้คำตอบที่ชัดเจนและสมบูรณ์"
)

user_proxy = autogen.UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding"},
)

# เริ่มการสนทนา
user_proxy.initiate_chat(
    assistant,
    message="ช่วยเขียนฟังก์ชัน Python ง่ายๆ ที่รับชื่อและวันเกิด แล้วคำนวณอายุปัจจุบัน พร้อมทั้งแสดงข้อความทักทาย"
)