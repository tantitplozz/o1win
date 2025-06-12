# LlamaIndex Example
import os

from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI

# ตั้งค่า API key (ควรใช้ environment variable จริงๆ)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# สร้างโฟลเดอร์และไฟล์ตัวอย่าง
os.makedirs("data", exist_ok=True)
with open("data/thai_food.txt", "w", encoding="utf-8") as f:
    f.write(
        """
ต้มยำกุ้ง เป็นอาหารไทยที่มีชื่อเสียงระดับโลก มีรสชาติเปรี้ยว เผ็ด และหอมสมุนไพร โดยมีกุ้งเป็นส่วนประกอบหลัก
ผัดไทย เป็นอาหารไทยประเภทเส้นผัดที่ได้รับความนิยมมาก มีส่วนผสมหลักคือเส้นจันท์ ไข่ เต้าหู้ และถั่วงอก
ส้มตำ เป็นอาหารประจำภาคอีสานของประเทศไทย มีรสชาติเปรี้ยว เผ็ด เค็ม หวาน ทำจากมะละกอสับ กระเทียม พริกขี้หนู
"""
    )

# โหลดเอกสารจากโฟลเดอร์
documents = SimpleDirectoryReader("data").load_data()

# ตั้งค่า LLM
service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0)
)

# สร้างดัชนีสำหรับค้นหา
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# สร้าง query engine
query_engine = index.as_query_engine()

# ทดลองถามคำถาม
response = query_engine.query("บอกฉันเกี่ยวกับอาหารไทยที่มีรสเผ็ด")
print(response)
