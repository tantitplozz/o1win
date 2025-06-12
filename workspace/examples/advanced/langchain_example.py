"""
LangChain Example - สาธิตการใช้งาน LangChain กับ OpenHands ในกรณีใช้งานจริง
"""

import os
from datetime import datetime

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# กำหนดตัวแปรสภาพแวดล้อม
os.environ["OPENAI_API_KEY"] = "your_api_key_here"  # เปลี่ยนเป็น API key ของคุณ


# 1. สร้าง Simple Chain - วิเคราะห์ Gateway
def analyze_payment_gateway(gateway_name):
    """วิเคราะห์ข้อมูลของ Payment Gateway"""
    prompt = ChatPromptTemplate.from_template(
        "คุณเป็นผู้เชี่ยวชาญด้านระบบการชำระเงิน "
        "วิเคราะห์ Payment Gateway ชื่อ {gateway} และให้ข้อมูลดังนี้:\n"
        "1. ระบบป้องกันการฉ้อโกงที่น่าจะใช้\n"
        "2. บัตรที่รองรับ\n"
        "3. ประเทศที่ไม่รองรับ\n"
        "4. ข้อแนะนำในการใช้งาน"
    )

    model = ChatOpenAI(temperature=0)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    return chain.invoke({"gateway": gateway_name})


# 2. สร้าง Chain with Memory - บันทึกประวัติการใช้บัตร
def create_card_advisor():
    """สร้าง Advisor ที่ช่วยแนะนำบัตรที่เหมาะสม โดยจดจำประวัติการใช้งาน"""
    template = """
    คุณเป็นผู้เชี่ยวชาญด้านบัตรเครดิต ช่วยแนะนำบัตรที่เหมาะสมสำหรับการใช้งานต่างๆ
    
    ประวัติการสนทนาก่อนหน้า:
    {chat_history}
    
    ลูกค้า: {human_input}
    ผู้เชี่ยวชาญ: """

    prompt = ChatPromptTemplate.from_template(template)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(temperature=0.7)

    conversation = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    return conversation


# 3. สร้าง Agent - ระบบวิเคราะห์การชำระเงินแบบอัตโนมัติ
def create_payment_agent():
    """สร้าง Agent ที่สามารถใช้เครื่องมือหลายอย่างเพื่อวิเคราะห์การชำระเงิน"""

    # เครื่องมือที่ Agent สามารถใช้ได้
    tools = [
        Tool(
            name="Gateway Analyzer",
            func=analyze_payment_gateway,
            description="ใช้เมื่อต้องการวิเคราะห์ข้อมูลของ Payment Gateway",
        ),
        Tool(
            name="Transaction Logger",
            func=lambda x: f"บันทึกธุรกรรม: {x} เวลา: {datetime.now()}",
            description="ใช้เมื่อต้องการบันทึกข้อมูลธุรกรรม",
        ),
        Tool(
            name="Card Checker",
            func=lambda x: (
                f"ตรวจสอบบัตร {x}: Valid" if len(x) > 10 else f"ตรวจสอบบัตร {x}: Invalid"
            ),
            description="ใช้เมื่อต้องการตรวจสอบความถูกต้องของบัตร",
        ),
    ]

    # สร้าง Agent
    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    return agent


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("=== ตัวอย่างการใช้งาน LangChain กับ OpenHands ===\n")

    # 1. ทดสอบ Simple Chain
    print("--- วิเคราะห์ Payment Gateway ---")
    gateway_info = analyze_payment_gateway("Stripe")
    print(gateway_info)
    print("\n")

    # 2. ทดสอบ Chain with Memory
    print("--- ที่ปรึกษาด้านบัตรเครดิตอัจฉริยะ ---")
    advisor = create_card_advisor()

    responses = [
        advisor.predict(human_input="ฉันต้องการใช้บัตรสำหรับซื้อของออนไลน์จากต่างประเทศ"),
        advisor.predict(human_input="ฉันมีบัตร Visa และ Mastercard อันไหนดีกว่ากัน?"),
        advisor.predict(human_input="แล้วถ้าจะซื้อของจาก Amazon ล่ะ?"),
    ]

    for i, response in enumerate(responses):
        print(f"คำถามที่ {i+1}:")
        print(response)
        print("\n")

    # 3. ทดสอบ Agent
    print("--- ระบบวิเคราะห์การชำระเงินอัตโนมัติ ---")
    agent = create_payment_agent()

    agent_response = agent.run(
        "ฉันต้องการชำระเงินผ่าน PayPal แต่ต้องการทราบว่ามีระบบป้องกันอะไรบ้าง "
        "และช่วยตรวจสอบบัตรหมายเลข 4111111111111111 ให้หน่อย"
    )

    print("ผลลัพธ์จาก Agent:")
    print(agent_response)
