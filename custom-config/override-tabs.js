// สคริปต์แทนที่แท็บ (Override Tabs)

(function () {
  // รายการแท็บที่ต้องการแสดง (เฉพาะ Cursor)
  const TABS_CONFIG = [
    {
      type: 'cursor',
      name: 'Cursor',
      label: 'Cursor',
      description: 'แก้ไขโค้ดด้วย Cursor Editor',
      enabled: true,
      default: true,
      logoUrl: '/custom/cursor-logo.svg',
    },
  ];

  // ฟังก์ชันแทนที่ค่าในหน้าเว็บ
  function overrideTabs() {
    // บังคับการตั้งค่าใน localStorage
    if (window.localStorage) {
      // กำหนดค่า
      window.localStorage.setItem('defaultTab', 'cursor');
      window.localStorage.setItem('editor', 'cursor');
      window.localStorage.setItem('editorType', 'cursor');
      window.localStorage.setItem('activeEditor', 'cursor');
      window.localStorage.setItem('defaultEditor', 'cursor');
      window.localStorage.setItem('tabsConfig', JSON.stringify(TABS_CONFIG));
      window.localStorage.setItem('tabsVisible', JSON.stringify(['cursor']));
      window.localStorage.removeItem('vscodeConfig');

      // ลบค่าเก่าที่อาจมีผลต่อการแสดง VS Code
      const keysToCheck = Object.keys(window.localStorage);
      keysToCheck.forEach((key) => {
        if (key.includes('vscode') || key.includes('VSCode')) {
          window.localStorage.removeItem(key);
        }
      });
    }

    // ปรับแต่ง DOM
    // 1. ซ่อนแท็บ VS Code
    const vscodeTabs = document.querySelectorAll(
      '[data-tab="vscode"], [data-value="vscode"], button:has(span:contains("VS Code"))'
    );
    vscodeTabs.forEach((tab) => {
      tab.style.display = 'none';
      tab.setAttribute('disabled', 'true');
      tab.style.visibility = 'hidden';
    });

    // 2. แสดงแท็บ Cursor
    const cursorTabs = document.querySelectorAll(
      '[data-tab="cursor"], [data-value="cursor"]'
    );
    cursorTabs.forEach((tab) => {
      tab.style.display = 'flex';
      tab.removeAttribute('disabled');
      tab.style.visibility = 'visible';
      tab.setAttribute('aria-selected', 'true');
    });

    // 3. ลบคอนเทนเนอร์ของ VS Code
    const vscodeContainers = document.querySelectorAll(
      '.vscode-container, .vs-code-container'
    );
    vscodeContainers.forEach((container) => {
      container.remove();
    });

    // 4. คลิกที่แท็บ Cursor (ถ้ามี)
    setTimeout(() => {
      const cursorTabButton = Array.from(
        document.querySelectorAll('button')
      ).find((button) => button.textContent.includes('Cursor'));
      if (cursorTabButton) {
        cursorTabButton.click();
        console.log('Clicked on Cursor tab button');
      }
    }, 100);

    // 5. เพิ่ม style เพื่อซ่อน VS Code
    const style = document.createElement('style');
    style.textContent = `
      [data-tab="vscode"], [title*="VS Code"], button:has(span:contains("VS Code")) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
      }
      iframe[src*="vscode"] {
        display: none !important;
      }
      [data-tab="cursor"], [title*="Cursor"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background-color: #1F1FCF !important;
        color: white !important;
      }
    `;
    document.head.appendChild(style);
  }

  // เรียกใช้งานฟังก์ชันทันที
  overrideTabs();

  // เรียกใช้งานฟังก์ชันซ้ำๆ
  setInterval(overrideTabs, 1000);

  // เรียกใช้งานเมื่อโหลดหน้าเว็บ
  window.addEventListener('DOMContentLoaded', () => {
    overrideTabs();
    setTimeout(overrideTabs, 500);
    setTimeout(overrideTabs, 1000);
  });

  // เรียกใช้งานเมื่อโหลดหน้าเว็บเสร็จสมบูรณ์
  window.addEventListener('load', () => {
    overrideTabs();
    setTimeout(overrideTabs, 500);
    setTimeout(overrideTabs, 1000);
    setTimeout(overrideTabs, 2000);
  });

  // ใช้ MutationObserver เพื่อตรวจจับการเปลี่ยนแปลงของ DOM
  const observer = new MutationObserver(() => {
    overrideTabs();
  });

  // เริ่มสังเกตการณ์เมื่อโหลดหน้าเว็บเสร็จ
  window.addEventListener('load', () => {
    observer.observe(document.body, { childList: true, subtree: true });
  });
})();
