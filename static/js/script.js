/**
 * P. Benarji Rathnam Portfolio — Interactive Client-side Script
 * Vanilla JavaScript (ES6+), zero external dependencies
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNavigation();
  initActiveSectionObserver();
  initContactForm();
  initArchitectureTabs();
  initClipboardButtons();
  initBackToTop();
});

/**
 * 1. Mobile Navigation Toggle
 */
function initMobileNavigation() {
  const toggleBtn = document.getElementById('mobile-nav-toggle');
  const navLinks = document.getElementById('nav-links');

  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
    toggleBtn.setAttribute('aria-expanded', !isExpanded);
    navLinks.classList.toggle('open');
  });

  // Close mobile nav when clicking a link
  navLinks.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!toggleBtn.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
}

/**
 * 2. Active Section Highlighting via IntersectionObserver
 */
function initActiveSectionObserver() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links .nav-link');

  if (!sections.length || !navLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach((link) => {
          const href = link.getAttribute('href');
          if (href === `#${id}` || href.endsWith(`#${id}`)) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));
}

/**
 * 3. Asynchronous Contact Form Submission with Progressive Enhancement
 */
function initContactForm() {
  const form = document.getElementById('contact-form');
  const submitBtn = document.getElementById('contact-submit-btn');
  const formStatus = document.getElementById('form-status');

  if (!form || !submitBtn || !formStatus) return;

  form.addEventListener('submit', async (e) => {
    // If browser supports fetch, handle asynchronously
    if (window.fetch) {
      e.preventDefault();

      // Clear previous alerts
      formStatus.innerHTML = '';
      formStatus.className = '';

      // Client-side quick validation
      const name = form.querySelector('[name="name"]').value.trim();
      const email = form.querySelector('[name="email"]').value.trim();
      const subject = form.querySelector('[name="subject"]').value.trim();
      const message = form.querySelector('[name="message"]').value.trim();
      const csrfToken = form.querySelector('[name="csrf_token"]').value;
      const honeypot = form.querySelector('[name="website"]').value;

      if (!name || name.length < 2) {
        showStatus('Please provide your name (at least 2 characters).', 'error');
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email || !emailRegex.test(email)) {
        showStatus('Please enter a valid email address.', 'error');
        return;
      }

      if (!message || message.length < 10) {
        showStatus('Please enter a message of at least 10 characters.', 'error');
        return;
      }

      // Set loading state
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="spin-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
          <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path>
        </svg>
        Sending Message...
      `;

      try {
        const response = await fetch('/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: JSON.stringify({
            name,
            email,
            subject,
            message,
            csrf_token: csrfToken,
            website: honeypot,
          }),
        });

        const data = await response.json();

        if (response.ok && data.success) {
          showStatus(data.message || 'Message sent successfully!', 'success');
          form.reset();
        } else {
          showStatus(
            data.message || 'Failed to submit message. Please try again.',
            'error'
          );
        }
      } catch (err) {
        showStatus(
          'Network or transmission issue occurred. Please email directly at benarjip69@gmail.com.',
          'error'
        );
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }
  });

  function showStatus(message, type) {
    formStatus.className = `alert alert-${type}`;
    formStatus.innerHTML = `
      <div class="alert-content">
        <span>${message}</span>
      </div>
    `;
    formStatus.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

/**
 * 4. AWS Architecture Interactive View Switcher
 */
function initArchitectureTabs() {
  const tabs = document.querySelectorAll('[data-arch-tab]');
  const views = document.querySelectorAll('[data-arch-view]');

  if (!tabs.length || !views.length) return;

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-arch-tab');

      tabs.forEach((t) => t.classList.remove('active'));
      views.forEach((v) => (v.style.display = 'none'));

      tab.classList.add('active');
      const activeView = document.querySelector(`[data-arch-view="${target}"]`);
      if (activeView) {
        activeView.style.display = 'block';
      }
    });
  });
}

/**
 * 5. Clipboard Copy Utility
 */
function initClipboardButtons() {
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const textToCopy = btn.getAttribute('data-copy');
      if (!textToCopy) return;

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalTitle = btn.getAttribute('title') || 'Copy';
        btn.setAttribute('title', 'Copied to clipboard!');
        btn.classList.add('copied');

        setTimeout(() => {
          btn.setAttribute('title', originalTitle);
          btn.classList.remove('copied');
        }, 2000);
      } catch (e) {
        console.warn('Clipboard copy failed:', e);
      }
    });
  });
}

/**
 * 6. Back-to-Top Button
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById('back-to-top');
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
