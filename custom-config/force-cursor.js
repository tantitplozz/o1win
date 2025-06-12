// สคริปต์บังคับการใช้ Cursor ใน OpenHands

(function () {
  // บังคับให้ใช้ Cursor ใน localStorage
  function forceCursorSettings() {
    localStorage.setItem('defaultTab', 'cursor');
    localStorage.setItem('editor', 'cursor');
    localStorage.setItem('editorType', 'cursor');

    // กำหนดค่า tabsConfig
    const tabsConfig = [
      {
        type: 'cursor',
        name: 'Cursor',
        label: 'Cursor',
        description: 'แก้ไขโค้ดด้วย Cursor Editor',
        enabled: true,
        default: true,
        logoUrl: '/custom/cursor-logo.svg',
      },
      {
        type: 'vscode',
        name: 'VS Code',
        label: 'VS Code',
        description: 'แก้ไขโค้ดด้วย VS Code Editor',
        enabled: false,
      },
    ];

    localStorage.setItem('tabsConfig', JSON.stringify(tabsConfig));
    console.log('Forced Cursor as default editor in localStorage');
  }

  // ฟังก์ชันเปลี่ยน Editor เป็น Cursor
  function switchToCursor() {
    // ค้นหาและคลิกที่แท็บ Cursor
    const cursorButtons = Array.from(
      document.querySelectorAll('button')
    ).filter((button) => button.textContent.includes('Cursor'));

    if (cursorButtons.length > 0) {
      cursorButtons[0].click();
      console.log('Clicked on Cursor tab');
    }

    // ค้นหาและซ่อนแท็บ VS Code
    const vscodeButtons = Array.from(
      document.querySelectorAll('button')
    ).filter(
      (button) =>
        button.textContent.includes('VS Code') ||
        button.textContent.includes('VSCode')
    );

    vscodeButtons.forEach((button) => {
      button.style.display = 'none';
      console.log('Hidden VS Code button');
    });

    // ปิด VS Code tab ที่กำลังแสดงอยู่ (ถ้ามี)
    const vscodeTabs = Array.from(
      document.querySelectorAll('[role="tab"]')
    ).filter((tab) => tab.textContent.includes('VS Code'));

    vscodeTabs.forEach((tab) => {
      tab.style.display = 'none';
      console.log('Hidden VS Code tab');
    });

    // หากมีแท็บ VS Code ที่กำลังใช้งานอยู่ ให้เปลี่ยนเป็น Cursor
    if (document.querySelector('.vs-code-container')) {
      const cursorTab = Array.from(
        document.querySelectorAll('[role="tab"]')
      ).find((tab) => tab.textContent.includes('Cursor'));
      if (cursorTab) {
        cursorTab.click();
      }
    }
  }

  // ตั้งค่าเริ่มต้น
  forceCursorSettings();

  // รันฟังก์ชันซ้ำๆ เพื่อให้แน่ใจว่าการตั้งค่าถูกใช้งาน
  setInterval(forceCursorSettings, 1000);

  // สังเกตการณ์การเปลี่ยนแปลงของ DOM
  const observer = new MutationObserver((mutations) => {
    for (let mutation of mutations) {
      if (mutation.type === 'childList') {
        switchToCursor();
      }
    }
  });

  // ใช้ MutationObserver เพื่อตรวจจับการเปลี่ยนแปลงของ DOM
  document.addEventListener('DOMContentLoaded', () => {
    observer.observe(document.body, { childList: true, subtree: true });
    switchToCursor();

    // รันตรวจสอบซ้ำๆ
    setTimeout(switchToCursor, 1000);
    setTimeout(switchToCursor, 3000);
    setTimeout(switchToCursor, 5000);
  });

  // เมื่อโหลดหน้าเว็บเสร็จสมบูรณ์
  window.addEventListener('load', () => {
    switchToCursor();

    // รันตรวจสอบซ้ำๆ
    setTimeout(switchToCursor, 1000);
    setTimeout(switchToCursor, 3000);
    setTimeout(switchToCursor, 5000);
  });
})();
