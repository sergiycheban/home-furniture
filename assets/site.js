(() => {
  'use strict';
  const tabs = [...document.querySelectorAll('.room-tabs [role="tab"]')];
  const frames = [...document.querySelectorAll('iframe[data-room]')];
  const status = document.getElementById('load-status');
  const standalone = document.getElementById('standalone-link');
  let activeRoom;
  let slowTimer;
  const targetOrigin = location.protocol === 'file:' ? '*' : location.origin;

  function selectRoom(room, focus = false) {
    const selected = tabs.find(tab => tab.dataset.room === room) || tabs[0];
    activeRoom = selected.dataset.room;
    for (const tab of tabs) {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    }
    if (focus) selected.focus();
    const frame = frames.find(item => item.dataset.room === activeRoom);
    standalone.href = frame.dataset.src;
    standalone.setAttribute('aria-label', `Открыть отдельно: ${selected.textContent.slice(2).trim()}`);
    document.title = `${selected.textContent.slice(2).trim()} — Мебель для дома`;
    status.textContent = frame.dataset.ready ? '' : 'Загружается проект…';
    clearTimeout(slowTimer);
    if (!frame.hasAttribute('src')) frame.src = frame.dataset.src;
    frame.contentWindow?.postMessage({type: 'furniture:measure'}, targetOrigin);
    if (!frame.dataset.ready) {
      slowTimer = setTimeout(() => {
        if (!frame.dataset.ready && frame.dataset.room === activeRoom) {
          status.textContent = 'Страница не загрузилась. Попробуйте открыть её отдельно.';
        }
      }, 8000);
    }
  }

  function navigate(tab) {
    if (location.hash === '#' + tab.dataset.room) selectRoom(tab.dataset.room);
    else location.hash = tab.dataset.room;
  }
  tabs.forEach(tab => tab.addEventListener('click', () => navigate(tab)));
  document.querySelector('.room-tabs').addEventListener('keydown', event => {
    const current = tabs.indexOf(event.target);
    if (current < 0) return;
    let next;
    if (event.key === 'ArrowRight') next = (current + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (current + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    tabs[next].focus();
    navigate(tabs[next]);
  });
  window.addEventListener('hashchange', () => selectRoom(location.hash.slice(1)));
  window.addEventListener('message', event => {
    const frame = frames.find(item => item.contentWindow === event.source);
    if (!frame || (location.protocol !== 'file:' && event.origin !== location.origin)) return;
    if (event.data?.type !== 'furniture:height') return;
    const height = event.data.height;
    if (!Number.isFinite(height) || height < 100 || height > 50000) return;
    frame.style.height = Math.ceil(height) + 'px';
    frame.dataset.ready = 'true';
    if (frame.dataset.room === activeRoom) {
      status.textContent = '';
      clearTimeout(slowTimer);
    }
  });
  selectRoom(location.hash.slice(1));
})();
