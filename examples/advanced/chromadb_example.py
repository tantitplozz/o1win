# ChromaDB Example - Vector Database
import chromadb

# สร้าง client
client = chromadb.Client()

# สร้าง collection
collection = client.create_collection(name="merchant_success_patterns")

# เพิ่มข้อมูล
collection.add(
    documents=[
        "Merchant A - Visa - Success",
        "Merchant B - Mastercard - Failed",
        "Merchant A - Mastercard - Success",
        "Merchant C - Visa - Failed",
        "Merchant C - Amex - Success",
    ],
    metadatas=[
        {"merchant": "Merchant A", "card_type": "Visa", "result": "Success"},
        {"merchant": "Merchant B", "card_type": "Mastercard", "result": "Failed"},
        {"merchant": "Merchant A", "card_type": "Mastercard", "result": "Success"},
        {"merchant": "Merchant C", "card_type": "Visa", "result": "Failed"},
        {"merchant": "Merchant C", "card_type": "Amex", "result": "Success"},
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
)

# ค้นหาข้อมูลด้วย semantic search
results = collection.query(query_texts=["Merchant A Success"], n_results=2)

print("Semantic Search Results:", results)

# ค้นหาด้วย metadata - แก้ไขตาม API ล่าสุด
results = collection.get(
    where={
        "$and": [{"merchant": {"$eq": "Merchant C"}}, {"result": {"$eq": "Success"}}]
    }
)

print("\nMetadata Search Results:", results)


# นำข้อมูลไปใช้งานจริง
def recommend_card_for_merchant(merchant_name):
    """แนะนำบัตรที่เหมาะสมสำหรับร้านค้านี้จากประสบการณ์ที่ผ่านมา"""
    # ค้นหาข้อมูลความสำเร็จในร้านค้านี้
    merchant_results = collection.get(
        where={
            "$and": [
                {"merchant": {"$eq": merchant_name}},
                {"result": {"$eq": "Success"}},
            ]
        }
    )

    if not merchant_results["ids"]:
        return f"ไม่มีข้อมูลการใช้บัตรที่สำเร็จกับร้านค้า {merchant_name}"

    # ถ้ามีข้อมูล ให้แนะนำบัตรที่เคยใช้สำเร็จ
    card_types = [meta["card_type"] for meta in merchant_results["metadatas"]]
    return f"แนะนำให้ใช้บัตรประเภท {', '.join(card_types)} กับร้านค้า {merchant_name}"


# ทดสอบการแนะนำบัตร
print("\nCard Recommendation:")
print(recommend_card_for_merchant("Merchant A"))
print(recommend_card_for_merchant("Merchant C"))
print(recommend_card_for_merchant("Merchant D"))  # ไม่มีข้อมูล
