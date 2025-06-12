# OpenHands by Windows

โปรเจคนี้เป็นการติดตั้ง OpenHands AI Assistant บน Windows โดยใช้ Docker

## คุณสมบัติ

- ใช้งาน OpenHands AI Assistant บนระบบ Windows
- รองรับหลาย LLM Providers (Gemini, OpenAI, OpenRouter, Mistral, Anthropic)
- มีการเชื่อมต่อกับ Redis และ PostgreSQL สำหรับเก็บข้อมูลและการแคช
- Custom Sandbox ที่มีเครื่องมือพัฒนาซอฟต์แวร์ครบครัน
- รองรับการทำงานกับหลายภาษาโปรแกรมมิ่ง (Node.js, Python, Go, Rust, Java, .NET, PHP)
- มีเครื่องมือสำหรับ Cloud Providers (AWS, GCP, Azure, Heroku)

## ความต้องการระบบ

- Windows 10/11
- Docker Desktop for Windows
- WSL2 (Windows Subsystem for Linux)
- พื้นที่ว่าง: อย่างน้อย 10GB

## การติดตั้ง

1. ติดตั้ง [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. เปิด Docker Desktop และตรวจสอบให้แน่ใจว่า WSL2 integration เปิดใช้งานอยู่
3. คัดลอกโปรเจคนี้ลงในเครื่อง
4. เปิด PowerShell หรือ Command Prompt และไปยังโฟลเดอร์โปรเจค
5. รันคำสั่งต่อไปนี้:

```bash
docker-compose up -d
```

หมายเหตุ: ในครั้งแรกอาจใช้เวลาหลายนาทีในการดาวน์โหลดและสร้าง images

## การเข้าถึง

เมื่อติดตั้งเสร็จสิ้น คุณสามารถเข้าถึง OpenHands ได้ที่:

- OpenHands UI: http://localhost:3001

## LLM Providers

โปรเจคนี้รองรับ LLM Providers หลายตัว:

### Gemini (เปิดใช้งานโดยค่าเริ่มต้น)
```yaml
- LLM_PROVIDER=google
- GOOGLE_API_KEY=AIzaSyApjpQaZCJIjuBwWm7IeIVDRXle6u46t4I
- LLM_MODEL=gemini-1.5-flash-latest
```

### OpenAI/Ollama
```yaml
- LLM_PROVIDER=openai
- OPENAI_API_BASE=http://host.docker.internal:11434/v1
- OPENAI_API_KEY=ollama
- LLM_MODEL=hf.co/TheBloke/Nous-Hermes-2-Yi-34B-GGUF:Q4_K_M
```

### OpenRouter
```yaml
- LLM_PROVIDER=openrouter
- OPENROUTER_API_KEY=your_openrouter_api_key
- LLM_MODEL=openrouter/auto
```

### Mistral
```yaml
- LLM_PROVIDER=mistral
- MISTRAL_API_KEY=your_mistral_api_key
- LLM_MODEL=mistral-large-latest
```

### Anthropic
```yaml
- LLM_PROVIDER=anthropic
- ANTHROPIC_API_KEY=your_anthropic_api_key
- LLM_MODEL=claude-3-opus-20240229
```

## การปรับแต่ง

คุณสามารถปรับแต่ง OpenHands ได้โดยการแก้ไขไฟล์ `docker-compose.yml`:

1. เปลี่ยน LLM Provider โดยการแก้ไขส่วน environment
2. ปรับแต่งค่า RAM และ CPU สำหรับ sandbox
3. เพิ่มหรือลบ services ตามความต้องการ

## Custom Sandbox

Custom Sandbox มีเครื่องมือพัฒนาซอฟต์แวร์หลากหลายติดตั้งไว้แล้ว:

- Languages: Node.js, Python, Go, Rust, Java, .NET, PHP
- Build tools: npm, yarn, pnpm, pip, maven, gradle, composer
- Frameworks: Angular, Vue, React, Next.js, Gatsby
- Cloud tools: AWS CLI, Google Cloud SDK, Azure CLI, Heroku CLI
- Development tools: Git, Docker CLI, และอื่นๆ อีกมากมาย

## การจัดการข้อมูล

OpenHands จะเก็บข้อมูลไว้ใน Docker volumes:

- `openhands_state`: เก็บข้อมูลสถานะของ OpenHands
- `redis_data`: เก็บข้อมูลแคชใน Redis
- `postgres_data`: เก็บข้อมูลใน PostgreSQL

## การแก้ไขปัญหา

หากคุณพบปัญหา ลองตรวจสอบสิ่งต่อไปนี้:

1. ตรวจสอบ Docker logs:
```bash
docker-compose logs
```

2. รีสตาร์ท containers:
```bash
docker-compose restart
```

3. ถ้ามีปัญหาอื่นๆ ลอง rebuild containers:
```bash
docker-compose down
docker-compose up -d --build
```

## โครงสร้างโปรเจค

```
openhandsbywin/
├── .vscode/                    # VSCode configuration
├── custom-sandbox/             # Custom sandbox configuration
│   └── Dockerfile              # Dockerfile สำหรับ custom sandbox
├── workspace/                  # พื้นที่ทำงานของ OpenHands
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # คุณกำลังอ่านไฟล์นี้
```

## License

รูปแบบการใช้งานเป็นไปตาม License ของ OpenHands 