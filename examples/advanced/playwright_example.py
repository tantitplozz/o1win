#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Playwright Example - Web Automation ที่เน้น Stealth Mode
"""

import asyncio
import json
import time
from datetime import datetime

from playwright.async_api import async_playwright


async def stealth_browser_session():
    """สร้าง Browser session แบบ stealth เพื่อหลีกเลี่ยงการตรวจจับ"""
    async with async_playwright() as p:
        # สร้าง browser context แบบ stealth
        browser = await p.chromium.launch(headless=False)

        # สร้าง context ที่มีการตั้งค่าเพื่อหลีกเลี่ยงการตรวจจับ
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            locale="th-TH",
            timezone_id="Asia/Bangkok",
            permissions=["geolocation"],
            java_script_enabled=True,
        )

        # เพิ่ม JavaScript เพื่อแก้ไข fingerprint
        await context.add_init_script(
            """
        // ปกปิด WebDriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
        
        // ปรับค่า Canvas fingerprint
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {
            if (this.width === 0 && this.height === 0) {
                return originalToDataURL.apply(this, arguments);
            }
            return originalToDataURL.apply(this, arguments);
        };
        
        // ปรับค่า AudioContext fingerprint
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function() {
            const result = originalGetChannelData.apply(this, arguments);
            return result;
        };
        """
        )

        # สร้าง page ใหม่
        page = await context.new_page()
        await page.goto("https://bot.sannysoft.com/")

        # รอให้ตรวจสอบเสร็จสิ้น
        await page.wait_for_timeout(5000)

        # บันทึกภาพหน้าจอ
        await page.screenshot(path="stealth_test_result.png")

        print("✅ ทดสอบการปกปิดตัวตนเสร็จสิ้น - ดูผลลัพธ์ได้ที่ stealth_test_result.png")

        # ตัวอย่างการดึงข้อมูลจากหน้าเว็บ
        await scrape_product_data(page)

        # ปิดหน้าเว็บ
        await browser.close()


async def scrape_product_data(page):
    """ตัวอย่างการดึงข้อมูลสินค้าจากเว็บอีคอมเมิร์ซ"""
    # ไปยังหน้าเว็บตัวอย่าง (ใช้ demo site)
    await page.goto("https://demo.opencart.com/")

    print("\n🔍 เริ่มดึงข้อมูลสินค้า...")

    # รอให้หน้าเว็บโหลดเสร็จ
    await page.wait_for_load_state("networkidle")

    # ค้นหาสินค้าทั้งหมดในหน้าแรก
    products = await page.query_selector_all(".product-thumb")

    result = []

    # ดึงข้อมูลจากแต่ละสินค้า
    for i, product in enumerate(products):
        # ดึงชื่อสินค้า
        name_element = await product.query_selector("h4 a")
        name = await name_element.inner_text() if name_element else "ไม่มีชื่อ"

        # ดึงราคา
        price_element = await product.query_selector(".price")
        price = await price_element.inner_text() if price_element else "ไม่มีราคา"

        # ดึง URL ของสินค้า
        url = await name_element.get_attribute("href") if name_element else ""

        # สร้าง URL เต็ม
        full_url = "https://demo.opencart.com/" + url if url else ""

        # เพิ่มข้อมูลเข้าไปในผลลัพธ์
        result.append(
            {
                "name": name,
                "price": price.replace("\n", " ").replace("\t", "").strip(),
                "url": full_url,
                "timestamp": datetime.now().isoformat(),
            }
        )

    # แสดงผลลัพธ์
    print(f"\n✅ ดึงข้อมูลเสร็จสิ้น พบสินค้า {len(result)} รายการ")
    print(json.dumps(result[:3], indent=2, ensure_ascii=False))

    # บันทึกผลลัพธ์ลงไฟล์
    with open("product_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n💾 บันทึกข้อมูลลงไฟล์ product_data.json เรียบร้อย")


async def interactive_automation():
    """ตัวอย่างการทำ automation แบบมีปฏิสัมพันธ์กับหน้าเว็บ"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # ไปยังหน้าเว็บ login ตัวอย่าง
        await page.goto("https://demo.opencart.com/index.php?route=account/login")

        print("\n🔐 เริ่มการทดสอบล็อกอิน...")

        # กรอกข้อมูลล็อกอิน
        await page.fill("#input-email", "test@example.com")
        await page.fill("#input-password", "password123")

        # คลิกปุ่มล็อกอิน
        await page.click("input[value='Login']")

        # รอให้หน้าเว็บโหลดเสร็จ
        await page.wait_for_load_state("networkidle")

        # ตรวจสอบว่ามีข้อความแจ้งเตือน
        alert = await page.query_selector(".alert-danger")
        if alert:
            alert_text = await alert.inner_text()
            print(f"❌ การล็อกอินล้มเหลว: {alert_text.strip()}")
        else:
            print("✅ การล็อกอินสำเร็จ")

        # ตัวอย่างการกรอกฟอร์มสมัครสมาชิก
        await page.goto("https://demo.opencart.com/index.php?route=account/register")

        print("\n📝 เริ่มทดสอบการกรอกฟอร์มสมัครสมาชิก...")

        # กรอกข้อมูลสมัครสมาชิก
        await page.fill("#input-firstname", "John")
        await page.fill("#input-lastname", "Doe")
        await page.fill("#input-email", f"test{int(time.time())}@example.com")
        await page.fill("#input-telephone", "0812345678")
        await page.fill("#input-password", "Password123!")
        await page.fill("#input-confirm", "Password123!")

        # เลือก checkbox ยอมรับเงื่อนไข
        await page.check("input[name='agree']")

        # คลิกปุ่มสมัครสมาชิก
        await page.click("input[value='Continue']")

        # รอให้หน้าเว็บโหลดเสร็จ
        await page.wait_for_load_state("networkidle")

        # ตรวจสอบผลลัพธ์
        success = await page.query_selector("h1")
        if success:
            success_text = await success.inner_text()
            if "account has been created" in success_text.lower():
                print("✅ การสมัครสมาชิกสำเร็จ")
            else:
                print(f"❓ ผลลัพธ์ไม่ชัดเจน: {success_text}")
        else:
            print("❌ การสมัครสมาชิกล้มเหลว")

        # ปิดหน้าเว็บ
        await browser.close()


# รันฟังก์ชันหลัก
if __name__ == "__main__":
    print("===== Playwright Stealth Automation Example =====")
    print("🌐 เริ่มทดสอบ Browser Automation แบบ Stealth...")

    # รันฟังก์ชัน stealth browser
    asyncio.run(stealth_browser_session())

    # รันฟังก์ชัน interactive automation
    print("\n\n===== Interactive Automation Example =====")
    asyncio.run(interactive_automation())
