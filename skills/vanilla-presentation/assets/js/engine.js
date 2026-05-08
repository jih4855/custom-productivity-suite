
let currentStep = 0;
let overviewMode = false;
const steps = Array.from(document.querySelectorAll('.step'));
const sidebarItems = Array.from(document.querySelectorAll('.sidebar-item'));
const presentation = document.getElementById('presentation');

function update() {
  const activeStep = steps[currentStep];
  if (!activeStep) return;

  if (overviewMode) {
    updateOverview();
    return;
  }
  
  const x = parseFloat(activeStep.getAttribute('data-x'));
  const y = parseFloat(activeStep.getAttribute('data-y'));

  document.body.classList.remove('overview-mode');
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

function updateOverview() {
  document.body.classList.add('overview-mode');
  presentation.style.transform = 'none';
  steps.forEach((s, i) => {
    s.style.opacity = "1";
    s.classList.toggle('active', i === currentStep);
  });
  sidebarItems.forEach((item, i) => {
    item.classList.toggle('active', i === currentStep);
  });
}

function next() { if (currentStep < steps.length - 1) { currentStep++; update(); } }
function prev() { if (currentStep > 0) { currentStep--; update(); } }
function goTo(idx) { currentStep = idx; update(); }
function toggleOverview(force) {
  overviewMode = typeof force === 'boolean' ? force : !overviewMode;
  update();
}

document.addEventListener('keydown', (e) => {
  const key = e.key.toLowerCase();
  if (key === 'arrowright' || key === 'pagedown' || key === ' ') { e.preventDefault(); next(); }
  if (key === 'arrowleft' || key === 'pageup') { e.preventDefault(); prev(); }
  if (key === 'home') { e.preventDefault(); currentStep = 0; update(); }
  if (key === 'end') { e.preventDefault(); currentStep = steps.length - 1; update(); }
  if (key === 'o') { e.preventDefault(); toggleOverview(); }
  if (key === 'escape' && overviewMode) { e.preventDefault(); toggleOverview(false); }
});

sidebarItems.forEach((item, i) => {
  item.addEventListener('click', () => goTo(i));
});

steps.forEach((step, i) => {
  step.addEventListener('click', () => {
    if (!overviewMode) return;
    currentStep = i;
    toggleOverview(false);
  });
});

// 초기화
update();
