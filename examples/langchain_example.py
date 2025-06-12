# LangChain Example
# ตั้งค่า API key (ควรใช้ environment variable จริงๆ)
import os

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

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
