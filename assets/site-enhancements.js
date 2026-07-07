(() => {
  const nav = document.querySelector('nav');
  if (!nav) return;

  const menuButton = nav.querySelector('.mobile-menu-toggle');
  const menu = nav.querySelector('ul');
  const solutionsItem = nav.querySelector('.solutions-item');
  const solutionsButton = nav.querySelector('.solutions-toggle');

  const closeMenu = () => {
    nav.classList.remove('menu-open');
    menuButton?.setAttribute('aria-expanded', 'false');
    solutionsItem?.classList.remove('open');
    solutionsButton?.setAttribute('aria-expanded', 'false');
  };

  menuButton?.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('menu-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });

  solutionsButton?.addEventListener('click', (event) => {
    event.preventDefault();
    const isOpen = solutionsItem.classList.toggle('open');
    solutionsButton.setAttribute('aria-expanded', String(isOpen));
  });

  nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));

  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target)) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeMenu();
      menuButton?.focus();
    }
  });

  const body = document.body;
  const ctaText = body.dataset.mobileCta;
  const ctaTarget = body.dataset.mobileTarget;
  if (ctaText && ctaTarget) {
    const sticky = document.createElement('a');
    sticky.className = 'mobile-sticky-cta';
    sticky.href = ctaTarget;
    sticky.textContent = ctaText;
    sticky.setAttribute('aria-label', ctaText);
    body.appendChild(sticky);
  }

  window.sitePageVisible = !document.hidden;
  document.addEventListener('visibilitychange', () => {
    window.sitePageVisible = !document.hidden;
  });

  if (menu) menu.setAttribute('aria-label', 'Primary navigation');
})();
