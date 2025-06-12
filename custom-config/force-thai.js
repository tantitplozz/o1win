// สคริปต์บังคับการใช้ภาษาไทยใน OpenHands

(function () {
  // บังคับให้ใช้ภาษาไทยใน localStorage
  localStorage.setItem('locale', 'th');

  // รายการภาษาที่ต้องมี
  const availableLocales = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'th', name: 'Thai', native: 'ไทย' },
    { code: 'ja', name: 'Japanese', native: '日本語' },
    { code: 'zh-CN', name: 'Simplified Chinese', native: '简体中文' },
    { code: 'zh-TW', name: 'Traditional Chinese', native: '繁體中文' },
    { code: 'ko', name: 'Korean', native: '한국어' },
    { code: 'no', name: 'Norwegian', native: 'Norsk' },
    { code: 'ar', name: 'Arabic', native: 'العربية' },
  ];

  // บันทึกรายการภาษาลงใน localStorage
  localStorage.setItem('locales', JSON.stringify(availableLocales));

  // เพิ่มภาษาไทยเข้าไปในเมนูภาษาโดยตรง
  function addThaiToLanguageMenu() {
    // ค้นหาปุ่มเลือกภาษา
    const languageButtons = Array.from(
      document.querySelectorAll('button')
    ).filter(
      (button) =>
        button.textContent.includes('Language') ||
        button.textContent.includes('ภาษา')
    );

    if (languageButtons.length > 0) {
      // คลิกปุ่มเพื่อเปิดเมนู
      languageButtons[0].click();

      // รอให้เมนูเปิด
      setTimeout(() => {
        // ค้นหาเมนูภาษา
        const languageMenus = document.querySelectorAll('[role="listbox"]');

        languageMenus.forEach((menu) => {
          const options = Array.from(menu.children);

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
            console.log('Force added Thai language to menu');

            // เลือกภาษาไทย
            thaiOption.click();
          }
        });
      }, 500);
    }
  }

  // รอให้หน้าเว็บโหลดเสร็จแล้วเรียกใช้ฟังก์ชั่น
  window.addEventListener('load', () => {
    setTimeout(addThaiToLanguageMenu, 2000);
  });

  // หากเป็นหน้า settings/app ให้รอแล้วเรียกใช้ฟังก์ชั่น
  if (window.location.href.includes('/settings/app')) {
    setTimeout(addThaiToLanguageMenu, 2000);
    setTimeout(addThaiToLanguageMenu, 5000);
  }
})();
