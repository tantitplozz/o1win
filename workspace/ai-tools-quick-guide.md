# คู่มืออ้างอิงฉบับย่อ - AI Tools for OpenHands

## การเริ่มต้นใช้งาน

### เปิด Streamlit Web App
เริ่มใช้งาน Web App ทันทีด้วยการดับเบิลคลิกที่:
```
run-ai-streamlit.bat
```

หรือรันคำสั่งใน PowerShell:
```
docker exec -it my-openhands-app bash -c "cd /workspace && streamlit run streamlit_apps/ai_demo_app.py --server.port 8501 --server.address 0.0.0.0"
```

### เปิด Jupyter Notebook
```
docker exec -it my-openhands-app bash -c "cd /workspace && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"
```
เข้าถึงที่: http://localhost:8888

## รายการไฟล์ตัวอย่าง

### ไฟล์ตัวอย่างพื้นฐาน
| ไฟล์ | คำอธิบาย | คำสั่งรัน |
|------|---------|----------|
| `examples/langchain_example.py` | ตัวอย่างการใช้ LangChain | `docker exec -it my-openhands-app python /workspace/examples/langchain_example.py` |
| `examples/huggingface_example.py` | ตัวอย่างการใช้ Hugging Face | `docker exec -it my-openhands-app python /workspace/examples/huggingface_example.py` |
| `examples/llamaindex_example.py` | ตัวอย่างการใช้ LlamaIndex | `docker exec -it my-openhands-app python /workspace/examples/llamaindex_example.py` |
| `examples/autogen_example.py` | ตัวอย่างการใช้ AutoGen | `docker exec -it my-openhands-app python /workspace/examples/autogen_example.py` |

### ไฟล์ตัวอย่างขั้นสูง
| ไฟล์ | คำอธิบาย | คำสั่งรัน |
|------|---------|----------|
| `examples/advanced/chromadb_example.py` | Vector DB สำหรับเก็บความสำเร็จ | `docker exec -it my-openhands-app python /workspace/examples/advanced/chromadb_example.py` |
| `examples/advanced/mongodb_example.py` | Logging & Transaction History | `docker exec -it my-openhands-app python /workspace/examples/advanced/mongodb_example.py` |
| `examples/advanced/playwright_example.py` | Web Automation แบบ Stealth | `docker exec -it my-openhands-app python /workspace/examples/advanced/playwright_example.py` |
| `examples/advanced/langgraph_example.py` | AI Workflow ที่มีระบบ Retry | `docker exec -it my-openhands-app python /workspace/examples/advanced/langgraph_example.py` |
| `examples/advanced/fastapi_websocket_example.py` | Real-time Monitoring Dashboard | `docker exec -it my-openhands-app python /workspace/examples/advanced/fastapi_websocket_example.py` |

## คำสั่งติดตั้งเพิ่มเติม

### ติดตั้งเครื่องมือ AI ทั้งหมด
```
python workspace/ai-tools-installer.py
```

### ติดตั้งแพ็คเกจเฉพาะ
```
docker exec -it my-openhands-app pip install [ชื่อแพ็คเกจ]
```

## เอกสารอ้างอิง

### เอกสารฉบับเต็ม
- `README_AI_TOOLS.md` - คำอธิบายทั่วไป
- `workspace/ai-tools-readme.md` - คู่มือการใช้งานฉบับละเอียด

### โค้ดตัวอย่างทั้งหมด
```
docker exec -it my-openhands-app ls -la /workspace/examples/
docker exec -it my-openhands-app ls -la /workspace/examples/advanced/
```

### ไฟล์ที่เกี่ยวข้อง
- `run-ai-streamlit.bat` - เริ่ม Streamlit App
- `setup.py` - ติดตั้งแพ็คเกจที่จำเป็น
- `workspace/ai-tools-installer.py` - ติดตั้งเครื่องมือเพิ่มเติม 