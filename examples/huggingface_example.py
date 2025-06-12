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
texts = [
    "I love this product!",
    "This was a terrible experience.",
    "It was okay, nothing special.",
]
for text in texts:
    result = sentiment_analyzer(text)
    print(f"Text: {text}")
    print(f"Sentiment: {result[0]['label']}, Score: {result[0]['score']:.4f}")
