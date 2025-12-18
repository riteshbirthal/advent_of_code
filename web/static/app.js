// Minimal JS for interactions: loading state and copy buttons
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('input-form');
  const runBtn = document.getElementById('run-btn');
  const resetBtn = document.getElementById('reset-btn');
  const copyAll = document.getElementById('copy-all');

  if (form && runBtn) {
    form.addEventListener('submit', () => {
      runBtn.disabled = true;
      runBtn.textContent = 'Running...';
      runBtn.classList.add('loading');
    });
  }

  // per-part copy buttons
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const el = document.getElementById(targetId);
      if (!el) return;
      copyText(el.innerText || el.textContent || '');
      btn.textContent = 'Copied';
      setTimeout(() => btn.textContent = 'Copy', 1200);
    });
  });

  if (copyAll) {
    copyAll.addEventListener('click', async () => {
      const p1 = document.getElementById('part1')?.innerText || '';
      const p2 = document.getElementById('part2')?.innerText || '';
      const combined = `Part1:\n${p1}\n\nPart2:\n${p2}`;
      await copyText(combined);
      copyAll.textContent = 'Copied';
      setTimeout(() => copyAll.textContent = 'Copy', 1200);
    });
  }

  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
  }
});