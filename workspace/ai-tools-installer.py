#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Tools Installer - เครื่องมือติดตั้งและตั้งค่าเทคโนโลยี AI ขั้นสูง
สำหรับใช้งานกับ OpenHands AI Assistant
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path


# สีสำหรับข้อความในเทอร์มินัล
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD} {text} {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_step(text):
    print(f"{Colors.BLUE}{Colors.BOLD}>> {text}...{Colors.ENDC}")


def print_success(text):
    print(f"{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}{Colors.BOLD}✗ {text}{Colors.ENDC}")


def run_command(command, shell=True, check=True):
    """รันคำสั่งและคืนค่าผลลัพธ์"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_error(f"เกิดข้อผิดพลาดขณะรันคำสั่ง: {command}")
        print(f"{Colors.RED}{e.stderr}{Colors.ENDC}")
        return None


def check_docker():
    """ตรวจสอบว่า Docker กำลังทำงานหรือไม่"""
    print_step("ตรวจสอบสถานะ Docker")
    try:
        result = run_command("docker info", check=False)
        if result and "Server Version" in result:
            print_success("Docker กำลังทำงาน")
            return True
        else:
            print_error("Docker ไม่ได้ทำงานอยู่ กรุณาเปิด Docker Desktop ก่อน")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะตรวจสอบ Docker: {e}")
        return False


def check_openhands():
    """ตรวจสอบว่า OpenHands container กำลังทำงานหรือไม่"""
    print_step("ตรวจสอบสถานะ OpenHands")
    try:
        result = run_command("docker ps --format '{{.Names}}'", check=False)
        if result and "my-openhands-app" in result:
            print_success("OpenHands container กำลังทำงาน")
            return True
        else:
            print_error("OpenHands container ไม่ได้ทำงานอยู่ กรุณาเริ่มต้น OpenHands ก่อน")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะตรวจสอบ OpenHands: {e}")
        return False


def install_langchain():
    """ติดตั้ง LangChain - เฟรมเวิร์คสำหรับสร้าง AI applications ที่เชื่อมต่อกับ LLM"""
    print_step("ติดตั้ง LangChain")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install langchain langchain-openai"
        )
        if result:
            print_success("ติดตั้ง LangChain สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง LangChain ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง LangChain: {e}")
        return False


def install_huggingface():
    """ติดตั้ง Hugging Face Transformers - ไลบรารีสำหรับโมเดล AI แบบ transformer-based"""
    print_step("ติดตั้ง Hugging Face Transformers")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install transformers datasets tokenizers"
        )
        if result:
            print_success("ติดตั้ง Hugging Face Transformers สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง Hugging Face Transformers ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง Hugging Face Transformers: {e}")
        return False


def install_llama_index():
    """ติดตั้ง LlamaIndex - เครื่องมือสำหรับสร้าง retrieval-augmented generation บน LLM"""
    print_step("ติดตั้ง LlamaIndex")
    try:
        result = run_command("docker exec -it my-openhands-app pip install llama-index")
        if result:
            print_success("ติดตั้ง LlamaIndex สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง LlamaIndex ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง LlamaIndex: {e}")
        return False


def install_autogen():
    """ติดตั้ง AutoGen - เครื่องมือสำหรับสร้าง AI agents ที่สามารถทำงานร่วมกันได้"""
    print_step("ติดตั้ง Microsoft AutoGen")
    try:
        result = run_command("docker exec -it my-openhands-app pip install pyautogen")
        if result:
            print_success("ติดตั้ง Microsoft AutoGen สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง Microsoft AutoGen ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง Microsoft AutoGen: {e}")
        return False


def install_llamafile():
    """ติดตั้ง llamafile - เครื่องมือสำหรับรัน LLM บนเครื่องแบบ standalone"""
    print_step("ติดตั้ง llamafile")
    try:
        # สร้างโฟลเดอร์สำหรับ llamafile
        run_command("docker exec -it my-openhands-app mkdir -p /tools/llamafile")

        # ดาวน์โหลด llamafile
        run_command(
            "docker exec -it my-openhands-app curl -L -o /tools/llamafile/llamafile https://github.com/Mozilla-Ocho/llamafile/releases/download/0.6.1/llamafile-0.6.1"
        )

        # ให้สิทธิ์การรัน
        run_command(
            "docker exec -it my-openhands-app chmod +x /tools/llamafile/llamafile"
        )

        print_success("ติดตั้ง llamafile สำเร็จ")
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง llamafile: {e}")
        return False


def install_gpt4all():
    """ติดตั้ง GPT4All - โมเดล LLM ที่สามารถรันบนเครื่องได้"""
    print_step("ติดตั้ง GPT4All")
    try:
        result = run_command("docker exec -it my-openhands-app pip install gpt4all")
        if result:
            print_success("ติดตั้ง GPT4All สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง GPT4All ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง GPT4All: {e}")
        return False


def install_deep_learning_tools():
    """ติดตั้งเครื่องมือสำหรับ Deep Learning"""
    print_step("ติดตั้งเครื่องมือสำหรับ Deep Learning")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install torch torchvision tensorflow keras scikit-learn pandas numpy matplotlib"
        )
        if result:
            print_success("ติดตั้งเครื่องมือสำหรับ Deep Learning สำเร็จ")
            return True
        else:
            print_error("ติดตั้งเครื่องมือสำหรับ Deep Learning ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้งเครื่องมือสำหรับ Deep Learning: {e}")
        return False


def install_openai_tools():
    """ติดตั้ง OpenAI API และเครื่องมือที่เกี่ยวข้อง"""
    print_step("ติดตั้ง OpenAI API และเครื่องมือที่เกี่ยวข้อง")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install openai tiktoken"
        )
        if result:
            print_success("ติดตั้ง OpenAI API และเครื่องมือที่เกี่ยวข้องสำเร็จ")
            return True
        else:
            print_error("ติดตั้ง OpenAI API และเครื่องมือที่เกี่ยวข้องไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง OpenAI API และเครื่องมือที่เกี่ยวข้อง: {e}")
        return False


def install_nodejs_ai_tools():
    """ติดตั้งเครื่องมือ AI สำหรับ Node.js"""
    print_step("ติดตั้งเครื่องมือ AI สำหรับ Node.js")
    try:
        result = run_command(
            "docker exec -it my-openhands-app npm install -g @langchain/community @langchain/openai langchain"
        )
        if result:
            print_success("ติดตั้งเครื่องมือ AI สำหรับ Node.js สำเร็จ")
            return True
        else:
            print_error("ติดตั้งเครื่องมือ AI สำหรับ Node.js ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้งเครื่องมือ AI สำหรับ Node.js: {e}")
        return False


def create_examples():
    """สร้างไฟล์ตัวอย่างการใช้งานเครื่องมือ AI"""
    print_step("สร้างไฟล์ตัวอย่างการใช้งานเครื่องมือ AI")

    # สร้างโฟลเดอร์ examples หากยังไม่มี
    os.makedirs("examples", exist_ok=True)

    # ตัวอย่างการใช้งาน LangChain
    langchain_example = """
# LangChain Example
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ตั้งค่า API key (ควรใช้ environment variable จริงๆ)
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# สร้าง prompt template
prompt = PromptTemplate(
    input_variables=["product"],
    template="คุณคิดว่าควรตั้งชื่ออะไรให้กับ {product}? ให้ 5 ชื่อพร้อมเหตุผล",
)

# สร้าง chain
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# รันและแสดงผลลัพธ์
response = chain.run(product="แอปพลิเคชันสอนทำอาหารไทย")
print(response)
"""

    # ตัวอย่างการใช้งาน Hugging Face
    huggingface_example = """
# Hugging Face Example
from transformers import pipeline

# โหลดโมเดลสำหรับแปลภาษา
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-th")

# แปลภาษาอังกฤษเป็นภาษาไทย
english_text = "Artificial intelligence is transforming the world."
translation = translator(english_text)
print(f"English: {english_text}")
print(f"Thai: {translation[0]['translation_text']}")

# โหลดโมเดลสำหรับวิเคราะห์ความรู้สึก
sentiment_analyzer = pipeline("sentiment-analysis")

# วิเคราะห์ความรู้สึกของข้อความ
texts = ["I love this product!", "This was a terrible experience.", "It was okay, nothing special."]
for text in texts:
    result = sentiment_analyzer(text)
    print(f"Text: {text}")
    print(f"Sentiment: {result[0]['label']}, Score: {result[0]['score']:.4f}")
"""

    # ตัวอย่างการใช้งาน LlamaIndex
    llamaindex_example = """
# LlamaIndex Example
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI

# ตั้งค่า API key (ควรใช้ environment variable จริงๆ)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# สร้างโฟลเดอร์และไฟล์ตัวอย่าง
os.makedirs("data", exist_ok=True)
with open("data/thai_food.txt", "w", encoding="utf-8") as f:
    f.write('''
ต้มยำกุ้ง เป็นอาหารไทยที่มีชื่อเสียงระดับโลก มีรสชาติเปรี้ยว เผ็ด และหอมสมุนไพร โดยมีกุ้งเป็นส่วนประกอบหลัก
ผัดไทย เป็นอาหารไทยประเภทเส้นผัดที่ได้รับความนิยมมาก มีส่วนผสมหลักคือเส้นจันท์ ไข่ เต้าหู้ และถั่วงอก
ส้มตำ เป็นอาหารประจำภาคอีสานของประเทศไทย มีรสชาติเปรี้ยว เผ็ด เค็ม หวาน ทำจากมะละกอสับ กระเทียม พริกขี้หนู
''')

# โหลดเอกสารจากโฟลเดอร์
documents = SimpleDirectoryReader("data").load_data()

# ตั้งค่า LLM
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0))

# สร้างดัชนีสำหรับค้นหา
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# สร้าง query engine
query_engine = index.as_query_engine()

# ทดลองถามคำถาม
response = query_engine.query("บอกฉันเกี่ยวกับอาหารไทยที่มีรสเผ็ด")
print(response)
"""

    # ตัวอย่างการใช้งาน AutoGen
    autogen_example = """
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
"""

    # เขียนไฟล์ตัวอย่าง
    with open("examples/langchain_example.py", "w", encoding="utf-8") as f:
        f.write(langchain_example.strip())

    with open("examples/huggingface_example.py", "w", encoding="utf-8") as f:
        f.write(huggingface_example.strip())

    with open("examples/llamaindex_example.py", "w", encoding="utf-8") as f:
        f.write(llamaindex_example.strip())

    with open("examples/autogen_example.py", "w", encoding="utf-8") as f:
        f.write(autogen_example.strip())

    print_success("สร้างไฟล์ตัวอย่างสำเร็จ ตรวจสอบได้ที่โฟลเดอร์ examples/")
    return True


def create_setup_script():
    """สร้างสคริปต์ setup.py สำหรับการติดตั้งแพ็คเกจที่จำเป็น"""
    print_step("สร้างสคริปต์ setup.py")

    setup_script = """
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ai_tools",
    version="0.1.0",
    description="เครื่องมือ AI ขั้นสูงสำหรับ OpenHands",
    author="OpenHands User",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "openai",
        "tiktoken",
        "transformers",
        "datasets",
        "tokenizers",
        "llama-index",
        "pyautogen",
        "gpt4all",
        "torch",
        "torchvision",
        "tensorflow",
        "keras",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
    ],
    python_requires=">=3.8",
)
"""

    with open("setup.py", "w", encoding="utf-8") as f:
        f.write(setup_script.strip())

    print_success("สร้างสคริปต์ setup.py สำเร็จ")
    return True


def create_readme():
    """สร้างไฟล์ README.md สำหรับเครื่องมือ AI"""
    print_step("สร้างไฟล์ README.md")

    readme_content = """
# เครื่องมือ AI ขั้นสูงสำหรับ OpenHands

ไลบรารีและเครื่องมือ AI ขั้นสูงสำหรับใช้งานกับ OpenHands AI Assistant

## เครื่องมือที่ติดตั้ง

- **LangChain**: เฟรมเวิร์คสำหรับสร้าง AI applications ที่เชื่อมต่อกับ LLM
- **Hugging Face Transformers**: ไลบรารีสำหรับโมเดล AI แบบ transformer-based
- **LlamaIndex**: เครื่องมือสำหรับสร้าง retrieval-augmented generation บน LLM
- **Microsoft AutoGen**: เครื่องมือสร้าง AI agents ที่ทำงานร่วมกันได้
- **llamafile**: เครื่องมือสำหรับรัน LLM บนเครื่องแบบ standalone
- **GPT4All**: โมเดล LLM ที่สามารถรันบนเครื่องได้
- **Deep Learning Tools**: TensorFlow, PyTorch, Keras, scikit-learn, pandas, numpy
- **OpenAI Tools**: OpenAI API client, tiktoken

## วิธีใช้งาน

1. ดูตัวอย่างการใช้งานได้ในโฟลเดอร์ `examples/`
2. รันสคริปต์ตัวอย่างด้วยคำสั่ง:
   ```
   docker exec -it my-openhands-app python /workspace/examples/langchain_example.py
   ```

3. ใช้คำสั่งในการติดตั้งแพ็คเกจเพิ่มเติม:
   ```
   docker exec -it my-openhands-app pip install <ชื่อแพ็คเกจ>
   ```

## หมายเหตุสำคัญ

- ต้องมี API key สำหรับบริการต่างๆ (เช่น OpenAI) ในการใช้งานบางฟีเจอร์
- ควรเก็บ API key ไว้ใน environment variables ไม่ควรฝังไว้ในโค้ด
- หากต้องการใช้โมเดลขนาดใหญ่ (เช่น GPT-4) ควรตรวจสอบทรัพยากรของเครื่องก่อน
"""

    with open("README_AI_TOOLS.md", "w", encoding="utf-8") as f:
        f.write(readme_content.strip())

    print_success("สร้างไฟล์ README.md สำเร็จ")
    return True


def install_vector_db():
    """ติดตั้ง Vector Database สำหรับ Memory & Learning"""
    print_step("ติดตั้ง Vector Database (ChromaDB, Weaviate)")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install chromadb weaviate-client"
        )
        if result:
            print_success("ติดตั้ง Vector Database สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง Vector Database ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง Vector Database: {e}")
        return False


def install_mongodb():
    """ติดตั้ง MongoDB สำหรับเก็บ Logs และข้อมูล"""
    print_step("ติดตั้ง MongoDB Client")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install pymongo"
        )
        if result:
            print_success("ติดตั้ง MongoDB Client สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง MongoDB Client ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง MongoDB Client: {e}")
        return False


def install_web_automation():
    """ติดตั้ง Web Automation Tools (Playwright, Undetected ChromeDriver)"""
    print_step("ติดตั้ง Web Automation Tools")
    try:
        # ติดตั้ง Playwright
        run_command(
            "docker exec -it my-openhands-app pip install playwright"
        )
        
        # ติดตั้ง Browsers สำหรับ Playwright
        run_command(
            "docker exec -it my-openhands-app playwright install"
        )
        
        # ติดตั้ง Undetected ChromeDriver
        run_command(
            "docker exec -it my-openhands-app pip install undetected-chromedriver"
        )
        
        print_success("ติดตั้ง Web Automation Tools สำเร็จ")
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง Web Automation Tools: {e}")
        return False


def install_fastapi():
    """ติดตั้ง FastAPI และ WebSocket สำหรับ Monitoring"""
    print_step("ติดตั้ง FastAPI และ WebSocket")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install fastapi uvicorn websockets"
        )
        if result:
            print_success("ติดตั้ง FastAPI และ WebSocket สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง FastAPI และ WebSocket ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง FastAPI และ WebSocket: {e}")
        return False


def install_langgraph():
    """ติดตั้ง LangGraph สำหรับสร้าง AI Workflows"""
    print_step("ติดตั้ง LangGraph")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install langgraph"
        )
        if result:
            print_success("ติดตั้ง LangGraph สำเร็จ")
            return True
        else:
            print_error("ติดตั้ง LangGraph ไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้ง LangGraph: {e}")
        return False


def install_webhook_tools():
    """ติดตั้งเครื่องมือสำหรับ Webhook และการแจ้งเตือน"""
    print_step("ติดตั้งเครื่องมือสำหรับ Webhook และการแจ้งเตือน")
    try:
        result = run_command(
            "docker exec -it my-openhands-app pip install requests python-telegram-bot discord.py"
        )
        if result:
            print_success("ติดตั้งเครื่องมือสำหรับ Webhook และการแจ้งเตือนสำเร็จ")
            return True
        else:
            print_error("ติดตั้งเครื่องมือสำหรับ Webhook และการแจ้งเตือนไม่สำเร็จ")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้งเครื่องมือสำหรับ Webhook และการแจ้งเตือน: {e}")
        return False


def install_react_tools():
    """ติดตั้งเครื่องมือสำหรับพัฒนา React Frontend"""
    print_step("ติดตั้งเครื่องมือสำหรับพัฒนา React Frontend")
    try:
        # ติดตั้ง Node.js packages
        run_command(
            "docker exec -it my-openhands-app npm install -g create-react-app"
        )
        
        print_success("ติดตั้งเครื่องมือสำหรับพัฒนา React Frontend สำเร็จ")
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะติดตั้งเครื่องมือสำหรับพัฒนา React Frontend: {e}")
        return False


def create_advanced_examples():
    """สร้างไฟล์ตัวอย่างการใช้งานเครื่องมือขั้นสูง"""
    print_step("สร้างไฟล์ตัวอย่างการใช้งานเครื่องมือขั้นสูง")
    
    # สร้างโฟลเดอร์ examples/advanced หากยังไม่มี
    os.makedirs("examples/advanced", exist_ok=True)
    
    # ตัวอย่างการใช้งาน ChromaDB
    chromadb_example = """# ChromaDB Example - Vector Database
import chromadb

# สร้าง client
client = chromadb.Client()

# สร้าง collection
collection = client.create_collection(name="merchant_success_patterns")

# เพิ่มข้อมูล
collection.add(
    documents=["Merchant A - Visa - Success", "Merchant B - Mastercard - Failed"],
    metadatas=[
        {"merchant": "Merchant A", "card_type": "Visa", "result": "Success"},
        {"merchant": "Merchant B", "card_type": "Mastercard", "result": "Failed"}
    ],
    ids=["doc1", "doc2"]
)

# ค้นหาข้อมูล
results = collection.query(
    query_texts=["Merchant A Success"],
    n_results=1
)

print("Results:", results)
"""
    
    # ตัวอย่างการใช้งาน MongoDB
    mongodb_example = """# MongoDB Example - Logging & History
import pymongo
from datetime import datetime

# เชื่อมต่อกับ MongoDB (ถ้ารันใน Docker ให้ใช้ host.docker.internal แทน localhost)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ai_agent_db"]
collection = db["transaction_logs"]

# บันทึกข้อมูล
log_entry = {
    "timestamp": datetime.now(),
    "action": "card_payment",
    "merchant": "Example Shop",
    "card_bin": "123456",
    "proxy_used": "us-east-1",
    "result": "success",
    "processing_time": 3.5,
    "details": {
        "response_code": 200,
        "auth_code": "A12345",
    }
}

# Insert log
result = collection.insert_one(log_entry)
print(f"Log inserted with ID: {result.inserted_id}")

# ค้นหาข้อมูล
success_logs = collection.find({"result": "success"})
print("Successful transactions:")
for log in success_logs:
    print(f"{log['timestamp']} - {log['merchant']} - {log['card_bin']}")
"""
    
    # ตัวอย่างการใช้งาน Playwright
    playwright_example = """# Playwright Example - Web Automation with Stealth
from playwright.sync_api import sync_playwright
import time
import random

def random_delay(min_seconds=1, max_seconds=3):
    """สร้างการหน่วงเวลาแบบสุ่มเพื่อเลียนแบบมนุษย์"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def human_like_typing(element, text, min_delay=0.05, max_delay=0.2):
    """พิมพ์ข้อความแบบเลียนแบบมนุษย์ด้วยความเร็วที่ไม่สม่ำเสมอ"""
    for char in text:
        element.type(char)
        time.sleep(random.uniform(min_delay, max_delay))

with sync_playwright() as p:
    # เปิด browser แบบ stealth
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    
    # เพิ่ม cookies และตั้งค่าอื่นๆ เพื่อความเหมือนมนุษย์
    context.add_cookies([{
        "name": "session_id", 
        "value": "test123", 
        "domain": "example.com",
        "path": "/",
    }])
    
    page = context.new_page()
    
    # เปิดเว็บไซต์
    page.goto("https://example.com/login")
    random_delay(2, 4)  # รอสักครู่
    
    # กรอกฟอร์มแบบคล้ายมนุษย์
    username_field = page.locator("#username")
    human_like_typing(username_field, "testuser@example.com")
    
    random_delay(1, 2)  # หน่วงเวลาระหว่างช่อง
    
    password_field = page.locator("#password")
    human_like_typing(password_field, "Password123!")
    
    random_delay(1.5, 3)  # หน่วงเวลาก่อนกดปุ่ม
    
    # ทำการคลิกปุ่ม
    page.locator("#login-button").click()
    
    # รอให้หน้าถัดไปโหลด
    page.wait_for_url("**/dashboard")
    
    print("Login successful!")
    
    # ทำการจับภาพหน้าจอ
    page.screenshot(path="dashboard.png")
    
    # ปิด browser
    browser.close()
"""
    
    # ตัวอย่างการใช้งาน LangGraph
    langgraph_example = """# LangGraph Example - AI Workflow with Retry Logic
from typing import Dict, List, Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
import os

# Set your API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Define state
class AgentState(TypedDict):
    messages: List[Annotated[HumanMessage | SystemMessage | AIMessage, "Messages"]]
    attempts: int
    status: Literal["running", "success", "failed"]
    card_bins: List[str]
    current_bin: str

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Node functions
def analyze_gateway(state: AgentState) -> AgentState:
    """Analyze payment gateway and requirements"""
    messages = state["messages"]
    messages.append(SystemMessage(content="You are analyzing a payment gateway to determine requirements."))
    
    # Process input and generate analysis
    ai_message = llm.invoke(messages)
    messages.append(ai_message)
    
    return {"messages": messages}

def select_card(state: AgentState) -> AgentState:
    """Select appropriate card BIN based on requirements"""
    messages = state["messages"]
    
    # If we have retried, use a different card
    if state["attempts"] > 0:
        messages.append(SystemMessage(content=f"Previous attempt failed. Try a different card. Avoided BINs: {state['current_bin']}"))
    
    # Add instruction to select a card
    messages.append(SystemMessage(content="Select an appropriate card BIN based on the gateway requirements."))
    
    # Get AI response
    ai_message = llm.invoke(messages)
    messages.append(ai_message)
    
    # Extract BIN from response (in real code, you'd use a better extraction method)
    suggested_bin = "123456"  # This would be extracted from the AI message
    
    return {
        "messages": messages,
        "current_bin": suggested_bin
    }

def process_payment(state: AgentState) -> AgentState:
    """Simulate payment processing with the selected card"""
    messages = state["messages"]
    current_bin = state["current_bin"]
    
    # Simulate success/failure (in real code, this would use the browser automation)
    # For demonstration, let's say odd-numbered attempts fail
    success = state["attempts"] % 2 == 0
    
    if success:
        messages.append(SystemMessage(content=f"Payment with BIN {current_bin} was successful!"))
        return {
            "messages": messages,
            "status": "success"
        }
    else:
        messages.append(SystemMessage(content=f"Payment with BIN {current_bin} failed."))
        return {
            "messages": messages,
            "status": "failed",
            "attempts": state["attempts"] + 1
        }

# Router function
def should_retry(state: AgentState) -> str:
    """Determine whether to retry or end"""
    if state["status"] == "success":
        return "end"
    elif state["attempts"] >= 3:
        return "end"  # Max attempts reached
    else:
        return "retry"

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_gateway", analyze_gateway)
workflow.add_node("select_card", select_card)
workflow.add_node("process_payment", process_payment)

# Connect nodes
workflow.add_edge("analyze_gateway", "select_card")
workflow.add_edge("select_card", "process_payment")

# Add conditional edges
workflow.add_conditional_edges(
    "process_payment",
    should_retry,
    {
        "end": END,
        "retry": "select_card"
    }
)

# Set entry point
workflow.set_entry_point("analyze_gateway")

# Compile
app = workflow.compile()

# Run the graph
result = app.invoke({
    "messages": [HumanMessage(content="Process payment for Merchant X using Stripe gateway.")],
    "attempts": 0,
    "status": "running",
    "card_bins": ["123456", "234567", "345678", "456789"],
    "current_bin": ""
})

# Print final state
print("Final state:", result)
"""
    
    # ตัวอย่างการใช้งาน FastAPI + WebSocket
    fastapi_example = """# FastAPI + WebSocket Example - Real-time Monitoring
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import asyncio
import json
from datetime import datetime

app = FastAPI()

# HTML for the monitoring dashboard
html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>AI Agent Monitor</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            #agents {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
            .agent-card {
                background: white;
                border-radius: 8px;
                padding: 15px;
                width: 300px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .agent-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            .agent-id {
                font-weight: bold;
                color: #333;
            }
            .status-running {
                color: #2196F3;
                font-weight: bold;
            }
            .status-success {
                color: #4CAF50;
                font-weight: bold;
            }
            .status-failed {
                color: #F44336;
                font-weight: bold;
            }
            .log-container {
                height: 200px;
                overflow-y: auto;
                background: #f9f9f9;
                border-radius: 4px;
                padding: 10px;
                font-family: monospace;
                font-size: 12px;
            }
            .log-item {
                margin-bottom: 5px;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }
            .timestamp {
                color: #666;
                font-size: 11px;
            }
        </style>
    </head>
    <body>
        <h1>AI Agent Monitoring Dashboard</h1>
        <div id="agents"></div>
        <script>
            const agentsContainer = document.getElementById('agents');
            const agents = {};
            
            // Create WebSocket connection
            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateAgentCard(data);
            };
            
            function updateAgentCard(data) {
                const agentId = data.agent_id;
                
                // Create agent card if it doesn't exist
                if (!agents[agentId]) {
                    const card = document.createElement('div');
                    card.className = 'agent-card';
                    card.innerHTML = `
                        <div class="agent-header">
                            <div class="agent-id">${agentId}</div>
                            <div class="agent-status status-${data.status}">${data.status}</div>
                        </div>
                        <div>Task: <span class="task-name">${data.task || 'N/A'}</span></div>
                        <div>Progress: <span class="progress">${data.progress || '0%'}</span></div>
                        <h4>Logs:</h4>
                        <div class="log-container" id="logs-${agentId}"></div>
                    `;
                    agentsContainer.appendChild(card);
                    agents[agentId] = {
                        card: card,
                        logs: document.getElementById(`logs-${agentId}`)
                    };
                }
                
                // Update status
                const statusEl = agents[agentId].card.querySelector('.agent-status');
                statusEl.className = `agent-status status-${data.status}`;
                statusEl.textContent = data.status;
                
                // Update task
                if (data.task) {
                    agents[agentId].card.querySelector('.task-name').textContent = data.task;
                }
                
                // Update progress
                if (data.progress) {
                    agents[agentId].card.querySelector('.progress').textContent = data.progress;
                }
                
                // Add log
                if (data.log) {
                    const logItem = document.createElement('div');
                    logItem.className = 'log-item';
                    logItem.innerHTML = `
                        <span class="timestamp">${new Date().toLocaleTimeString()}</span>: ${data.log}
                    `;
                    agents[agentId].logs.appendChild(logItem);
                    agents[agentId].logs.scrollTop = agents[agentId].logs.scrollHeight;
                }
            }
        </script>
    </body>
</html>
'''

# Connection manager
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

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Simulate some initial data
        await websocket.send_text(json.dumps({
            "agent_id": "agent-001",
            "status": "running",
            "task": "Processing Merchant X",
            "progress": "25%",
            "log": "Started processing payment"
        }))
        
        # Simulate agent updates
        for i in range(5):
            await asyncio.sleep(3)
            status = "running"
            progress = f"{(i+2)*20}%"
            log = f"Step {i+1} completed"
            
            if i == 4:  # Last iteration
                status = "success"
                log = "Payment processed successfully"
            
            await websocket.send_text(json.dumps({
                "agent_id": "agent-001",
                "status": status,
                "task": "Processing Merchant X",
                "progress": progress,
                "log": log
            }))
        
        # Keep connection alive
        while True:
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    
    # เขียนไฟล์ตัวอย่าง
    with open("examples/advanced/chromadb_example.py", "w", encoding="utf-8") as f:
        f.write(chromadb_example.strip())
    
    with open("examples/advanced/mongodb_example.py", "w", encoding="utf-8") as f:
        f.write(mongodb_example.strip())
    
    with open("examples/advanced/playwright_example.py", "w", encoding="utf-8") as f:
        f.write(playwright_example.strip())
    
    with open("examples/advanced/langgraph_example.py", "w", encoding="utf-8") as f:
        f.write(langgraph_example.strip())
    
    with open("examples/advanced/fastapi_websocket_example.py", "w", encoding="utf-8") as f:
        f.write(fastapi_example.strip())
    
    print_success("สร้างไฟล์ตัวอย่างขั้นสูงสำเร็จ ตรวจสอบได้ที่โฟลเดอร์ examples/advanced/")
    return True

def update_main_function():
    """อัปเดตฟังก์ชัน main ให้เรียกใช้ฟังก์ชันใหม่"""
    # อัปเดตส่วนของฟังก์ชัน main ในไฟล์นี้
    # เนื่องจากเราไม่สามารถแก้ไขโค้ดโดยตรง จึงต้องเพิ่มการเรียกฟังก์ชันใหม่ในส่วนนี้
    return True

def main():
    """ฟังก์ชันหลักสำหรับติดตั้งเครื่องมือ AI"""
    print_header("เครื่องมือติดตั้ง AI ขั้นสูงสำหรับ OpenHands")
    
    # ตรวจสอบ Docker และ OpenHands
    if not check_docker() or not check_openhands():
        print_error("ไม่สามารถดำเนินการต่อได้ กรุณาตรวจสอบการทำงานของ Docker และ OpenHands")
        return
    
    print_header("เริ่มการติดตั้งเครื่องมือ AI")
    
    # ติดตั้งเครื่องมือพื้นฐาน
    install_langchain()
    install_huggingface()
    install_llama_index()
    install_autogen()
    install_llamafile()
    install_gpt4all()
    install_deep_learning_tools()
    install_openai_tools()
    install_nodejs_ai_tools()
    
    # ติดตั้งเครื่องมือขั้นสูง
    install_vector_db()
    install_mongodb()
    install_web_automation()
    install_fastapi()
    install_langgraph()
    install_webhook_tools()
    install_react_tools()
    
    # สร้างไฟล์ตัวอย่างและเอกสาร
    create_examples()
    create_advanced_examples()
    create_setup_script()
    create_readme()
    
    print_header("การติดตั้งเครื่องมือ AI สำเร็จ")
    print(f"{Colors.GREEN}{Colors.BOLD}คุณสามารถเริ่มใช้งานเครื่องมือ AI ได้แล้ว!{Colors.ENDC}")
    print(
        f"{Colors.CYAN}ดูวิธีการใช้งานและตัวอย่างได้ในไฟล์ README_AI_TOOLS.md และโฟลเดอร์ examples/{Colors.ENDC}"
    )


if __name__ == "__main__":
    main()
