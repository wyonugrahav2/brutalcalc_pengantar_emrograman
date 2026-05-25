// ================================================================
// BRUTALCALC — MAIN JAVASCRIPT
// Soviet Constructivist Calculator
// ================================================================

(function () {
    'use strict';

    // ─── THEME MANAGEMENT ────────────────────────────────────────
    const THEME_KEY = 'brutalcalc_theme';

    function getStoredTheme() {
        try { return localStorage.getItem(THEME_KEY) || 'dark'; }
        catch (e) { return 'dark'; }
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        var icon = document.getElementById('themeIcon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '\u263E' : '\u2600';
        }
        try { localStorage.setItem(THEME_KEY, theme); }
        catch (e) { /* ignore */ }
    }

    function toggleTheme() {
        var current = document.documentElement.getAttribute('data-theme') || 'dark';
        setTheme(current === 'dark' ? 'light' : 'dark');
    }

    // Init theme on load
    setTheme(getStoredTheme());

    // Bind toggle button
    document.addEventListener('DOMContentLoaded', function () {
        var toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleTheme);
        }

        // Mark active nav link
        highlightNav();

        // Add keyboard shortcut: Enter key to submit
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                var calcBtn = document.getElementById('calcBtn');
                if (calcBtn && !calcBtn.disabled) {
                    calcBtn.click();
                }
            }
        });
    });

    // ─── NAV HIGHLIGHT ───────────────────────────────────────────
    function highlightNav() {
        var path = window.location.pathname;
        var links = document.querySelectorAll('.nav-link');
        links.forEach(function (link) {
            var href = link.getAttribute('href');
            if (href && (path === href || (path === '/' && href === '/arithmetic'))) {
                link.classList.add('active');
            }
        });
    }

    // ─── UTILITY: FORMAT NUMBER ───────────────────────────────────
    window.formatNum = function (n) {
        if (typeof n === 'number' && !isNaN(n)) {
            return n.toLocaleString('id-ID');
        }
        return String(n);
    };

    // Expose theme functions globally
    window.setTheme = setTheme;
    window.toggleTheme = toggleTheme;

})();
