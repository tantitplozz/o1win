"""
Playwright Example - สาธิตการใช้งาน Playwright สำหรับ Browser Automation ในสถานการณ์จริง
"""

import asyncio
import json
import os
import random
import time

from playwright.async_api import async_playwright


# ฟังก์ชันสำหรับสร้างการหน่วงเวลาแบบมนุษย์
def human_delay(min_seconds=0.5, max_seconds=2.0):
    """สร้างการหน่วงเวลาแบบมนุษย์เพื่อให้การทำงานดูเป็นธรรมชาติ"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay


# ฟังก์ชันสำหรับพิมพ์ข้อความแบบมนุษย์
async def type_like_human(element, text, min_delay=0.05, max_delay=0.2):
    """พิมพ์ข้อความเข้าฟอร์มแบบมนุษย์ ทีละตัวอักษรพร้อมหน่วงเวลา"""
    for char in text:
        await element.type(char, delay=random.uniform(min_delay, max_delay) * 1000)


# ฟังก์ชันหลักสำหรับจำลองการทำธุรกรรม
async def simulate_transaction(merchant_url, card_info, proxy=None):
    """
    จำลองการทำธุรกรรมบนเว็บไซต์ด้วย Playwright

    Args:
        merchant_url: URL ของร้านค้า
        card_info: ข้อมูลบัตรที่ใช้ในการชำระเงิน
        proxy: Proxy ที่ใช้ในการเชื่อมต่อ (ถ้ามี)

    Returns:
        dict: ผลลัพธ์ของการทำธุรกรรม
    """
    async with async_playwright() as p:
        # ตั้งค่า Browser
        browser_type = p.chromium
        browser_args = []

        # ตั้งค่า Proxy ถ้ามี
        if proxy:
            browser_args.append(f"--proxy-server={proxy}")

        # เปิด Browser แบบ stealth mode
        browser = await browser_type.launch(
            headless=False, args=browser_args  # ตั้งเป็น True ในการใช้งานจริง
        )

        # สร้าง Context พร้อมตั้งค่า User-Agent เพื่อหลีกเลี่ยงการตรวจจับ
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="th-TH",
            timezone_id="Asia/Bangkok",
            viewport={"width": 1366, "height": 768},
        )

        # เปิดหน้าใหม่
        page = await context.new_page()

        try:
            # 1. เข้าสู่เว็บไซต์ร้านค้า
            print(f"กำลังเข้าสู่เว็บไซต์: {merchant_url}")
            await page.goto(merchant_url)
            human_delay(2, 4)

            # 2. จำลองการเลือกสินค้า (ตัวอย่าง)
            print("กำลังเลือกสินค้า...")

            # สมมติว่ามีปุ่ม "Add to Cart"
            try:
                add_to_cart_button = await page.wait_for_selector(
                    "button:has-text('Add to Cart')", timeout=5000
                )
                await add_to_cart_button.click()
                human_delay()
                print("เพิ่มสินค้าลงตะกร้าแล้ว")
            except:
                print("ไม่พบปุ่ม 'Add to Cart', กำลังหาปุ่มอื่น...")
                # ลองหาปุ่มอื่นที่คล้ายกัน
                buttons = await page.query_selector_all("button")
                for button in buttons:
                    text = await button.text_content()
                    if (
                        "cart" in text.lower()
                        or "buy" in text.lower()
                        or "add" in text.lower()
                    ):
                        await button.click()
                        human_delay()
                        print(f"คลิกปุ่ม '{text.strip()}'")
                        break

            # 3. ไปที่หน้าชำระเงิน
            print("กำลังไปที่หน้าชำระเงิน...")

            # สมมติว่ามีปุ่ม "Checkout" หรือ "ชำระเงิน"
            try:
                checkout_button = await page.wait_for_selector(
                    "a:has-text('Checkout'), button:has-text('Checkout')", timeout=5000
                )
                await checkout_button.click()
                human_delay(1, 3)
                print("ไปที่หน้าชำระเงินแล้ว")
            except:
                print("ไม่พบปุ่ม 'Checkout', กำลังหาปุ่มอื่น...")
                # ลองหาปุ่มที่เกี่ยวข้องกับการชำระเงิน
                checkout_elements = await page.query_selector_all("a, button")
                for element in checkout_elements:
                    text = await element.text_content()
                    if any(
                        keyword in text.lower()
                        for keyword in [
                            "checkout",
                            "payment",
                            "ชำระเงิน",
                            "ชำระ",
                            "สั่งซื้อ",
                        ]
                    ):
                        await element.click()
                        human_delay(1, 3)
                        print(f"คลิก '{text.strip()}'")
                        break

            # 4. กรอกข้อมูลบัตร
            print("กำลังกรอกข้อมูลบัตร...")

            # ตรวจสอบว่ามี iframe สำหรับการชำระเงินหรือไม่
            payment_frames = await page.frames
            main_frame = page

            for frame in payment_frames:
                frame_url = frame.url
                if (
                    "checkout" in frame_url
                    or "payment" in frame_url
                    or "stripe" in frame_url
                    or "paypal" in frame_url
                ):
                    main_frame = frame
                    print(f"พบ payment iframe: {frame_url}")
                    break

            # กรอกข้อมูลบัตร
            try:
                # หาฟิลด์กรอกหมายเลขบัตร
                card_number_field = await main_frame.wait_for_selector(
                    "input[name='cardnumber'], input[placeholder*='card'], input[aria-label*='Card']",
                    timeout=5000,
                )
                await type_like_human(card_number_field, card_info["card_number"])
                human_delay()

                # กรอกข้อมูลอื่นๆ
                # วันหมดอายุ
                expiry_field = await main_frame.wait_for_selector(
                    "input[name='exp-date'], input[placeholder*='MM'], input[aria-label*='expiration']",
                    timeout=5000,
                )
                await type_like_human(expiry_field, card_info["expiry"])
                human_delay()

                # CVC
                cvc_field = await main_frame.wait_for_selector(
                    "input[name='cvc'], input[placeholder*='CVC'], input[aria-label*='security']",
                    timeout=5000,
                )
                await type_like_human(cvc_field, card_info["cvc"])
                human_delay()

                # ชื่อบนบัตร (ถ้ามี)
                try:
                    name_field = await main_frame.wait_for_selector(
                        "input[name*='name'], input[placeholder*='name'], input[aria-label*='name']",
                        timeout=3000,
                    )
                    await type_like_human(name_field, card_info["name"])
                    human_delay()
                except:
                    print("ไม่พบฟิลด์ชื่อบนบัตร หรือไม่จำเป็นต้องกรอก")

                print("กรอกข้อมูลบัตรเรียบร้อย")
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการกรอกข้อมูลบัตร: {str(e)}")
                # บันทึกภาพหน้าจอเพื่อการแก้ไขปัญหา
                await page.screenshot(
                    path=os.path.join(os.getcwd(), "error_screenshot.png")
                )
                return {"success": False, "error": str(e)}

            # 5. กดยืนยันการชำระเงิน
            print("กำลังยืนยันการชำระเงิน...")

            # หาปุ่มยืนยันการชำระเงิน
            confirm_buttons = await main_frame.query_selector_all("button")
            submit_button = None

            for button in confirm_buttons:
                text = await button.text_content()
                if any(
                    keyword in text.lower()
                    for keyword in ["confirm", "pay", "submit", "ยืนยัน", "ชำระ"]
                ):
                    submit_button = button
                    break

            if submit_button:
                await submit_button.click()
                print("คลิกปุ่มยืนยันการชำระเงิน")

                # รอการประมวลผล
                human_delay(3, 5)

                # 6. ตรวจสอบผลลัพธ์
                print("กำลังตรวจสอบผลลัพธ์...")

                # จำลองการตรวจสอบผลลัพธ์ (ในการใช้งานจริงควรมีการตรวจสอบที่เหมาะสม)
                success_indicators = [
                    "success",
                    "thank you",
                    "ขอบคุณ",
                    "เสร็จสิ้น",
                    "สำเร็จ",
                ]
                error_indicators = [
                    "declined",
                    "error",
                    "fail",
                    "ล้มเหลว",
                    "ปฏิเสธ",
                    "ไม่สำเร็จ",
                ]

                page_content = await page.content()

                if any(
                    indicator in page_content.lower()
                    for indicator in success_indicators
                ):
                    print("การทำธุรกรรมสำเร็จ!")
                    # บันทึกภาพหน้าจอเพื่อยืนยัน
                    await page.screenshot(
                        path=os.path.join(os.getcwd(), "success_screenshot.png")
                    )
                    return {
                        "success": True,
                        "message": "Transaction completed successfully",
                    }
                elif any(
                    indicator in page_content.lower() for indicator in error_indicators
                ):
                    print("การทำธุรกรรมล้มเหลว")
                    # บันทึกภาพหน้าจอเพื่อการแก้ไขปัญหา
                    await page.screenshot(
                        path=os.path.join(os.getcwd(), "failure_screenshot.png")
                    )
                    return {"success": False, "message": "Transaction failed"}
                else:
                    print("ไม่สามารถระบุผลลัพธ์ได้ชัดเจน")
                    await page.screenshot(
                        path=os.path.join(os.getcwd(), "unknown_screenshot.png")
                    )
                    return {"success": None, "message": "Unclear transaction result"}
            else:
                print("ไม่พบปุ่มยืนยันการชำระเงิน")
                await page.screenshot(
                    path=os.path.join(os.getcwd(), "no_submit_button_screenshot.png")
                )
                return {"success": False, "error": "Submit button not found"}

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {str(e)}")
            # บันทึกภาพหน้าจอเพื่อการแก้ไขปัญหา
            try:
                await page.screenshot(
                    path=os.path.join(os.getcwd(), "error_screenshot.png")
                )
            except:
                pass
            return {"success": False, "error": str(e)}

        finally:
            # ปิด Browser
            await browser.close()
            print("ปิด Browser แล้ว")


# ฟังก์ชันสำหรับบันทึกผลลัพธ์ลงไฟล์
def log_result(merchant, card_info, result):
    """บันทึกผลลัพธ์การทำธุรกรรมลงไฟล์"""
    log_file = os.path.join(os.getcwd(), "transaction_logs.json")

    # สร้างข้อมูลล็อก
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "merchant": merchant,
        "card_info": {
            "card_type": card_info["card_type"],
            "bin": card_info["card_number"][:6]
            + "XXXXXX"
            + card_info["card_number"][-4:],
        },
        "result": result,
    }

    # ตรวจสอบว่ามีไฟล์ล็อกหรือไม่
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    else:
        logs = []

    # เพิ่มล็อกใหม่
    logs.append(log_entry)

    # บันทึกไฟล์
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"บันทึกผลลงไฟล์ {log_file} แล้ว")


# ฟังก์ชันหลักสำหรับเรียกใช้งาน
async def main():
    # ข้อมูลตัวอย่าง (ในการใช้งานจริง ควรเก็บไว้ในที่ปลอดภัย)
    merchant_url = "https://www.example-store.com/checkout"  # ตัวอย่าง URL

    card_info = {
        "card_type": "Visa",
        "card_number": "4111111111111111",  # บัตรทดสอบ
        "expiry": "12/25",
        "cvc": "123",
        "name": "JOHN DOE",
    }

    # Proxy (ถ้ามี)
    proxy = None  # "http://username:password@proxy-server:port"

    print("=== เริ่มการจำลองการทำธุรกรรม ===")
    result = await simulate_transaction(merchant_url, card_info, proxy)

    print(f"ผลลัพธ์: {result}")

    # บันทึกผลลัพธ์
    log_result("Example Store", card_info, result)

    print("=== เสร็จสิ้นการจำลอง ===")


# รันโปรแกรม
if __name__ == "__main__":
    # ใช้ asyncio เพื่อรันฟังก์ชัน async
    asyncio.run(main())
