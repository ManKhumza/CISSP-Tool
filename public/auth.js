/**
 * Auth module for CISSP Study Portal
 * Handles user authentication, token management, and progress sync
 */
const Auth = (function() {
  const API_BASE = '/api';
  let token = null;
  let user = null;
  let syncInterval = null;
  let pendingSync = false;

  // DOM elements
  let authModal = null;
  let loginForm = null;
  let registerForm = null;
  let userMenu = null;
  let userDropdown = null;
  let authButton = null;
  let userEmail = null;
  let logoutBtn = null;

  // Initialize auth
  let initialized = false;
  function init() {
    if (initialized) return;
    initialized = true;
    token = localStorage.getItem('cissp_token');
    const savedUser = localStorage.getItem('cissp_user');
    if (savedUser) user = JSON.parse(savedUser);

    createAuthUI();
    bindEvents();

    if (token) {
      validateToken();
    } else {
      showAuthState(false);
    }
  }

  // Create auth UI elements
  function createAuthUI() {
    // Auth modal
    authModal = document.createElement('div');
    authModal.id = 'authModal';
    authModal.className = 'modal';
    authModal.innerHTML = `
      <div class="modal-content auth-modal">
        <div class="auth-tabs">
          <button class="auth-tab active" data-tab="login">Sign In</button>
          <button class="auth-tab" data-tab="register">Create Account</button>
        </div>
        <form id="loginForm" class="auth-form active">
          <div class="form-group">
            <label for="loginEmail">Email</label>
            <input type="email" id="loginEmail" required autocomplete="email">
          </div>
          <div class="form-group">
            <label for="loginPassword">Password</label>
            <input type="password" id="loginPassword" required autocomplete="current-password">
          </div>
          <button type="submit" class="btn primary">Sign In</button>
          <p class="auth-error" id="loginError"></p>
        </form>
        <form id="registerForm" class="auth-form">
          <div class="form-group">
            <label for="registerEmail">Email</label>
            <input type="email" id="registerEmail" required autocomplete="email">
          </div>
          <div class="form-group">
            <label for="registerPassword">Password</label>
            <input type="password" id="registerPassword" required minlength="8" autocomplete="new-password">
          </div>
          <div class="form-group">
            <label for="registerConfirm">Confirm Password</label>
            <input type="password" id="registerConfirm" required autocomplete="new-password">
          </div>
          <button type="submit" class="btn primary">Create Account</button>
          <p class="auth-error" id="registerError"></p>
        </form>
        <button class="modal-close" aria-label="Close">&times;</button>
      </div>
    `;
    document.body.appendChild(authModal);

    // User menu in topbar
    const topbar = document.getElementById('topbar') || document.querySelector('.topbar');
    if (topbar) {
      userMenu = document.createElement('div');
      userMenu.id = 'userMenu';
      userMenu.className = 'user-menu';
      userMenu.innerHTML = `
        <button id="authButton" class="tb-btn auth-btn" style="display: none;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span id="userEmail"></span>
        </button>
        <div id="userDropdown" class="user-dropdown" style="display: none;">
          <span id="dropdownEmail" class="dropdown-email"></span>
          <hr>
          <button id="syncBtn" class="dropdown-item">Sync Progress Now</button>
          <button id="logoutBtn" class="dropdown-item danger">Sign Out</button>
        </div>
      `;
      // Insert before the theme toggle or at the end of topbar
      const themeBtn = document.getElementById('btnTheme');
      if (themeBtn) {
        topbar.insertBefore(userMenu, themeBtn);
      } else {
        topbar.appendChild(userMenu);
      }
    }

    loginForm = document.getElementById('loginForm');
    registerForm = document.getElementById('registerForm');
    authButton = document.getElementById('authButton');
    userEmail = document.getElementById('userEmail');
    logoutBtn = document.getElementById('logoutBtn');
    userDropdown = document.getElementById('userDropdown');

    // Tab switching
    document.querySelectorAll('.auth-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab + 'Form').classList.add('active');
        clearErrors();
      });
    });

    // Modal close
    authModal.querySelector('.modal-close').addEventListener('click', closeModal);
    authModal.addEventListener('click', e => {
      if (e.target === authModal) closeModal();
    });
  }

  function bindEvents() {
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    authModal.addEventListener('click', e => { if (e.target === authModal) closeModal(); });
    
    if (logoutBtn) logoutBtn.addEventListener('click', logout);
    document.getElementById('syncBtn')?.addEventListener('click', syncProgress);
    
    // Show auth modal / user menu when clicking auth button
    authButton?.addEventListener('click', (e) => {
      e.stopPropagation();
      if (token && user) {
        const dd = userDropdown;
        if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
      } else {
        openModal('login');
      }
    });
    // Close the dropdown when clicking elsewhere
    document.addEventListener('click', (e) => {
      if (userDropdown) {
        const menu = userMenu;
        if (!menu || !menu.contains(e.target)) userDropdown.style.display = 'none';
      }
    });
  }

  // API calls
  async function api(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `HTTP ${res.status}`);
    }
    return data;
  }

  // Auth handlers
  async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');

    try {
      const data = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      setAuth(data.user, data.token);
      closeModal();
      await syncProgress();
      showToast('Welcome back!');
    } catch (err) {
      errorEl.textContent = err.message;
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;
    const confirm = document.getElementById('registerConfirm').value;
    const errorEl = document.getElementById('registerError');

    if (password !== confirm) {
      errorEl.textContent = 'Passwords do not match';
      return;
    }

    try {
      const data = await api('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      setAuth(data.user, data.token);
      closeModal();
      showToast('Account created!');
    } catch (err) {
      errorEl.textContent = err.message;
    }
  }

  function setAuth(userData, tokenData) {
    user = userData;
    token = tokenData;
    localStorage.setItem('cissp_token', token);
    localStorage.setItem('cissp_user', JSON.stringify(user));
    showAuthState(true);
    startSyncInterval();
  }

  function showAuthState(loggedIn) {
    if (!authButton) return;
    if (loggedIn && user) {
      authButton.style.display = 'inline-flex';
      document.getElementById('userEmail').textContent = user.email;
      document.getElementById('dropdownEmail').textContent = user.email;
      if (userDropdown) userDropdown.style.display = 'none';
    } else {
      // Offer a visible "Sign in" entry point when logged out.
      authButton.style.display = 'inline-flex';
      document.getElementById('userEmail').textContent = 'Sign In';
      if (userDropdown) userDropdown.style.display = 'none';
    }
  }

  async function validateToken() {
    try {
      const data = await api('/auth/me');
      user = data.user;
      showAuthState(true);
      startSyncInterval();
    } catch (e) {
      logout(false);
    }
  }

  function logout(sync = true) {
    if (sync && token) {
      syncProgress().catch(console.error);
    }
    token = null;
    user = null;
    localStorage.removeItem('cissp_token');
    localStorage.removeItem('cissp_user');
    stopSyncInterval();
    showAuthState(false);
    closeModal();
    showToast('Signed out');
  }

  // Progress sync
  function portal() {
    return window.__portal;
  }

  function collectLocalProgress() {
    // This integrates with the existing progress system
    const prog = portal()?.progress;
    if (!prog) return { progress: [], sectionProgress: [] };
    
    const progressData = [];
    for (const [qid, ans] of Object.entries(prog.answers || {})) {
      progressData.push({
        questionId: parseInt(qid),
        picked: ans.picked,
        correct: ans.correct ? 1 : 0,
        revealed: prog.revealed?.[qid] ? 1 : 0,
        marked: prog.marks?.[qid] ? 1 : 0
      });
    }

    const sectionProgress = [];
    for (const [sid, sprog] of Object.entries(prog.sections || {})) {
      const match = sid.match(/^(\d+)\.(.+)$/);
      if (match) {
        sectionProgress.push({
          sectionId: sid,
          domainId: parseInt(match[1]),
          answered: sprog.answered || 0,
          correct: sprog.correct || 0,
          marked: sprog.marked || 0,
          lastQuestionIndex: sprog.lastIndex || 0,
          showGuide: sprog.showGuide ? 1 : 0,
          filter: sprog.filter || 'all'
        });
      }
    }
    return { progress: progressData, sectionProgress };
  }

  function applyServerProgress(serverData) {
    const p = portal();
    if (!p || !p.progress) return;

    let changed = false;
    if (serverData.progress) {
      for (const sp of serverData.progress) {
        const qid = sp.question_id;
        // Only adopt the server's answer when this client has not answered yet.
        if (sp.picked && !p.progress.answers[qid]) {
          p.progress.answers[qid] = { picked: sp.picked, correct: !!sp.correct };
          changed = true;
        }
        if (sp.revealed && !p.progress.revealed[qid]) { p.progress.revealed[qid] = true; changed = true; }
        if (sp.marked && !p.progress.marks[qid]) { p.progress.marks[qid] = true; changed = true; }
      }
    }
    if (serverData.sectionProgress) {
      for (const s of serverData.sectionProgress) {
        const sid = s.section_id;
        if (!p.progress.sections[sid]) {
          p.progress.sections[sid] = {};
          changed = true;
        }
        const cur = p.progress.sections[sid];
        if (cur.answered !== undefined) {
          // Keep whichever has attempted more questions.
          if (s.answered > (cur.answered || 0)) {
            Object.assign(cur, {
              answered: s.answered,
              correct: s.correct,
              marked: s.marked,
              lastIndex: s.last_question_index,
              showGuide: !!s.show_guide,
              filter: s.filter
            });
            changed = true;
          }
        }
      }
    }
    if (changed) {
      if (typeof p.saveProgress === 'function') p.saveProgress();
      if (typeof p.refreshSidebar === 'function') p.refreshSidebar();
      if (typeof p.render === 'function') p.render();
    }
  }

  async function syncProgress() {
    if (pendingSync || !token) return;
    pendingSync = true;
    const syncBtn = document.getElementById('syncBtn');
    if (syncBtn) syncBtn.disabled = true;

    try {
      // Pull the server's current state so progress follows across devices.
      const serverState = await api('/progress');
      if (serverState.progress || serverState.sectionProgress) {
        applyServerProgress(serverState);
      }
      // Push the merged local state (server wins on conflicts).
      const localData = collectLocalProgress();
      await api('/progress', {
        method: 'POST',
        body: JSON.stringify(localData)
      });
      showToast('Progress synced');
    } catch (err) {
      console.error('Sync failed:', err);
      showToast('Sync failed: ' + err.message, 'error');
    } finally {
      pendingSync = false;
      if (syncBtn) syncBtn.disabled = false;
    }
  }

  function startSyncInterval() {
    if (syncInterval) return;
    // Initial sync
    syncProgress();
    // Periodic sync every 2 minutes
    syncInterval = setInterval(syncProgress, 2 * 60 * 1000);
  }

  function stopSyncInterval() {
    if (syncInterval) {
      clearInterval(syncInterval);
      syncInterval = null;
    }
  }

  // UI helpers
  function openModal(tab = 'login') {
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    document.querySelector(`.auth-tab[data-tab="${tab}"]`)?.classList.add('active');
    document.getElementById(`${tab}Form`)?.classList.add('active');
    clearErrors();
    authModal.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => document.getElementById(tab === 'login' ? 'loginEmail' : 'registerEmail')?.focus(), 100);
  }

  function closeModal() {
    authModal.classList.remove('open');
    document.body.style.overflow = '';
    clearErrors();
  }

  function clearErrors() {
    document.getElementById('loginError').textContent = '';
    document.getElementById('registerError').textContent = '';
  }

  function showToast(message, type = 'success') {
    // Reuse existing toast if available
    if (typeof toast === 'function') {
      toast(message);
    } else {
      const el = document.createElement('div');
      el.className = `toast ${type}`;
      el.textContent = message;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 3000);
    }
  }

  // Public API
  return {
    init,
    getUser: () => user,
    isLoggedIn: () => !!token,
    sync: syncProgress,
    logout,
    openModal: (tab) => openModal(tab)
  };
})();

// Auto-init when DOM ready
document.addEventListener('DOMContentLoaded', () => Auth.init());

// Export for global access
window.Auth = Auth;