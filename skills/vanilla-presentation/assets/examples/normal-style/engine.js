
let currentStep = 0;
const steps = Array.from(document.querySelectorAll('.step'));
const sidebarItems = Array.from(document.querySelectorAll('.sidebar-item'));
const presentation = document.getElementById('presentation');

function update() {
  const activeStep = steps[currentStep];
  if (!activeStep) return;
  
  const x = parseFloat(activeStep.getAttribute('data-x'));
  const y = parseFloat(activeStep.getAttribute('data-y'));

  // 슬라이드 이동 (Transform 방식)
  presentation.style.transform = `translate(${-x}px, ${-y}px)`;

  // 상태 업데이트
  steps.forEach((s, i) => {
    s.style.opacity = (i === currentStep) ? "1" : "0";
    s.classList.toggle('active', i === currentStep);
  });

  sidebarItems.forEach((item, i) => {
    item.classList.toggle('active', i === currentStep);
  });
}

function next() { if (currentStep < steps.length - 1) { currentStep++; update(); } }
function prev() { if (currentStep > 0) { currentStep--; update(); } }
function goTo(idx) { currentStep = idx; update(); }

document.addEventListener('keydown', (e) => {
  const key = e.key.toLowerCase();
  if (key === 'arrowright') { e.preventDefault(); next(); }
  if (key === 'arrowleft') { e.preventDefault(); prev(); }
});

sidebarItems.forEach((item, i) => {
  item.addEventListener('click', () => goTo(i));
});

// 초기화
update();
