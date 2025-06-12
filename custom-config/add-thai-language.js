// สคริปต์สำหรับเพิ่มภาษาไทยเข้าไปในตัวเลือกภาษา

(function () {
  // ฟังก์ชั่นเพื่อเพิ่มภาษาไทยเข้าไปในตัวเลือกภาษา
  function addThaiLanguage() {
    // ตั้งค่าภาษาไทยใน localStorage
    window.localStorage.setItem('locale', 'th');

    // อัปเดตรายการภาษาใน localStorage
    try {
      // รายการภาษาที่ต้องมี
      const requiredLanguages = [
        { code: 'en', name: 'English', native: 'English' },
        { code: 'th', name: 'Thai', native: 'ไทย' },
        { code: 'ja', name: '日本語', native: '日本語' },
        { code: 'zh-CN', name: '简体中文', native: '简体中文' },
        { code: 'zh-TW', name: '繁體中文', native: '繁體中文' },
        { code: 'ko', name: '한국어', native: '한국어' },
        { code: 'no', name: 'Norsk', native: 'Norsk' },
        { code: 'ar', name: 'العربية', native: 'العربية' },
      ];

      // อัปเดต localStorage
      window.localStorage.setItem('locales', JSON.stringify(requiredLanguages));
      console.log('Added Thai language to localStorage');
    } catch (e) {
      console.error('Error updating language list:', e);
    }

    // ค้นหาและแก้ไขเมนูภาษาในหน้าเว็บ
    function updateLanguageMenu() {
      // ค้นหาเมนูภาษา
      const languageMenus = document.querySelectorAll('[role="listbox"]');

      // ตรวจสอบทุกเมนูที่พบ
      languageMenus.forEach((menu) => {
        // ตรวจสอบว่าเป็นเมนูภาษาหรือไม่
        const options = Array.from(menu.children);
        const languageOptions = options.filter(
          (option) =>
            option.textContent.includes('English') ||
            option.textContent.includes('日本語') ||
            option.textContent.includes('简体中文') ||
            option.textContent.includes('繁體中文')
        );

        if (languageOptions.length > 0) {
          // ตรวจสอบว่ามีภาษาไทยหรือไม่
          const hasThaiOption = options.some((option) =>
            option.textContent.includes('ไทย')
          );

          // ถ้าไม่มีภาษาไทย ให้เพิ่มเข้าไป
          if (!hasThaiOption && options.length > 0) {
            const template = options[0];
            const thaiOption = template.cloneNode(true);
            thaiOption.textContent = 'ไทย';
            thaiOption.setAttribute('data-value', 'th');

            // เพิ่มเข้าไปในเมนู
            menu.appendChild(thaiOption);
            console.log('Added Thai language option to menu');
          }
        }
      });
    }

    // ใช้ MutationObserver เพื่อตรวจจับการเปลี่ยนแปลงของ DOM
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          // ตรวจสอบว่ามีเมนูภาษาหรือไม่
          updateLanguageMenu();
        }
      });
    });

    // เริ่มการสังเกตการณ์
    observer.observe(document.body, { childList: true, subtree: true });

    // เรียกใช้ทันทีเผื่อเมนูภาษาถูกโหลดไปแล้ว
    updateLanguageMenu();
  }

  // เรียกใช้ฟังก์ชั่นเมื่อหน้าเว็บโหลดเสร็จ
  if (document.readyState === 'complete') {
    addThaiLanguage();
  } else {
    window.addEventListener('load', addThaiLanguage);
  }

  // เรียกใช้อีกครั้งหลังจากโหลดเสร็จสักพัก
  setTimeout(addThaiLanguage, 2000);
  setTimeout(addThaiLanguage, 5000);
})();
