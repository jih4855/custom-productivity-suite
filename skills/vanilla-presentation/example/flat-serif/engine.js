let currentStep = 0;
const steps = Array.from(document.querySelectorAll('.step'));
const presentation = document.getElementById('presentation');

// 슬라이드(1280×720)를 화면에 맞춰 zoom — 비율 유지하면서 letterbox 처리
function fit() {
  const root = getComputedStyle(document.documentElement);
  const sw = parseFloat(root.getPropertyValue('--slide-w')) || 1280;
  const sh = parseFloat(root.getPropertyValue('--slide-h')) || 720;
  const sx = window.innerWidth / sw;
  const sy = window.innerHeight / sh;
  document.documentElement.style.setProperty('--scale', Math.min(sx, sy));
}
window.addEventListener('resize', fit);
fit();

function update() {
  const activeStep = steps[currentStep];
  if (!activeStep) return;

  // active step의 절대 좌표를 기준으로, 모든 step의 위치를 상대 좌표로 변환한다.
  // 다음 슬라이드(currentStep+1)는 우측, 이전 슬라이드(currentStep-1)는 좌측에 위치하므로
  // next/prev 모두 자연스러운 carousel 모션이 나온다.
  const cx = parseFloat(activeStep.dataset.x) || 0;
  const cy = parseFloat(activeStep.dataset.y) || 0;

  steps.forEach((step, index) => {
    const active = index === currentStep;
    const sx = parseFloat(step.dataset.x) || 0;
    const sy = parseFloat(step.dataset.y) || 0;
    const dx = sx - cx;
    const dy = sy - cy;
    step.style.opacity = active ? '1' : '0';
    step.classList.toggle('active', active);
    step.style.transform = `translate3d(${dx}px, ${dy}px, 0) scale(1)`;
  });
}

function next() {
  if (currentStep < steps.length - 1) {
    currentStep += 1;
    update();
  }
}

function prev() {
  if (currentStep > 0) {
    currentStep -= 1;
    update();
  }
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight') {
    event.preventDefault();
    next();
  }

  if (event.key === 'ArrowLeft') {
    event.preventDefault();
    prev();
  }
});

update();
