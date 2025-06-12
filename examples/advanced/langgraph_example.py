#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LangGraph Example - สร้าง Agent Flow ที่มี Memory และสถานะ
ตัวอย่างการใช้ LangGraph สร้าง Agent ที่จดจำบทสนทนาและจัดการ Flow การทำงาน
"""

import operator
import os
from typing import Annotated, Any, Dict, List, TypedDict, Union

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# นำเข้า LangGraph
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor, tools

# กำหนด OpenAI API Key (ในตัวอย่างนี้ให้ใช้ตัวแปรสภาพแวดล้อม)
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# สร้างโมเดล LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# กำหนดโครงสร้างสถานะ
class AgentState(TypedDict):
    # ประวัติการสนทนา
    messages: List[Union[HumanMessage, AIMessage]]
    # สถานะหรือข้อมูลอื่นๆ ที่ต้องการเก็บ
    user_info: Dict[str, Any]
    # สถานะการทำงาน
    status: str


# สร้างเครื่องมือสำหรับ Agent
@tools.tool
def check_transaction_history(merchant_id: str) -> str:
    """ตรวจสอบประวัติการทำธุรกรรมกับร้านค้า"""
    # จำลองข้อมูลจากฐานข้อมูล
    transaction_history = {
        "merchant_a": {
            "count": 25,
            "total_amount": 12500.75,
            "last_transaction": "2023-06-15",
            "status": "active",
        },
        "merchant_b": {
            "count": 5,
            "total_amount": 2500.50,
            "last_transaction": "2023-07-20",
            "status": "pending_review",
        },
        "merchant_c": {
            "count": 0,
            "total_amount": 0,
            "last_transaction": None,
            "status": "new",
        },
    }

    # ทำให้เป็นตัวพิมพ์เล็กและแทนที่ช่องว่าง
    merchant_id = merchant_id.lower().replace(" ", "_")

    if merchant_id in transaction_history:
        data = transaction_history[merchant_id]
        return f"พบข้อมูลธุรกรรมของร้านค้า {merchant_id}: จำนวน {data['count']} รายการ, ยอดรวม {data['total_amount']} บาท, ธุรกรรมล่าสุด {data['last_transaction'] or 'ไม่มี'}, สถานะ: {data['status']}"
    else:
        return f"ไม่พบข้อมูลธุรกรรมสำหรับร้านค้า {merchant_id}"


@tools.tool
def check_merchant_status(merchant_id: str) -> str:
    """ตรวจสอบสถานะของร้านค้า"""
    # จำลองข้อมูลร้านค้า
    merchant_database = {
        "merchant_a": {
            "name": "ร้านค้า A",
            "status": "verified",
            "category": "อาหารและเครื่องดื่ม",
            "risk_level": "low",
        },
        "merchant_b": {
            "name": "ร้านค้า B",
            "status": "under_review",
            "category": "เครื่องใช้ไฟฟ้า",
            "risk_level": "medium",
        },
        "merchant_c": {
            "name": "ร้านค้า C",
            "status": "pending",
            "category": "แฟชั่น",
            "risk_level": "unknown",
        },
    }

    # ทำให้เป็นตัวพิมพ์เล็กและแทนที่ช่องว่าง
    merchant_id = merchant_id.lower().replace(" ", "_")

    if merchant_id in merchant_database:
        data = merchant_database[merchant_id]
        return f"ข้อมูลร้านค้า {data['name']}: สถานะ {data['status']}, หมวดหมู่ {data['category']}, ระดับความเสี่ยง {data['risk_level']}"
    else:
        return f"ไม่พบข้อมูลร้านค้า {merchant_id}"


@tools.tool
def update_user_profile(name: str, value: str) -> str:
    """อัปเดตข้อมูลในโปรไฟล์ของผู้ใช้"""
    return f"อัปเดตข้อมูล '{name}' เป็น '{value}' เรียบร้อยแล้ว"


# สร้าง Tool Executor
all_tools = [check_transaction_history, check_merchant_status, update_user_profile]
tool_executor = ToolExecutor(all_tools)

# สร้าง prompt สำหรับ Agent
agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """คุณคือผู้ช่วยอัจฉริยะสำหรับระบบชำระเงิน คุณสามารถช่วยผู้ใช้ตรวจสอบข้อมูลร้านค้าและธุรกรรมได้
            
คุณสามารถเข้าถึงเครื่องมือต่อไปนี้:
{tool_descriptions}

ข้อมูลของผู้ใช้:
{user_info}

คำแนะนำ:
1. พยายามเข้าใจความต้องการของผู้ใช้ให้ได้มากที่สุด
2. หากต้องการข้อมูลเพิ่มเติม ให้ถามคำถามกับผู้ใช้
3. ใช้เครื่องมือที่เหมาะสมเพื่อตอบคำถามของผู้ใช้
4. อย่าสร้างข้อมูลเท็จ ให้ใช้ข้อมูลจากเครื่องมือเท่านั้น

ในการตอบคำถาม ให้อธิบายวิธีการหาคำตอบด้วย แต่อย่ามากเกินไป
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# สร้าง prompt สำหรับวิเคราะห์ความต้องการ
router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """คุณเป็นผู้วิเคราะห์ความต้องการของผู้ใช้ในบทสนทนา

อ่านข้อความล่าสุดของผู้ใช้แล้วตัดสินใจว่าจะดำเนินการต่อไปอย่างไร ตัวเลือกของคุณคือ:

1. "use_tool" - ถ้าผู้ใช้ต้องการทราบข้อมูลที่ต้องใช้เครื่องมือ เช่น ข้อมูลร้านค้า ประวัติธุรกรรม
2. "update_profile" - ถ้าผู้ใช้ต้องการอัปเดตข้อมูลในโปรไฟล์
3. "answer" - ถ้าคุณสามารถตอบคำถามได้โดยตรงโดยไม่ต้องใช้เครื่องมือเพิ่มเติม

คุณต้องตอบเพียงอย่างใดอย่างหนึ่งเท่านั้น: "use_tool", "update_profile" หรือ "answer"
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Parser สำหรับเครื่องมือ
tool_parser = JsonOutputParser()


# ฟังก์ชันสำหรับสร้าง prompt ของเครื่องมือ
def create_tool_prompt(tool_names):
    tool_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """คุณเป็นผู้ช่วยสำหรับเลือกและใช้เครื่องมือ คุณต้องเลือกเครื่องมือที่เหมาะสมจากรายการด้านล่าง:

{tool_descriptions}

ข้อความล่าสุดของผู้ใช้คือ:
{last_message}

เลือกเครื่องมือที่เหมาะสมที่สุดและระบุพารามิเตอร์ที่จำเป็น ตอบในรูปแบบ JSON ตามนี้:
```
{{
    "tool": "ชื่อเครื่องมือ",
    "tool_input": "พารามิเตอร์ที่ต้องใช้"
}}
```
                """,
            ),
        ]
    )
    return tool_prompt


# ฟังก์ชันต่างๆ สำหรับ Graph
def get_last_message(state: AgentState) -> str:
    """ดึงข้อความล่าสุดจากผู้ใช้"""
    return state["messages"][-1].content


def route(state: AgentState) -> str:
    """ตัดสินใจว่าจะทำอะไรต่อไป"""
    messages = state["messages"]
    response = llm.invoke(router_prompt.format(messages=messages))

    action = response.content.strip().lower()
    print(f"การตัดสินใจ: {action}")

    return action


def call_tool(state: AgentState) -> AgentState:
    """เรียกใช้เครื่องมือตามที่ต้องการ"""
    messages = state["messages"]
    last_message = get_last_message(state)

    # สร้าง tool description
    tool_descriptions = "\n".join(
        [f"{tool.name}: {tool.description}" for tool in all_tools]
    )

    # เลือกเครื่องมือ
    tool_prompt = create_tool_prompt(all_tools)
    tool_response = llm.invoke(
        tool_prompt.format(
            tool_descriptions=tool_descriptions,
            last_message=last_message,
        )
    )

    # แปลง response เป็น JSON
    tool_choice = tool_parser.parse(tool_response.content)

    # เรียกใช้เครื่องมือ
    tool_result = tool_executor.execute(
        {
            "name": tool_choice["tool"],
            "input": tool_choice["tool_input"],
        }
    )

    # สร้างข้อความจาก AI ด้วยผลลัพธ์
    return {
        **state,
        "messages": messages
        + [AIMessage(content=f"ผลลัพธ์จากเครื่องมือ {tool_choice['tool']}: {tool_result}")],
    }


def update_profile(state: AgentState) -> AgentState:
    """อัปเดตข้อมูลโปรไฟล์ของผู้ใช้"""
    messages = state["messages"]
    last_message = get_last_message(state)

    # วิเคราะห์ว่าผู้ใช้ต้องการอัปเดตอะไร
    profile_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """วิเคราะห์ว่าผู้ใช้ต้องการอัปเดตข้อมูลอะไรในโปรไฟล์ ตอบในรูปแบบ JSON:
```
{
    "field": "ชื่อฟิลด์ที่ต้องการอัปเดต",
    "value": "ค่าใหม่"
}
```
            """,
            ),
            HumanMessage(content=last_message),
        ]
    )

    profile_response = llm.invoke(profile_prompt)
    update_data = tool_parser.parse(profile_response.content)

    # เรียกใช้เครื่องมืออัปเดตโปรไฟล์
    tool_result = tool_executor.execute(
        {
            "name": "update_user_profile",
            "input": {
                "name": update_data["field"],
                "value": update_data["value"],
            },
        }
    )

    # อัปเดตข้อมูลในสถานะ
    new_user_info = {**state["user_info"]}
    new_user_info[update_data["field"]] = update_data["value"]

    # สร้างข้อความจาก AI ด้วยผลลัพธ์
    return {
        **state,
        "messages": messages + [AIMessage(content=f"อัปเดตข้อมูล: {tool_result}")],
        "user_info": new_user_info,
    }


def answer(state: AgentState) -> AgentState:
    """ตอบคำถามโดยตรง"""
    messages = state["messages"]
    user_info = state["user_info"]

    # สร้าง tool description
    tool_descriptions = "\n".join(
        [f"{tool.name}: {tool.description}" for tool in all_tools]
    )

    # Generate response
    response = llm.invoke(
        agent_prompt.format(
            messages=messages,
            tool_descriptions=tool_descriptions,
            user_info="\n".join([f"{k}: {v}" for k, v in user_info.items()]),
        )
    )

    return {
        **state,
        "messages": messages + [response],
        "status": "answered",
    }


# สร้าง Graph
def create_graph():
    # กำหนด builder
    builder = StateGraph(AgentState)

    # เพิ่ม nodes
    builder.add_node("route", route)
    builder.add_node("call_tool", call_tool)
    builder.add_node("update_profile", update_profile)
    builder.add_node("answer", answer)

    # กำหนด edges
    builder.set_entry_point("route")
    builder.add_edge("route", "call_tool", condition=lambda x: x == "use_tool")
    builder.add_edge(
        "route", "update_profile", condition=lambda x: x == "update_profile"
    )
    builder.add_edge("route", "answer", condition=lambda x: x == "answer")

    # เส้นทางจาก call_tool และ update_profile กลับไปที่ route
    builder.add_edge("call_tool", "route")
    builder.add_edge("update_profile", "route")

    # จาก answer ไปที่ END
    builder.add_edge("answer", END)

    # สร้าง graph
    return builder.compile()


# ฟังก์ชันหลักสำหรับรัน agent
def run_agent():
    # สร้าง graph
    graph = create_graph()

    # ข้อมูลเริ่มต้นของผู้ใช้
    initial_user_info = {
        "name": "คุณสมชาย",
        "membership_level": "Silver",
        "preferred_card": "Visa",
        "language": "Thai",
    }

    # สถานะเริ่มต้น
    initial_state = {
        "messages": [HumanMessage(content="สวัสดี ฉันอยากรู้ข้อมูลเกี่ยวกับร้านค้า A")],
        "user_info": initial_user_info,
        "status": "started",
    }

    # รัน graph กับสถานะเริ่มต้น
    result = graph.invoke(initial_state)

    # แสดงผลลัพธ์ของการสนทนา
    print("\n=== ผลลัพธ์การสนทนา ===")
    for i, message in enumerate(result["messages"]):
        speaker = "ผู้ใช้" if isinstance(message, HumanMessage) else "AI"
        print(f"{speaker}: {message.content}")
        print("-" * 50)

    # ทดสอบสนทนาต่อเนื่อง
    print("\n=== ทดสอบสนทนาต่อเนื่อง ===")
    follow_up_state = {
        **result,
        "messages": result["messages"]
        + [HumanMessage(content="ฉันอยากอัปเดตบัตรที่ต้องการเป็น Mastercard")],
        "status": "continued",
    }

    follow_up_result = graph.invoke(follow_up_state)

    # แสดงผลลัพธ์ของการสนทนาต่อเนื่อง
    print("\n=== ผลลัพธ์การสนทนาต่อเนื่อง ===")
    for i, message in enumerate(follow_up_result["messages"]):
        speaker = "ผู้ใช้" if isinstance(message, HumanMessage) else "AI"
        print(f"{speaker}: {message.content}")
        print("-" * 50)

    # แสดงข้อมูลผู้ใช้ที่อัปเดตแล้ว
    print("\n=== ข้อมูลผู้ใช้ที่อัปเดตแล้ว ===")
    for key, value in follow_up_result["user_info"].items():
        print(f"{key}: {value}")


# รัน agent ถ้าเรียกใช้โดยตรง
if __name__ == "__main__":
    print("===== LangGraph Agent with Memory Example =====")
    run_agent()
