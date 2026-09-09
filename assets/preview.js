// Embedded into each standalone preview by tools/prepare-previews.py.
(() => {
  'use strict';
  if (window.parent === window) return;
  const targetOrigin = location.protocol === 'file:' ? '*' : location.origin;
  let scheduled = false;
  let previousHeight = 0;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      if (document.body.getBoundingClientRect().width === 0) return;
      // Measure content, not the iframe viewport, so shorter tabs can shrink.
      const height = Math.ceil(document.body.getBoundingClientRect().height) + 2;
      if (height < 100 || height === previousHeight) return;
      previousHeight = height;
      window.parent.postMessage({type: 'furniture:height', height}, targetOrigin);
    });
  }
  new ResizeObserver(schedule).observe(document.body);
  window.addEventListener('load', schedule);
  window.addEventListener('message', event => {
    if (event.source !== window.parent || event.data?.type !== 'furniture:measure') return;
    if (location.protocol !== 'file:' && event.origin !== location.origin) return;
    previousHeight = 0;
    schedule();
  });
  document.fonts?.ready.then(schedule);
  schedule();
})();
