# MythoMax-L2-13B Ollama for Railway

Deploy God-Tier AI Model "thebloke/mythomax-l2-13b" ด้วย Railway

## Deploy

1. Push repo นี้ขึ้น GitHub
2. Deploy บน Railway (เลือก Pro 32GB RAM)
3. ยิง API ครั้งแรก Model จะถูกโหลดเอง

## API Example

import requests
url = "https://<your-app-name>.up.railway.app/api/generate"
payload = {
    "model": "mythomax-l2-13b",
    "prompt": "Give me a God-Tier Agentic AI example.",
    "stream": False
}
resp = requests.post(url, json=payload)
print(resp.json())
