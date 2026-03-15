def get_dashboard_html() -> str:
    return '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>dnsboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root, [data-theme="dark"] {
    --bg: #0a0a0a;
    --card: #1a1a1a;
    --card-border: #2a2a2a;
    --card-hover: #222;
    --green: #4ade80;
    --green-dim: rgba(74, 222, 128, 0.15);
    --amber: #f59e0b;
    --amber-dim: rgba(245, 158, 11, 0.15);
    --red: #ef4444;
    --red-dim: rgba(239, 68, 68, 0.15);
    --text: #e5e5e5;
    --text-muted: #a3a3a3;
    --text-dim: #666;
    --chart-bg: #111;
    --chart-grid: #222;
    --chart-line: #4ade80;
    --chart-fill: rgba(74, 222, 128, 0.08);
    --chart-dot: #4ade80;
    --input-bg: #161616;
    --mono: 'Courier New', 'Consolas', monospace;
}

[data-theme="light"] {
    --bg: #f5f5f5;
    --card: #ffffff;
    --card-border: #e0e0e0;
    --card-hover: #fafafa;
    --green: #16a34a;
    --green-dim: rgba(22, 163, 74, 0.1);
    --amber: #d97706;
    --amber-dim: rgba(217, 119, 6, 0.1);
    --red: #dc2626;
    --red-dim: rgba(220, 38, 38, 0.1);
    --text: #1a1a1a;
    --text-muted: #666;
    --text-dim: #999;
    --chart-bg: #fafafa;
    --chart-grid: #e8e8e8;
    --chart-line: #16a34a;
    --chart-fill: rgba(22, 163, 74, 0.06);
    --chart-dot: #16a34a;
    --input-bg: #f0f0f0;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    padding: 40px 20px;
    transition: background 0.3s, color 0.3s;
}

.container { max-width: 900px; margin: 0 auto; }

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--card-border);
    flex-wrap: wrap;
    gap: 12px;
}

.header-left { display: flex; align-items: baseline; gap: 16px; }

h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: -0.02em;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.last-updated {
    font-size: 0.78rem;
    color: var(--text-dim);
    animation: pulse-text 3s ease-in-out infinite;
}

@keyframes pulse-text {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* Search */
.search-bar {
    margin-bottom: 24px;
}

.search-input {
    width: 100%;
    background: var(--input-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    color: var(--text);
    outline: none;
    transition: border-color 0.2s;
}

.search-input::placeholder { color: var(--text-dim); }
.search-input:focus { border-color: var(--text-muted); }

/* Theme toggle */
.theme-toggle {
    background: none;
    border: 1px solid var(--card-border);
    color: var(--text-muted);
    width: 32px;
    height: 32px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    transition: all 0.2s;
}

.theme-toggle:hover { border-color: var(--text-muted); color: var(--text); }

/* Loading */
.loading {
    text-align: center;
    padding: 80px 0;
    color: var(--text-muted);
    font-size: 1.1rem;
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid var(--card-border);
    border-top-color: var(--text-muted);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-right: 10px;
    vertical-align: middle;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    margin-bottom: 24px;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeIn 0.5s ease forwards;
    overflow: hidden;
    transition: background 0.3s, border-color 0.3s;
}

.card.hidden { display: none; }

@keyframes fadeIn {
    to { opacity: 1; transform: translateY(0); }
}

.card.alert-down { border-left: 3px solid var(--red); }
.card.alert-ssl { border-left: 3px solid var(--amber); }
.card.alert-whois { border-left: 3px solid var(--amber); }

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 28px;
    cursor: pointer;
    user-select: none;
    transition: background 0.15s;
}

.card-header:hover { background: var(--card-hover); }

.card-collapse-icon {
    font-size: 0.6rem;
    color: var(--text-dim);
    transition: transform 0.25s ease;
    flex-shrink: 0;
}

.card.collapsed .card-collapse-icon { transform: rotate(-90deg); }

.domain-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    font-weight: 400;
    flex: 1;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

.status-dot.up {
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    animation: pulse-green 2s ease-in-out infinite;
}

.status-dot.down {
    background: var(--red);
    box-shadow: 0 0 6px var(--red);
    animation: pulse-red 1.5s ease-in-out infinite;
}

.status-dot.unknown { background: var(--text-dim); }

@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 4px var(--green); }
    50% { box-shadow: 0 0 12px var(--green); }
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 4px var(--red); }
    50% { box-shadow: 0 0 14px var(--red); }
}

.status-text {
    font-size: 0.85rem;
    color: var(--text-muted);
    font-family: var(--mono);
}

.card-body {
    padding: 0 28px 28px;
    max-height: 2000px;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.4s ease, opacity 0.3s ease;
    opacity: 1;
}

.card.collapsed .card-body {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    opacity: 0;
}

/* Two-column row */
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

@media (max-width: 700px) {
    .two-col { grid-template-columns: 1fr; }
}

.two-col > .section { margin-bottom: 0; }

/* Sections */
.section { margin-bottom: 20px; }
.section:last-child { margin-bottom: 0; }

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim);
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--card-border);
}

.data-grid {
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 6px 16px;
}

.data-label {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.data-value {
    font-size: 0.85rem;
    font-family: var(--mono);
    word-break: break-all;
}

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: var(--mono);
}

.badge.up { background: var(--green-dim); color: var(--green); }
.badge.down { background: var(--red-dim); color: var(--red); }
.badge.warn { background: var(--amber-dim); color: var(--amber); }
.badge.ok { background: var(--green-dim); color: var(--green); }

.error-msg {
    color: var(--text-dim);
    font-size: 0.85rem;
    font-style: italic;
}

/* Response time chart */
.chart-container {
    margin-top: 12px;
    background: var(--chart-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 16px;
    position: relative;
}

.chart-container canvas {
    width: 100%;
    height: 120px;
    display: block;
}

.chart-label {
    font-size: 0.7rem;
    color: var(--text-dim);
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
}

.chart-label .chart-value {
    font-family: var(--mono);
    color: var(--chart-line);
    font-weight: 600;
}

/* DNS Details */
details.dns-details { margin-top: 4px; }

details.dns-details summary {
    cursor: pointer;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim);
    padding-bottom: 6px;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 10px;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 6px;
}

details.dns-details summary::before {
    content: '\\25B6';
    font-size: 0.55rem;
    transition: transform 0.2s;
}

details.dns-details[open] summary::before { transform: rotate(90deg); }

.dns-group { margin-bottom: 12px; }

.dns-type {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    font-family: var(--mono);
    color: var(--text-muted);
    background: rgba(128,128,128,0.1);
    padding: 2px 6px;
    border-radius: 3px;
    margin-bottom: 4px;
    min-width: 50px;
    text-align: center;
}

.dns-value {
    font-size: 0.8rem;
    font-family: var(--mono);
    color: var(--text);
    padding: 2px 0 2px 12px;
}

/* Propagation */
.prop-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 0;
    font-size: 0.8rem;
    border-bottom: 1px solid rgba(128,128,128,0.06);
}

.prop-row:last-of-type { border-bottom: none; }

.prop-logo {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.prop-logo svg { width: 16px; height: 16px; }

.prop-resolver {
    min-width: 72px;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.78rem;
}

.prop-records {
    font-family: var(--mono);
    font-size: 0.75rem;
    flex: 1;
    color: var(--text);
}

.prop-status-badge {
    flex-shrink: 0;
}

.prop-consistent {
    margin-top: 6px;
    padding: 5px 8px;
    font-size: 0.72rem;
    font-weight: 500;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.prop-consistent.ok {
    background: var(--green-dim);
    color: var(--green);
}

.prop-consistent.warn {
    background: var(--amber-dim);
    color: var(--amber);
}

.prop-loading {
    color: var(--text-dim);
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.prop-loading .loading-spinner {
    width: 14px;
    height: 14px;
    border-width: 1.5px;
    margin-right: 0;
}

/* Buttons */
.refresh-btn {
    background: none;
    border: 1px solid var(--card-border);
    color: var(--text-muted);
    padding: 4px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.75rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
}

.refresh-btn:hover { border-color: var(--text-muted); color: var(--text); }

/* Toast */
.toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 0.85rem;
    color: var(--text-muted);
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
    pointer-events: none;
    z-index: 100;
}

.toast.visible { opacity: 1; transform: translateY(0); }

/* Ping log */
.ping-log {
    max-height: 140px;
    overflow-y: auto;
    margin-top: 8px;
    scrollbar-width: thin;
    scrollbar-color: var(--card-border) transparent;
}

.ping-entry {
    display: flex;
    gap: 12px;
    padding: 3px 0;
    font-size: 0.78rem;
    font-family: var(--mono);
    border-bottom: 1px solid rgba(128,128,128,0.05);
}

.ping-entry .time { color: var(--text-dim); min-width: 70px; }
.ping-entry .code { min-width: 36px; }
.ping-entry .ms { color: var(--text-muted); min-width: 70px; text-align: right; }
</style>
</head>
<body>
<div class="container">
    <header>
        <div class="header-left">
            <h1>dnsboard</h1>
        </div>
        <div class="header-right">
            <button class="refresh-btn" onclick="refreshAll()">Refresh All</button>
            <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme" id="themeBtn">&#9790;</button>
            <span class="last-updated" id="lastUpdated">loading...</span>
        </div>
    </header>
    <div class="search-bar">
        <input type="text" class="search-input" id="searchInput" placeholder="Filter domains..." oninput="filterDomains()">
    </div>
    <div id="domains">
        <div class="loading"><span class="loading-spinner"></span>Fetching domain data...</div>
    </div>
</div>
<div class="toast" id="toast"></div>

<script>
const pingHistory = {};
const chartData = {};
let lastData = null;
let pollTimer = null;
let pingTimer = null;
const collapsedState = {};

// Theme
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('dnsboard-theme', next);
    document.getElementById('themeBtn').innerHTML = next === 'dark' ? '&#9790;' : '&#9788;';
    // Redraw charts with new theme colors
    Object.keys(chartData).forEach(domain => drawChart(domain));
}

(function initTheme() {
    const saved = localStorage.getItem('dnsboard-theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
        if (saved === 'light') document.getElementById('themeBtn').innerHTML = '&#9788;';
    }
})();

// Search / Filter
function filterDomains() {
    const q = document.getElementById('searchInput').value.toLowerCase().trim();
    document.querySelectorAll('.card[data-domain]').forEach(card => {
        const domain = card.dataset.domain.toLowerCase();
        card.classList.toggle('hidden', q && !domain.includes(q));
    });
}

// Collapse
function toggleCard(domain) {
    const card = document.querySelector(`.card[data-domain="${domain}"]`);
    if (!card) return;
    card.classList.toggle('collapsed');
    collapsedState[domain] = card.classList.contains('collapsed');
}

// Data fetching
async function fetchData() {
    try {
        const res = await fetch('/api/data');
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        lastData = data;
        renderDomains(data);
        updateTimestamp();
        hideToast();
    } catch (e) {
        showToast('Connection lost, retrying...');
    }
}

async function fetchPings() {
    try {
        const res = await fetch('/api/ping');
        if (!res.ok) return;
        const data = await res.json();
        const domains = data._meta ? data._meta.domains : [];
        domains.forEach(domain => {
            const p = data[domain];
            if (!p) return;

            // Update ping history
            if (p.timestamp) {
                if (!pingHistory[domain]) pingHistory[domain] = [];
                const last = pingHistory[domain][pingHistory[domain].length - 1];
                if (!last || last.timestamp !== p.timestamp) {
                    pingHistory[domain].push(p);
                    if (pingHistory[domain].length > 60) pingHistory[domain].shift();
                }
            }

            // Update chart data
            if (p.response_time_ms != null) {
                if (!chartData[domain]) chartData[domain] = [];
                chartData[domain].push({
                    time: new Date(p.timestamp),
                    ms: p.response_time_ms,
                    up: p.is_up
                });
                if (chartData[domain].length > 60) chartData[domain].shift();
                drawChart(domain);
            }

            // Update status elements in-place
            updateCardStatus(domain, p);
        });
        updateTimestamp();
    } catch (e) { /* silent */ }
}

function updateCardStatus(domain, p) {
    const card = document.querySelector(`.card[data-domain="${domain}"]`);
    if (!card) return;

    const dot = card.querySelector('.status-dot');
    if (dot) {
        dot.className = 'status-dot ' + (p.is_up ? 'up' : (p.is_up === false ? 'down' : 'unknown'));
    }

    const statusText = card.querySelector('.status-text');
    if (statusText) {
        statusText.textContent = p.error ? p.error : `${p.status_code} \\u00b7 ${p.response_time_ms}ms`;
    }

    // Update ping log
    const logEl = card.querySelector('.ping-log');
    if (logEl) {
        const pings = pingHistory[domain] || [];
        let html = '';
        for (let i = pings.length - 1; i >= Math.max(0, pings.length - 20); i--) {
            const pg = pings[i];
            const t = new Date(pg.timestamp).toLocaleTimeString();
            const codeClass = pg.is_up ? 'up' : 'down';
            const ms = pg.response_time_ms != null ? pg.response_time_ms + 'ms' : '\\u2014';
            const code = pg.status_code || '\\u2014';
            html += `<div class="ping-entry"><span class="time">${t}</span><span class="code">${badge(code, codeClass)}</span><span class="ms">${ms}</span></div>`;
        }
        logEl.innerHTML = html;
    }
}

async function refreshAll() {
    showToast('Refreshing all data...');
    try {
        const res = await fetch('/api/refresh', { method: 'POST' });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        lastData = data;
        renderDomains(data);
        updateTimestamp();
        hideToast();
    } catch (e) {
        showToast('Refresh failed');
    }
}

function updateTimestamp() {
    document.getElementById('lastUpdated').textContent = 'updated ' + new Date().toLocaleTimeString();
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('visible');
}

function hideToast() {
    document.getElementById('toast').classList.remove('visible');
}

// DNS Propagation - Provider logos (inline SVGs)
const RESOLVER_LOGOS = {
    Google: '<svg viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>',
    Cloudflare: '<svg viewBox="0 0 24 24"><path fill="#F6821F" d="M16.51 17.65l-.28-1.15c-.07-.28-.05-.54.06-.76s.31-.38.56-.46l6.36-2.17c.11-.04.2-.11.24-.2s.06-.2.04-.3a6.92 6.92 0 0 0-6.76-5.34c-2.83 0-5.26 1.7-6.34 4.13a3.41 3.41 0 0 0-2.7-.67 3.48 3.48 0 0 0-2.42 1.85A4.84 4.84 0 0 0 0 17.18a.4.4 0 0 0 .39.42h15.73c.12 0 .23-.04.3-.12a.39.39 0 0 0 .09-.31z"/><path fill="#FAAD3F" d="M19.35 12.77c-.07 0-.14 0-.2.01l-.26 1.01c-.07.28-.05.54.06.76s.31.38.56.46l1.48.5c.11.04.2.11.24.2s.06.2.04.3c-.19.86-.57 1.62-1.08 2.26a.32.32 0 0 1-.28.12.34.34 0 0 1-.09 0H19.7c-.03-.01-.05-.01-.07-.02a3.35 3.35 0 0 0-.28-7.6z"/></svg>',
    Quad9: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="none" stroke="#2C6FBA" stroke-width="2"/><text x="12" y="16.5" text-anchor="middle" fill="#2C6FBA" font-family="Inter,sans-serif" font-weight="700" font-size="13">9</text></svg>',
    OpenDNS: '<svg viewBox="0 0 24 24"><path fill="#F37C20" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.1 0 2 .9 2 2v3.17a3 3 0 1 1-4 0V7c0-1.1.9-2 2-2z"/><circle cx="12" cy="14" r="1.5" fill="#fff"/></svg>',
    AdGuard: '<svg viewBox="0 0 24 24"><path fill="#66B574" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 3.18L18 7.3v3.7c0 4.28-2.88 8.3-6 9.82-3.12-1.52-6-5.54-6-9.82V7.3L12 4.18z"/><path fill="#66B574" d="M12 6.5L7 8.7v2.3c0 3.13 2.13 6.08 5 7.1 2.87-1.02 5-3.97 5-7.1V8.7L12 6.5z" opacity="0.3"/></svg>'
};

function buildPropagationContent(propData) {
    if (!propData || propData.error) {
        return '<span class="error-msg">Propagation data unavailable</span>';
    }
    if (!Array.isArray(propData) || propData.length === 0) {
        return '<div class="prop-loading"><span class="loading-spinner"></span>Loading...</div>';
    }
    let html = '';
    propData.forEach(r => {
        const isOk = r.status === 'ok' && r.records.length > 0;
        const logo = RESOLVER_LOGOS[r.resolver] || '';
        html += `<div class="prop-row">
            <span class="prop-logo">${logo}</span>
            <span class="prop-resolver">${esc(r.resolver)}</span>
            <span class="prop-records">${isOk ? r.records.map(x => esc(x)).join(', ') : esc(r.status)}</span>
            <span class="prop-status-badge">${isOk ? badge('\\u2713', 'up') : badge('\\u2717', 'down')}</span>
        </div>`;
    });
    const consistent = propData.length > 0 && propData[0].consistent;
    html += `<div class="prop-consistent ${consistent ? 'ok' : 'warn'}">
        ${consistent ? '\\u2713 Consistent' : '\\u26a0 Inconsistent'}
    </div>`;
    return html;
}

// Render
function renderDomains(data) {
    const container = document.getElementById('domains');
    const domains = data._meta ? data._meta.domains : Object.keys(data).filter(k => k !== '_meta');

    if (!domains.length) {
        container.innerHTML = '<div class="loading">No domains to display</div>';
        return;
    }

    const existingCards = {};
    container.querySelectorAll('.card').forEach(c => { existingCards[c.dataset.domain] = c; });

    const fragment = document.createDocumentFragment();
    domains.forEach((domain, idx) => {
        const d = data[domain];
        if (!d) return;

        // Init ping/chart history
        if (d.ping && d.ping.timestamp) {
            if (!pingHistory[domain]) pingHistory[domain] = [];
            const last = pingHistory[domain][pingHistory[domain].length - 1];
            if (!last || last.timestamp !== d.ping.timestamp) {
                pingHistory[domain].push(d.ping);
                if (pingHistory[domain].length > 60) pingHistory[domain].shift();
            }
            if (d.ping.response_time_ms != null) {
                if (!chartData[domain]) chartData[domain] = [];
                chartData[domain].push({
                    time: new Date(d.ping.timestamp),
                    ms: d.ping.response_time_ms,
                    up: d.ping.is_up
                });
                if (chartData[domain].length > 60) chartData[domain].shift();
            }
        }

        const isUp = d.ping && d.ping.is_up;
        const isDown = d.ping && d.ping.is_up === false;
        const sslWarn = d.ssl && d.ssl.days_until_expiry != null && d.ssl.days_until_expiry < 30 && !d.ssl.error;
        const whoisWarn = d.whois && d.whois.days_until_expiry != null && d.whois.days_until_expiry < 60 && !d.whois.error;

        let alertClass = '';
        if (isDown) alertClass = ' alert-down';
        else if (sslWarn) alertClass = ' alert-ssl';
        else if (whoisWarn) alertClass = ' alert-whois';

        const existing = existingCards[domain];
        const card = existing || document.createElement('div');
        const isCollapsed = collapsedState[domain] || false;

        if (!existing) {
            card.className = 'card' + alertClass + (isCollapsed ? ' collapsed' : '');
            card.dataset.domain = domain;
            card.style.animationDelay = (idx * 0.1) + 's';
        } else {
            const baseClass = 'card' + alertClass + (isCollapsed ? ' collapsed' : '');
            card.className = baseClass;
            card.style.animationDelay = '0s';
            card.style.opacity = '1';
            card.style.transform = 'none';
        }

        card.innerHTML = buildCardContent(domain, d, isUp, isDown, sslWarn, whoisWarn);
        if (!existing) fragment.appendChild(card);
        delete existingCards[domain];
    });

    Object.values(existingCards).forEach(c => c.remove());

    if (!container.querySelector('.card')) container.innerHTML = '';
    container.appendChild(fragment);

    // Draw charts after DOM is ready
    domains.forEach(domain => { if (chartData[domain]) drawChart(domain); });

    // Reapply search filter
    filterDomains();
}

function buildCardContent(domain, d, isUp, isDown, sslWarn, whoisWarn) {
    let html = '';
    const domId = domain.replace(/\\./g, '-');

    // Header (clickable to collapse)
    const dotClass = isUp ? 'up' : (isDown ? 'down' : 'unknown');
    const statusText = d.ping
        ? (d.ping.error ? d.ping.error : `${d.ping.status_code} \\u00b7 ${d.ping.response_time_ms}ms`)
        : '';
    html += `<div class="card-header" onclick="toggleCard('${esc(domain)}')">
        <span class="card-collapse-icon">\\u25BC</span>
        <span class="status-dot ${dotClass}"></span>
        <span class="domain-name">${esc(domain)}</span>
        <span class="status-text">${esc(statusText)}</span>
    </div>`;

    html += '<div class="card-body">';

    // Response time chart
    html += `<div class="section">
        <div class="chart-container">
            <div class="chart-label">
                <span>Response Time</span>
                <span class="chart-value" id="chart-val-${domId}">${d.ping && d.ping.response_time_ms != null ? d.ping.response_time_ms + ' ms' : '\\u2014'}</span>
            </div>
            <canvas id="chart-${domId}" height="120"></canvas>
        </div>
    </div>`;

    // Two-column: Status + DNS Propagation
    html += '<div class="two-col">';

    // Left: Status
    html += '<div class="section">';
    html += '<div class="section-title">Status</div>';
    if (d.ping && !d.ping.error) {
        html += '<div class="data-grid">';
        html += row('Status', isUp ? badge('UP', 'up') : badge('DOWN', 'down'));
        html += row('Status Code', d.ping.status_code);
        html += row('Response Time', d.ping.response_time_ms + ' ms');
        html += row('URL', d.ping.url);
        html += '</div>';
    } else if (d.ping && d.ping.error) {
        html += '<div class="data-grid">';
        html += row('Status', badge('DOWN', 'down'));
        html += row('Error', `<span class="error-msg">${esc(d.ping.error)}</span>`);
        html += '</div>';
    }

    // Ping log
    const pings = pingHistory[domain] || [];
    html += '<div class="ping-log">';
    for (let i = pings.length - 1; i >= Math.max(0, pings.length - 20); i--) {
        const p = pings[i];
        const t = new Date(p.timestamp).toLocaleTimeString();
        const codeClass = p.is_up ? 'up' : 'down';
        const ms = p.response_time_ms != null ? p.response_time_ms + 'ms' : '\\u2014';
        const code = p.status_code || '\\u2014';
        html += `<div class="ping-entry"><span class="time">${t}</span><span class="code">${badge(code, codeClass)}</span><span class="ms">${ms}</span></div>`;
    }
    html += '</div>';
    html += '</div>';

    // Right: DNS Propagation
    html += '<div class="section">';
    html += '<div class="section-title">DNS Propagation</div>';
    html += buildPropagationContent(d.propagation);
    html += '</div>';

    html += '</div>'; // end two-col

    // SSL
    html += '<div class="section">';
    html += '<div class="section-title">SSL Certificate</div>';
    if (d.ssl && !d.ssl.error) {
        const daysClass = d.ssl.days_until_expiry < 7 ? 'down' : (d.ssl.days_until_expiry < 30 ? 'warn' : 'ok');
        html += '<div class="data-grid">';
        html += row('Issuer', d.ssl.issuer);
        html += row('Subject', d.ssl.subject);
        html += row('Valid From', formatDate(d.ssl.valid_from));
        html += row('Valid To', formatDate(d.ssl.valid_to));
        html += row('Expires In', badge(d.ssl.days_until_expiry + ' days', daysClass));
        html += '</div>';
    } else {
        html += `<span class="error-msg">${esc(d.ssl ? d.ssl.error : 'No data')}</span>`;
    }
    html += '</div>';

    // WHOIS
    html += '<div class="section">';
    html += '<div class="section-title">WHOIS</div>';
    if (d.whois && !d.whois.error) {
        html += '<div class="data-grid">';
        html += row('Registrar', d.whois.registrar || '\\u2014');
        html += row('Created', formatDate(d.whois.creation_date));
        html += row('Updated', formatDate(d.whois.updated_date));
        html += row('Expires', formatDate(d.whois.expiration_date));
        if (d.whois.days_until_expiry != null) {
            const wClass = d.whois.days_until_expiry < 30 ? 'down' : (d.whois.days_until_expiry < 60 ? 'warn' : 'ok');
            html += row('Expires In', badge(d.whois.days_until_expiry + ' days', wClass));
        }
        if (d.whois.name_servers && d.whois.name_servers.length) {
            html += row('Nameservers', d.whois.name_servers.map(ns => esc(ns)).join('<br>'));
        }
        html += '</div>';
    } else {
        html += `<span class="error-msg">${esc(d.whois ? d.whois.error : 'No data')}</span>`;
    }
    html += '</div>';

    // DNS Records section (collapsible)
    html += '<details class="dns-details">';
    html += '<summary>DNS Records</summary>';
    if (d.dns && !d.dns.error) {
        const types = ['A','AAAA','CNAME','MX','NS','TXT','SOA'];
        types.forEach(type => {
            if (!d.dns[type]) return;
            html += '<div class="dns-group">';
            html += `<span class="dns-type">${type}</span>`;
            const val = d.dns[type];
            if (type === 'SOA' && typeof val === 'object' && !Array.isArray(val)) {
                html += `<div class="dns-value">mname: ${esc(val.mname)}</div>`;
                html += `<div class="dns-value">rname: ${esc(val.rname)}</div>`;
                html += `<div class="dns-value">serial: ${val.serial}</div>`;
            } else if (type === 'MX' && Array.isArray(val)) {
                val.forEach(mx => { html += `<div class="dns-value">${mx.priority} ${esc(mx.exchange)}</div>`; });
            } else if (Array.isArray(val)) {
                val.forEach(v => { html += `<div class="dns-value">${esc(String(v))}</div>`; });
            }
            html += '</div>';
        });
    } else {
        html += `<span class="error-msg">${esc(d.dns ? d.dns.error : 'No data')}</span>`;
    }
    html += '</details>';

    html += '</div>'; // card-body
    return html;
}

// Chart drawing
function drawChart(domain) {
    const domId = domain.replace(/\\./g, '-');
    const canvas = document.getElementById('chart-' + domId);
    if (!canvas) return;

    const data = chartData[domain] || [];
    if (data.length === 0) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = 120 * dpr;
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = 120;
    const pad = { top: 8, right: 12, bottom: 20, left: 40 };
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;

    ctx.clearRect(0, 0, w, h);

    // Compute range
    const values = data.map(d => d.ms);
    const maxMs = Math.max(...values, 50);
    const minMs = 0;

    // Get theme colors from CSS
    const style = getComputedStyle(document.documentElement);
    const gridColor = style.getPropertyValue('--chart-grid').trim();
    const lineColor = style.getPropertyValue('--chart-line').trim();
    const fillColor = style.getPropertyValue('--chart-fill').trim();
    const dimColor = style.getPropertyValue('--text-dim').trim();

    // Grid lines
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 4; i++) {
        const y = pad.top + (plotH / 4) * i;
        ctx.beginPath();
        ctx.moveTo(pad.left, y);
        ctx.lineTo(w - pad.right, y);
        ctx.stroke();
    }

    // Y axis labels
    ctx.fillStyle = dimColor;
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 4; i++) {
        const y = pad.top + (plotH / 4) * i;
        const val = Math.round(maxMs - (maxMs / 4) * i);
        ctx.fillText(val + 'ms', pad.left - 6, y + 3);
    }

    if (data.length < 2) return;

    // X positions spread evenly
    const points = data.map((d, i) => ({
        x: pad.left + (i / (data.length - 1)) * plotW,
        y: pad.top + plotH - ((d.ms - minMs) / (maxMs - minMs)) * plotH,
        ms: d.ms,
        up: d.up,
        time: d.time
    }));

    // Fill area
    ctx.beginPath();
    ctx.moveTo(points[0].x, h - pad.bottom);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, h - pad.bottom);
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();

    // Line
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1];
        const curr = points[i];
        const cpx = (prev.x + curr.x) / 2;
        ctx.bezierCurveTo(cpx, prev.y, cpx, curr.y, curr.x, curr.y);
    }
    ctx.strokeStyle = lineColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Dots
    points.forEach((p, i) => {
        const isLast = i === points.length - 1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, isLast ? 4 : 2, 0, Math.PI * 2);
        ctx.fillStyle = p.up ? lineColor : style.getPropertyValue('--red').trim();
        ctx.fill();
        if (isLast) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 7, 0, Math.PI * 2);
            ctx.strokeStyle = lineColor;
            ctx.lineWidth = 1;
            ctx.globalAlpha = 0.3;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }
    });

    // Update value label
    const valEl = document.getElementById('chart-val-' + domId);
    if (valEl) {
        const latest = data[data.length - 1];
        valEl.textContent = latest.ms + ' ms';
    }
}

function row(label, value) {
    return `<div class="data-label">${esc(label)}</div><div class="data-value">${value}</div>`;
}

function badge(text, cls) {
    return `<span class="badge ${cls}">${text}</span>`;
}

function formatDate(d) {
    if (!d || d === 'None') return '\\u2014';
    try {
        const date = new Date(d);
        if (isNaN(date)) return esc(String(d));
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch { return esc(String(d)); }
}

function esc(s) {
    if (s == null) return '\\u2014';
    const div = document.createElement('div');
    div.textContent = String(s);
    return div.innerHTML;
}

// Start
fetchData();
pollTimer = setInterval(fetchData, 30000);
pingTimer = setInterval(fetchPings, 2000);
</script>
</body>
</html>'''
