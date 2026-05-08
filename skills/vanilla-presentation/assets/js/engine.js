let currentStep = 0;
const steps = Array.from(document.querySelectorAll('.step'));
const presentation = document.getElementById('presentation');

function update() {
  const activeStep = steps[currentStep];
  if (!activeStep) return;

  const x = parseFloat(activeStep.getAttribute('data-x'));
  const y = parseFloat(activeStep.getAttribute('data-y'));

  presentation.style.transform = `translate(${-x}px, ${-y}px)`;

  steps.forEach((step, index) => {
    const active = index === currentStep;
    step.style.opacity = active ? '1' : '0';
    step.classList.toggle('active', active);
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
