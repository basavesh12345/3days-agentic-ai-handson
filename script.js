// ================================================================
//  Agentic AI Workshop — Interactive JS
// ================================================================

/* ── Scroll Reveal ── */
function initScrollReveal() {
  const targets = document.querySelectorAll(
    '.outcome-card, .session-card, .tool-card, .timeline-item, .day-block'
  );
  targets.forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add('visible'), i * 60);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );
  targets.forEach(el => observer.observe(el));
}

/* ── Active Nav Highlight ── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

/* ── Session Card Tilt Effect ── */
function initTilt() {
  document.querySelectorAll('.session-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const dx = (x - cx) / cx;
      const dy = (y - cy) / cy;
      card.style.transform = `translateY(-4px) rotateX(${-dy * 3}deg) rotateY(${dx * 3}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}

/* ── Stat Counter Animation ── */
function animateCounter(el, target, duration = 1200) {
  const start = performance.now();
  const isPercent = String(target).includes('%');
  const numTarget = parseInt(target);

  const tick = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * numTarget);
    el.textContent = isPercent ? current + '%' : current + (target.includes('+') ? '+' : '');
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function initCounters() {
  const statNums = document.querySelectorAll('.stat-num');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const raw = el.textContent.trim();
        animateCounter(el, raw);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  statNums.forEach(el => observer.observe(el));
}

/* ── Particle Canvas ── */
function initParticles() {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;pointer-events:none;opacity:0.35;z-index:1;';
  hero.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width = hero.clientWidth;
    H = canvas.height = hero.clientHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  const colors = ['#6366f1', '#a855f7', '#22d3ee', '#ec4899'];
  for (let i = 0; i < 55; i++) {
    particles.push({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 2 + 0.5,
      dx: (Math.random() - 0.5) * 0.4,
      dy: (Math.random() - 0.5) * 0.4,
      color: colors[Math.floor(Math.random() * colors.length)],
    });
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if (p.x < 0 || p.x > W) p.dx *= -1;
      if (p.y < 0 || p.y > H) p.dy *= -1;
    });

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 110) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(99,102,241,${0.15 * (1 - dist / 110)})`;
          ctx.lineWidth = 0.6;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
}

/* ── Tool Card Hover Glow ── */
function initToolGlow() {
  document.querySelectorAll('.tool-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.boxShadow = '0 0 30px rgba(99,102,241,0.35), 0 8px 20px rgba(0,0,0,0.4)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.boxShadow = '';
    });
  });
}

/* ── Project Choice Interaction ── */
function initProjectChoices() {
  document.querySelectorAll('.project-choice').forEach(pc => {
    pc.addEventListener('click', () => {
      document.querySelectorAll('.project-choice').forEach(p => {
        p.style.background = '';
        p.style.borderColor = '';
        p.style.color = '';
      });
      pc.style.background = 'rgba(99,102,241,0.22)';
      pc.style.borderColor = 'rgba(99,102,241,0.55)';
      pc.style.color = '#e0e7ff';
    });
  });
}

/* ── Floating Header ── */
function initFloatingBadges() {
  const badges = document.querySelectorAll('.badge');
  badges.forEach((badge, i) => {
    badge.style.animationDelay = `${i * 0.15}s`;
  });
}

/* ── Day Header Hover ── */
function initDayHeaders() {
  const headers = [
    { el: document.querySelector('.day-header-1'), grad: 'rgba(59,130,246,0.35)' },
    { el: document.querySelector('.day-header-2'), grad: 'rgba(168,85,247,0.35)' },
    { el: document.querySelector('.day-header-3'), grad: 'rgba(245,158,11,0.35)' },
  ];
  headers.forEach(({ el, grad }) => {
    if (!el) return;
    el.addEventListener('mouseenter', () => el.style.boxShadow = `0 4px 30px ${grad}`);
    el.addEventListener('mouseleave', () => el.style.boxShadow = '');
  });
}

/* ── Theme Toggle Switch ── */
function initThemeToggle() {
  const getSavedTheme = () => localStorage.getItem('theme') || 'dark';
  const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.textContent = theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    });
  };

  applyTheme(getSavedTheme());

  document.body.addEventListener('click', (e) => {
    if (e.target && e.target.classList.contains('theme-toggle-btn')) {
      const newTheme = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', newTheme);
      applyTheme(newTheme);
    }
  });
}

/* ── Copy Code Global Delegation ── */
function initCopyCode() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.copy-btn');
    if (!btn) return;
    const wrapper = btn.closest('.code-block-wrapper');
    if (!wrapper) return;
    const code = wrapper.querySelector('code');
    if (!code) return;
    navigator.clipboard.writeText(code.innerText).then(() => {
      const origText = btn.textContent;
      btn.textContent = '✅ Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = origText;
        btn.classList.remove('copied');
      }, 2000);
    }).catch(err => console.error('Copy failed:', err));
  });
}

function copyCode(btn) {
  // Global fallback handler for explicit inline onClick calls
  const wrapper = btn.closest('.code-block-wrapper');
  if (!wrapper) return;
  const code = wrapper.querySelector('code');
  if (!code) return;
  navigator.clipboard.writeText(code.innerText).then(() => {
    const origText = btn.textContent;
    btn.textContent = '✅ Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = origText;
      btn.classList.remove('copied');
    }, 2000);
  });
}

/* ── Init All ── */
document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initCopyCode();
  initScrollReveal();
  initSmoothScroll();
  initTilt();
  initCounters();
  initParticles();
  initToolGlow();
  initProjectChoices();
  initFloatingBadges();
  initDayHeaders();

  // Console greeting
  console.log('%c🤖 Agentic AI Workshop', 'color:#a855f7;font-size:18px;font-weight:bold;');
  console.log('%cBuilt with passion for 5th Sem CSE students 🚀', 'color:#6366f1;font-size:13px;');
});
