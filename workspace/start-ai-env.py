#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Environment Starter - เครื่องมือเริ่มสภาพแวดล้อมสำหรับ AI
สำหรับใช้งานกับ OpenHands AI Assistant
"""

import argparse
import json
import os
import platform
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


def setup_jupyter_notebook():
    """ติดตั้งและเตรียม Jupyter Notebook สำหรับการทำงานกับ AI"""
    print_step("เตรียม Jupyter Notebook สำหรับการทำงานกับ AI")
    try:
        # ติดตั้ง Jupyter ถ้ายังไม่มี
        run_command(
            "docker exec -it my-openhands-app pip install jupyter notebook ipywidgets matplotlib"
        )

        # สร้างโฟลเดอร์สำหรับ notebooks
        run_command("docker exec -it my-openhands-app mkdir -p /workspace/notebooks")

        # สร้าง notebook ตัวอย่างสำหรับ AI
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# ยินดีต้อนรับสู่ AI Notebook\n",
                        "Notebook นี้ถูกสร้างขึ้นสำหรับการทำงานกับเครื่องมือ AI ขั้นสูง",
                    ],
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## ทดสอบการใช้งาน LangChain\n",
                        "ตัวอย่างการใช้งาน LangChain กับ OpenAI API",
                    ],
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# ตัวอย่างการใช้งาน LangChain\n",
                        "# ตั้งค่า API key ก่อนใช้งาน\n",
                        "import os\n",
                        '# os.environ["OPENAI_API_KEY"] = "your-api-key-here"\n',
                        "\n",
                        "from langchain.llms import OpenAI\n",
                        "from langchain.prompts import PromptTemplate\n",
                        "\n",
                        "# สร้าง prompt template\n",
                        "prompt = PromptTemplate(\n",
                        '    input_variables=["product"],\n',
                        '    template="คุณคิดว่าควรตั้งชื่ออะไรให้กับ {product}? ให้ 5 ชื่อพร้อมเหตุผล",\n',
                        ")\n",
                        "\n",
                        "# ตัวอย่างการใช้งาน (ต้องตั้งค่า API key ก่อน)\n",
                        "# llm = OpenAI(temperature=0.7)\n",
                        '# print(llm(prompt.format(product="แอปพลิเคชันสอนทำอาหารไทย")))',
                    ],
                    "outputs": [],
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## ทดสอบการใช้งาน Hugging Face\n",
                        "ตัวอย่างการใช้งาน Hugging Face Transformers",
                    ],
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": [
                        "# ตัวอย่างการใช้งาน Hugging Face\n",
                        "from transformers import pipeline\n",
                        "\n",
                        "# สร้าง pipeline สำหรับวิเคราะห์ความรู้สึก\n",
                        'sentiment_analyzer = pipeline("sentiment-analysis")\n',
                        "\n",
                        "# ทดสอบวิเคราะห์ความรู้สึกของข้อความ\n",
                        'texts = ["I love this product!", "This was a terrible experience."]\n',
                        "for text in texts:\n",
                        "    result = sentiment_analyzer(text)\n",
                        '    print(f"Text: {text}")\n',
                        "    print(f\"Sentiment: {result[0]['label']}, Score: {result[0]['score']:.4f}\")",
                    ],
                    "outputs": [],
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.10",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

        # เขียน notebook ไปยังไฟล์ในโฟลเดอร์ workspace/notebooks
        notebook_path = os.path.join("notebooks", "ai_tools_demo.ipynb")
        with open(notebook_path, "w", encoding="utf-8") as f:
            json.dump(notebook_content, f, ensure_ascii=False, indent=2)

        print_success("เตรียม Jupyter Notebook สำเร็จ")
        print_success(f"สร้าง notebook ตัวอย่างที่ {notebook_path}")
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะเตรียม Jupyter Notebook: {e}")
        return False


def start_jupyter_notebook():
    """เริ่มต้น Jupyter Notebook ใน container"""
    print_step("เริ่มต้น Jupyter Notebook")
    try:
        # รันคำสั่งเริ่ม Jupyter Notebook ใน background ของ container
        run_command(
            "docker exec -d my-openhands-app bash -c 'cd /workspace && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root'"
        )

        # รอให้ Jupyter Notebook เริ่มต้นสำเร็จ
        print_warning("รอให้ Jupyter Notebook เริ่มต้น...")
        time.sleep(5)

        # ดึง URL และ token ของ Jupyter Notebook
        notebook_info = run_command(
            "docker exec -it my-openhands-app bash -c 'jupyter notebook list'"
        )

        if notebook_info and "http://" in notebook_info:
            # แสดง URL ที่สามารถเข้าถึง Jupyter Notebook ได้
            notebook_url = notebook_info.split("http://")[1].split()[0]
            print_success(f"Jupyter Notebook เริ่มต้นสำเร็จ")
            print(
                f"{Colors.CYAN}เข้าถึง Jupyter Notebook ได้ที่: {Colors.BOLD}http://localhost:8888{Colors.ENDC}"
            )

            # สกัด token จาก URL
            if "token=" in notebook_url:
                token = notebook_url.split("token=")[1]
                print(f"{Colors.CYAN}Token: {Colors.BOLD}{token}{Colors.ENDC}")

            return True
        else:
            print_error("ไม่สามารถเริ่มต้น Jupyter Notebook ได้")
            return False
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะเริ่มต้น Jupyter Notebook: {e}")
        return False


def setup_streamlit():
    """ติดตั้งและเตรียม Streamlit สำหรับการสร้าง AI Web App"""
    print_step("เตรียม Streamlit สำหรับการสร้าง AI Web App")
    try:
        # ติดตั้ง Streamlit
        run_command("docker exec -it my-openhands-app pip install streamlit")

        # สร้างโฟลเดอร์สำหรับ Streamlit apps
        run_command(
            "docker exec -it my-openhands-app mkdir -p /workspace/streamlit_apps"
        )

        # สร้าง Streamlit app ตัวอย่าง
        app_content = """
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Demo App", page_icon="🤖", layout="wide")

# หัวข้อหลัก
st.title("🤖 ตัวอย่าง AI Web App ด้วย Streamlit")
st.markdown("---")

# แสดงข้อความต้อนรับ
st.markdown('''
## ยินดีต้อนรับสู่ AI Web App

แอปพลิเคชันนี้เป็นตัวอย่างการใช้งาน Streamlit สำหรับสร้าง AI Web App
คุณสามารถปรับแต่งและพัฒนาต่อยอดได้ตามต้องการ
''')

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
        st.session_state.data = pd.DataFrame({
            'x': np.random.randn(data_size),
            'y': np.random.randn(data_size)
        })
        st.success("สร้างข้อมูลใหม่แล้ว!")

# สร้างข้อมูลเริ่มต้นถ้ายังไม่มี
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'x': np.random.randn(data_size),
        'y': np.random.randn(data_size)
    })

# แสดงข้อมูลตาม checkbox
if show_data:
    st.subheader("ข้อมูล")
    st.dataframe(st.session_state.data)

if show_chart:
    st.subheader("กราฟแสดงข้อมูล")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(st.session_state.data['x'], st.session_state.data['y'], alpha=0.7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
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
"""

        # เขียน app ไปยังไฟล์ในโฟลเดอร์ workspace/streamlit_apps
        app_path = os.path.join("streamlit_apps", "ai_demo_app.py")
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_content.strip())

        print_success("เตรียม Streamlit สำเร็จ")
        print_success(f"สร้าง Streamlit app ตัวอย่างที่ {app_path}")
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะเตรียม Streamlit: {e}")
        return False


def start_streamlit():
    """เริ่มต้น Streamlit app ใน container"""
    print_step("เริ่มต้น Streamlit")
    try:
        # รันคำสั่งเริ่ม Streamlit ใน background ของ container
        run_command(
            "docker exec -d my-openhands-app bash -c 'cd /workspace/streamlit_apps && streamlit run ai_demo_app.py --server.port 8501 --server.address 0.0.0.0'"
        )

        # รอให้ Streamlit เริ่มต้นสำเร็จ
        print_warning("รอให้ Streamlit เริ่มต้น...")
        time.sleep(5)

        print_success(f"Streamlit เริ่มต้นสำเร็จ")
        print(
            f"{Colors.CYAN}เข้าถึง Streamlit app ได้ที่: {Colors.BOLD}http://localhost:8501{Colors.ENDC}"
        )
        return True
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดขณะเริ่มต้น Streamlit: {e}")
        return False


def main():
    """ฟังก์ชันหลักสำหรับเริ่มสภาพแวดล้อม AI"""
    print_header("เครื่องมือเริ่มสภาพแวดล้อมสำหรับ AI")

    # สร้าง parser สำหรับรับ argument จาก command line
    parser = argparse.ArgumentParser(description="เริ่มสภาพแวดล้อมสำหรับ AI")
    parser.add_argument("--jupyter", action="store_true", help="เริ่มต้น Jupyter Notebook")
    parser.add_argument("--streamlit", action="store_true", help="เริ่มต้น Streamlit")
    parser.add_argument(
        "--all", action="store_true", help="เริ่มต้นทั้ง Jupyter Notebook และ Streamlit"
    )

    args = parser.parse_args()

    # ถ้าไม่มี argument ให้เริ่มทั้งหมด
    if not (args.jupyter or args.streamlit or args.all):
        args.all = True

    # ตรวจสอบ Docker และ OpenHands
    if not check_docker() or not check_openhands():
        print_error("ไม่สามารถดำเนินการต่อได้ กรุณาตรวจสอบการทำงานของ Docker และ OpenHands")
        return

    # สร้างโฟลเดอร์ที่จำเป็น
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("streamlit_apps", exist_ok=True)

    # เริ่ม Jupyter Notebook ถ้าต้องการ
    if args.jupyter or args.all:
        setup_jupyter_notebook()
        start_jupyter_notebook()

    # เริ่ม Streamlit ถ้าต้องการ
    if args.streamlit or args.all:
        setup_streamlit()
        start_streamlit()

    print_header("เริ่มสภาพแวดล้อม AI สำเร็จ")
    print(f"{Colors.GREEN}{Colors.BOLD}คุณสามารถเริ่มใช้งานเครื่องมือ AI ได้แล้ว!{Colors.ENDC}")

    if args.jupyter or args.all:
        print(
            f"{Colors.CYAN}Jupyter Notebook: {Colors.BOLD}http://localhost:8888{Colors.ENDC}"
        )
    if args.streamlit or args.all:
        print(
            f"{Colors.CYAN}Streamlit App: {Colors.BOLD}http://localhost:8501{Colors.ENDC}"
        )


if __name__ == "__main__":
    main()
