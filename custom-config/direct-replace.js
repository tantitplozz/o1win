// สคริปต์แทนที่ VS Code ด้วย Cursor โดยตรง - เวอร์ชันที่เข้มงวด

// ประกาศตัวแปรใน window เพื่อตรวจสอบว่าสคริปต์ทำงานแล้ว
window.__CURSOR_SCRIPT_RUNNING = true;
console.log('===== DIRECT-REPLACE.JS LOADED =====');

// รันฟังก์ชันหลักทันทีเมื่อโหลดสคริปต์
(function executeImmediately() {
  console.log('===== EXECUTING CURSOR REPLACEMENT IMMEDIATELY =====');

  // ลบแท็บ VS Code ออกจาก DOM โดยตรงทันที
  const removeVSCodeTabsDirectly = function () {
    // ค้นหาทุกองค์ประกอบที่เกี่ยวข้องกับ VS Code
    const vscodeElements = document.querySelectorAll(
      '[data-tab="vscode"], [title*="VS Code"], [aria-label*="VS Code"]'
    );
    console.log('Found VS Code elements to remove:', vscodeElements.length);

    // ลบออกจาก DOM
    vscodeElements.forEach((element) => {
      element.remove();
      console.log('Removed VS Code element from DOM');
    });

    // ค้นหาแท็บที่มีข้อความ VS Code
    document.querySelectorAll('button, [role="tab"]').forEach((element) => {
      if (element.textContent && element.textContent.includes('VS Code')) {
        element.remove();
        console.log('Removed VS Code tab/button from DOM');
      }
    });
  };

  // เรียกใช้งานทันที
  removeVSCodeTabsDirectly();

  // เรียกซ้ำเพื่อให้แน่ใจว่าถูกลบ
  setTimeout(removeVSCodeTabsDirectly, 100);
  setTimeout(removeVSCodeTabsDirectly, 500);
  setTimeout(removeVSCodeTabsDirectly, 1000);
})();

(function () {
  // ฟังก์ชันแทนที่ข้อความ VS Code ด้วย Cursor ในทุกส่วนของหน้าเว็บ
  function replaceVSCodeWithCursor() {
    console.log('====== Direct Replace Script Running ======');

    // บังคับค่า localStorage ก่อนทำอย่างอื่น
    if (window.localStorage) {
      window.localStorage.setItem('defaultTab', 'cursor');
      window.localStorage.setItem('editor', 'cursor');
      window.localStorage.setItem('editorType', 'cursor');
      window.localStorage.setItem('activeEditor', 'cursor');
      window.localStorage.setItem('defaultEditor', 'cursor');

      // ลบการตั้งค่าที่เกี่ยวข้องกับ VS Code
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (
          key &&
          (key.includes('vscode') ||
            key.includes('VSCode') ||
            key.includes('vs-code'))
        ) {
          localStorage.removeItem(key);
          console.log('Removed localStorage key:', key);
        }
      }

      // ตั้งค่า tabsConfig
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
      ];
      window.localStorage.setItem('tabsConfig', JSON.stringify(tabsConfig));
      window.localStorage.setItem('tabsVisible', JSON.stringify(['cursor']));

      console.log('Set all localStorage values to force Cursor');
    }

    // ลบแท็บ VS Code ออกจาก DOM โดยตรง
    const vscodeTabs = document.querySelectorAll(
      '[data-tab="vscode"], [title*="VS Code"], [aria-label*="VS Code"]'
    );
    vscodeTabs.forEach((element) => {
      element.remove();
      console.log('Removed VS Code element from DOM');
    });

    // ค้นหาทุกองค์ประกอบข้อความในหน้าเว็บ
    const textNodes = [];
    function findTextNodes(node) {
      if (node.nodeType === 3) {
        // Node.TEXT_NODE
        textNodes.push(node);
      } else {
        for (let i = 0; i < node.childNodes.length; i++) {
          findTextNodes(node.childNodes[i]);
        }
      }
    }
    findTextNodes(document.body);

    // แทนที่ข้อความ "VS Code" ด้วย "Cursor" ในทุกโหนดข้อความ
    textNodes.forEach((node) => {
      if (
        node.nodeValue &&
        (node.nodeValue.includes('VS Code') ||
          node.nodeValue.includes('VSCode'))
      ) {
        node.nodeValue = node.nodeValue.replace(/VS\s*Code/g, 'Cursor');
        node.nodeValue = node.nodeValue.replace(/VSCode/g, 'Cursor');
      }
    });

    // แทนที่ข้อความในแอตทริบิวต์
    const elementsWithAttributes = document.querySelectorAll(
      '[title], [alt], [placeholder], [aria-label], [data-tooltip]'
    );
    elementsWithAttributes.forEach((element) => {
      ['title', 'alt', 'placeholder', 'aria-label', 'data-tooltip'].forEach(
        (attr) => {
          if (element.hasAttribute(attr)) {
            const value = element.getAttribute(attr);
            if (
              value &&
              (value.includes('VS Code') || value.includes('VSCode'))
            ) {
              element.setAttribute(
                attr,
                value
                  .replace(/VS\s*Code/g, 'Cursor')
                  .replace(/VSCode/g, 'Cursor')
              );
            }
          }
        }
      );
    });

    // แทนที่ชื่อแท็บ
    const tabElements = document.querySelectorAll('[role="tab"]');
    tabElements.forEach((tab) => {
      if (
        tab.textContent.includes('VS Code') ||
        tab.textContent.includes('VSCode')
      ) {
        // แทนที่ข้อความแทนการซ่อน
        const originalText = tab.textContent;
        tab.textContent = originalText
          .replace(/VS\s*Code/g, 'Cursor')
          .replace(/VSCode/g, 'Cursor');
        tab.setAttribute('data-tab', 'cursor');
        tab.setAttribute('data-custom-tab', 'true');
        tab.setAttribute('aria-selected', 'true');
        tab.style.backgroundColor = '#1F1FCF';
        tab.style.color = 'white';
        tab.style.fontWeight = 'bold';
        tab.style.display = 'flex';
        tab.style.position = 'relative';
        tab.style.zIndex = '1000';
        tab.click(); // คลิกที่แท็บ
        console.log('Modified VS Code tab to Cursor');
      }
    });

    // แทนที่ข้อความใน DOM
    document
      .querySelectorAll('button, a, div, span, h1, h2, h3, h4, h5, h6, p, li')
      .forEach((element) => {
        if (
          element.textContent.includes('VS Code') ||
          element.textContent.includes('VSCode')
        ) {
          Array.from(element.childNodes).forEach((child) => {
            if (child.nodeType === 3) {
              // Node.TEXT_NODE
              child.nodeValue = child.nodeValue
                .replace(/VS\s*Code/g, 'Cursor')
                .replace(/VSCode/g, 'Cursor');
            }
          });
        }
      });

    // ฟังก์ชันสำหรับสร้างแท็บ Cursor ใหม่
    function createNewCursorTab() {
      console.log('Creating new Cursor tab...');
      // สร้าง Element ใหม่
      const newCursorTab = document.createElement('button');
      newCursorTab.textContent = 'Cursor';
      newCursorTab.setAttribute('role', 'tab');
      newCursorTab.setAttribute('data-tab', 'cursor');
      newCursorTab.setAttribute('data-custom-tab', 'true');
      newCursorTab.setAttribute('aria-selected', 'true');
      newCursorTab.style.backgroundColor = '#1F1FCF';
      newCursorTab.style.color = 'white';
      newCursorTab.style.fontWeight = 'bold';
      newCursorTab.style.padding = '8px 16px';
      newCursorTab.style.border = 'none';
      newCursorTab.style.margin = '4px';
      newCursorTab.style.borderRadius = '4px';
      newCursorTab.style.cursor = 'pointer';
      newCursorTab.style.display = 'flex';
      newCursorTab.style.alignItems = 'center';
      newCursorTab.style.justifyContent = 'center';
      newCursorTab.style.position = 'relative';
      newCursorTab.style.zIndex = '1000';

      // เพิ่ม Event Listener สำหรับการคลิก
      newCursorTab.addEventListener('click', function () {
        console.log('Custom Cursor tab clicked');
        // บังคับเปลี่ยนเป็น Cursor
        if (window.localStorage) {
          window.localStorage.setItem('defaultTab', 'cursor');
          window.localStorage.setItem('editor', 'cursor');
          window.localStorage.setItem('editorType', 'cursor');
        }

        // ค้นหาคอนเทนเนอร์ที่เกี่ยวข้องกับ Cursor
        const cursorContainers = document.querySelectorAll(
          '[data-editor="cursor"]'
        );
        cursorContainers.forEach((container) => {
          container.style.display = 'block';
        });

        // ซ่อนคอนเทนเนอร์ของ VS Code
        const vscodeContainers = document.querySelectorAll(
          '[data-editor="vscode"]'
        );
        vscodeContainers.forEach((container) => {
          container.style.display = 'none';
        });
      });

      return newCursorTab;
    }

    // เพิ่มแท็บ Cursor อย่างชัดเจน
    function addCursorTab() {
      console.log('Attempting to add Cursor tab...');

      // ค้นหาแท็บคอนเทนเนอร์ด้วยวิธีที่หลากหลาย
      const tabContainers = [
        document.querySelector('[role="tablist"]'),
        document.querySelector('.tabs-container'),
        document.querySelector('.tab-list'),
        document.querySelector('.editor-tabs'),
        document.querySelector('header nav'),
        document.querySelector('nav'),
        document.querySelector('.tabbed-editor'),
        document.querySelector('[class*="tab"]'),
        document.querySelector('[class*="Tab"]'),
        document.querySelector('.openhands-header'),
        document.querySelector('header'),
        document.querySelector('div[role="navigation"]'),
        document.querySelector('ul[role="tablist"]'),
        document.querySelector('.tab-container'),
        document.querySelector('.editor-container'),
        document.querySelector('.tabs'),
      ];

      const tabContainer = tabContainers.find(
        (container) => container !== null
      );

      if (tabContainer) {
        console.log('Found tab container:', tabContainer);

        // ค้นหาแท็บ Cursor ที่มีอยู่แล้ว
        const existingCursorTab = Array.from(tabContainer.children).find(
          (tab) => tab.textContent.includes('Cursor')
        );

        if (!existingCursorTab) {
          console.log('No existing Cursor tab found, creating new one');

          // ใช้แท็บแรกเป็นเทมเพลต หรือสร้างใหม่ถ้าไม่มี
          if (tabContainer.children.length > 0) {
            const firstTab = tabContainer.firstElementChild;
            console.log('Using first child as template:', firstTab);

            // สร้างแท็บ Cursor ใหม่
            const cursorTab = firstTab.cloneNode(true);

            // กำหนดคุณสมบัติให้แท็บ
            cursorTab.textContent = 'Cursor';
            cursorTab.setAttribute('data-tab', 'cursor');
            cursorTab.setAttribute('data-custom-tab', 'true');
            cursorTab.setAttribute('aria-selected', 'true');
            cursorTab.style.backgroundColor = '#1F1FCF';
            cursorTab.style.color = 'white';
            cursorTab.style.fontWeight = 'bold';
            cursorTab.style.display = 'flex';
            cursorTab.style.position = 'relative';
            cursorTab.style.zIndex = '1000';

            // เพิ่มแท็บลงในคอนเทนเนอร์
            tabContainer.insertBefore(cursorTab, firstTab);

            // คลิกที่แท็บ Cursor
            setTimeout(() => {
              cursorTab.click();
              console.log('Added and clicked on new Cursor tab (clone)');
            }, 100);

            return true;
          } else {
            console.log('No children in tab container, creating brand new tab');
            // สร้างแท็บใหม่เลย
            const newTab = createNewCursorTab();
            tabContainer.appendChild(newTab);

            setTimeout(() => {
              newTab.click();
              console.log('Added and clicked on new Cursor tab (new)');
            }, 100);

            return true;
          }
        } else {
          console.log('Found existing Cursor tab, updating it');
          // ถ้ามีแท็บ Cursor อยู่แล้ว ทำให้มันถูกเลือก
          existingCursorTab.style.backgroundColor = '#1F1FCF';
          existingCursorTab.style.color = 'white';
          existingCursorTab.style.fontWeight = 'bold';
          existingCursorTab.style.display = 'flex';
          existingCursorTab.style.position = 'relative';
          existingCursorTab.style.zIndex = '1000';
          existingCursorTab.setAttribute('aria-selected', 'true');

          setTimeout(() => {
            existingCursorTab.click();
            console.log('Selected existing Cursor tab');
          }, 100);

          return true;
        }
      } else {
        console.log('No tab container found');
      }

      return false;
    }

    // ทำการสร้างแท็บ Cursor
    const tabAdded = addCursorTab();

    // ถ้าไม่สามารถเพิ่มแท็บได้ ให้ลองวิธีอื่น
    if (!tabAdded) {
      console.log(
        'Failed to add tab through container, trying alternative methods'
      );

      // ค้นหาแท็บหรือปุ่มที่มีอยู่และปรับเปลี่ยน
      const buttons = document.querySelectorAll('button');

      let cursorButtonFound = false;
      buttons.forEach((button) => {
        if (button.textContent.includes('VS Code')) {
          button.textContent = button.textContent.replace(
            /VS\s*Code/g,
            'Cursor'
          );
          button.style.backgroundColor = '#1F1FCF';
          button.style.color = 'white';
          button.style.fontWeight = 'bold';
          button.style.display = 'flex';
          button.style.position = 'relative';
          button.style.zIndex = '1000';
          button.setAttribute('data-tab', 'cursor');
          button.click();
          console.log('Converted VS Code button to Cursor');
          cursorButtonFound = true;
        } else if (button.textContent.includes('Cursor')) {
          button.style.backgroundColor = '#1F1FCF';
          button.style.color = 'white';
          button.style.fontWeight = 'bold';
          button.style.display = 'flex';
          button.style.position = 'relative';
          button.style.zIndex = '1000';
          button.click();
          console.log('Found and clicked existing Cursor button');
          cursorButtonFound = true;
        }
      });

      // วิธีที่สาม: สร้างปุ่ม Cursor แบบลอยบนหน้าจอ (Floating Button)
      if (
        !cursorButtonFound &&
        !document.querySelector('[data-custom-cursor-tab]')
      ) {
        console.log('Creating floating Cursor button');

        const cursorButton = createNewCursorTab();
        cursorButton.setAttribute('data-custom-cursor-tab', 'true');

        // กำหนดสไตล์ให้ลอยบนหน้าจอ
        cursorButton.style.position = 'fixed';
        cursorButton.style.top = '50px'; // ใต้ header
        cursorButton.style.left = '50%';
        cursorButton.style.transform = 'translateX(-50%)'; // จัดกึ่งกลาง
        cursorButton.style.zIndex = '9999';
        cursorButton.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';

        document.body.appendChild(cursorButton);
        console.log('Created floating Cursor button');

        setTimeout(() => {
          cursorButton.click();
        }, 100);
      }
    }

    // เพิ่ม stylesheet สำหรับบังคับแสดง Cursor และซ่อน VS Code
    if (!document.getElementById('cursor-force-styles')) {
      console.log('Adding global stylesheet for Cursor/VS Code visibility');
      const styleSheet = document.createElement('style');
      styleSheet.id = 'cursor-force-styles';
      styleSheet.textContent = `
        /* แสดง Cursor เสมอ */
        [data-tab="cursor"], [data-value="cursor"], [title*="Cursor"], [data-custom-tab="true"] {
          display: flex !important;
          visibility: visible !important;
          opacity: 1 !important;
          position: relative !important;
          z-index: 1000 !important;
        }
        
        /* ซ่อน VS Code เสมอ */
        [data-tab="vscode"], [data-value="vscode"], [title*="VS Code"], 
        [aria-label*="VS Code"], div[data-tab="vscode"], button[data-tab="vscode"],
        *:has(> span:contains("VS Code")), *:has(> div:contains("VS Code")) {
          display: none !important;
          visibility: hidden !important;
          opacity: 0 !important;
          height: 0 !important;
          width: 0 !important;
          overflow: hidden !important;
          pointer-events: none !important;
          position: absolute !important;
          z-index: -1000 !important;
        }

        /* ซ่อน iframe ของ VS Code */
        iframe[src*="vscode"], iframe[title*="VS Code"], iframe[class*="vscode"] {
          display: none !important;
          visibility: hidden !important;
          opacity: 0 !important;
          height: 0 !important;
          width: 0 !important;
        }
      `;
      document.head.appendChild(styleSheet);
    }
  }

  // เรียกใช้ฟังก์ชันเมื่อโหลดหน้าเว็บ
  function init() {
    console.log('Initializing direct-replace.js');
    replaceVSCodeWithCursor();

    // เรียกใช้ซ้ำๆ ถี่ๆ ในช่วงแรก
    setTimeout(replaceVSCodeWithCursor, 100);
    setTimeout(replaceVSCodeWithCursor, 500);
    setTimeout(replaceVSCodeWithCursor, 1000);
    setTimeout(replaceVSCodeWithCursor, 2000);

    // เรียกใช้ต่อเนื่องทุก 2 วินาที
    setInterval(replaceVSCodeWithCursor, 2000);
  }

  // เรียกใช้เมื่อโหลด DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // เรียกใช้เมื่อโหลดหน้าเว็บเสร็จสมบูรณ์
  window.addEventListener('load', () => {
    console.log('Page fully loaded, running direct replacement');
    replaceVSCodeWithCursor();
    setTimeout(replaceVSCodeWithCursor, 500);
    setTimeout(replaceVSCodeWithCursor, 2000);
    setTimeout(replaceVSCodeWithCursor, 5000);
  });

  // ใช้ MutationObserver เพื่อตรวจจับการเปลี่ยนแปลง DOM
  const observer = new MutationObserver(() => {
    replaceVSCodeWithCursor();
  });

  // เริ่มสังเกตการณ์
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
  });
})();
