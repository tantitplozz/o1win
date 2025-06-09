# ✅ Railway + Ollama + MythoMax-13B

Deploy uncensored AI model (thebloke/mythomax-l2-13b) via Railway.

---

## 🌐 API Endpoint

POST <https://o1win-o1win.up.railway.app/api/generate>

---

## 📥 Example Payload

```json
{
  "model": "mythomax-l2-13b",
  "prompt": "Explain God-Tier Agentic AI.",
  "stream": false
}
```

🧪 Python Test

```python
import requests

url = "https://o1win-o1win.up.railway.app/api/generate"
payload = {
    "model": "mythomax-l2-13b",
    "prompt": "Explain God-Tier Agentic AI.",
    "stream": False
}
resp = requests.post(url, json=payload)
print(resp.json())
```

⚠️ Notes
No need to RUN ollama pull in Dockerfile.

First request may take time (model lazy-load).

Once cached, responses are fast.

---

## 🧠 ขั้นตอน Push ให้เสร็จ

```bash
git clone https://github.com/tantitplozz/o1win.git
cd o1win

# สร้าง Dockerfile
echo 'FROM ollama/ollama:latest
CMD ["serve"]' > Dockerfile

# สร้าง README.md
# <วางเนื้อหา README.md ด้านบนลงไป หรือใช้ VSCode แปะได้เลย>

# Push
git add .
git commit -m "God-Tier Init: Ollama + MythoMax-13B"
git push origin main
```

🚀 พร้อมใช้งานแล้วที่:

```bash
https://o1win-o1win.up.railway.app/api/generate
```
