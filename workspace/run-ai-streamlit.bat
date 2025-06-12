@echo off
echo ===== กำลังเริ่มต้น AI Web App ด้วย Streamlit =====
echo.

REM ตรวจสอบว่า Docker กำลังทำงานหรือไม่
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo [ข้อผิดพลาด] Docker ไม่ได้ทำงานอยู่ กรุณาเปิด Docker Desktop ก่อน
    pause
    exit /b 1
)

REM ตรวจสอบว่า OpenHands container กำลังทำงานหรือไม่
docker ps --format "{{.Names}}" | findstr "my-openhands-app" > nul
if %errorlevel% neq 0 (
    echo [ข้อผิดพลาด] OpenHands container ไม่ได้ทำงานอยู่ กรุณาเริ่มต้น OpenHands ก่อน
    pause
    exit /b 1
)

echo [กำลังเริ่มต้น] Streamlit AI Web App...
echo.
echo เมื่อเริ่มต้นสำเร็จ คุณสามารถเข้าถึง app ได้ที่: http://localhost:8501
echo กดปุ่ม Ctrl+C เพื่อหยุดการทำงาน
echo.

REM รัน Streamlit app
docker exec -it my-openhands-app bash -c "cd /workspace && streamlit run streamlit_apps/ai_demo_app.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ===== Streamlit app หยุดทำงานแล้ว =====
pause 