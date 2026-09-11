(() => {
  'use strict';
  const picker = document.querySelector('.view-picker');
  const buttons = [...picker.querySelectorAll('button[data-view]')];
  const views = [...document.querySelectorAll('.room-view')];
  function selectView(button) {
    for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
    for (const view of views) view.hidden = view.id !== button.getAttribute('aria-controls');
  }
  picker.hidden = false;
  document.querySelector('.drawing-tools').hidden = false;
  document.getElementById('drawing-zoom').addEventListener('change', event => {
    const scale = Number(event.target.value);
    document.documentElement.style.setProperty('--drawing-scale', scale);
    document.body.classList.toggle('is-zoomed', scale > 1);
  });
  document.getElementById('print-drawings').addEventListener('click', () => window.print());
  buttons.forEach(button => button.addEventListener('click', () => selectView(button)));
  selectView(buttons[0]);
})();
