def get_dashboard_html() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>dnsboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg: #0a0a0a;
    --card: #1a1a1a;
    --card-border: #2a2a2a;
    --green: #4ade80;
    --green-dim: rgba(74, 222, 128, 0.15);
    --amber: #f59e0b;
    --amber-dim: rgba(245, 158, 11, 0.15);
    --red: #ef4444;
    --red-dim: rgba(239, 68, 68, 0.15);
    --text: #e5e5e5;
    --text-muted: #a3a3a3;
    --text-dim: #666;
    --mono: 'Courier New', 'Consolas', monospace;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    padding: 40px 20px;
}

.container { max-width: 900px; margin: 0 auto; }

header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--card-border);
}

h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: -0.02em;
}

.last-updated {
    font-size: 0.8rem;
    color: var(--text-dim);
    animation: pulse-text 3s ease-in-out infinite;
}

@keyframes pulse-text {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

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

.card {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeIn 0.5s ease forwards;
}

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
    margin-bottom: 24px;
}

.domain-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    font-weight: 400;
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

.status-dot.unknown {
    background: var(--text-dim);
}

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

.section {
    margin-bottom: 20px;
}

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

.data-value.updated {
    animation: highlight 1s ease;
}

@keyframes highlight {
    0% { background: rgba(74, 222, 128, 0.2); }
    100% { background: transparent; }
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

details.dns-details {
    margin-top: 4px;
}

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

details.dns-details[open] summary::before {
    transform: rotate(90deg);
}

.dns-group { margin-bottom: 12px; }

.dns-type {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    font-family: var(--mono);
    color: var(--text-muted);
    background: rgba(255,255,255,0.05);
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

.ping-log {
    max-height: 180px;
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
    border-bottom: 1px solid rgba(255,255,255,0.03);
}

.ping-entry .time { color: var(--text-dim); min-width: 70px; }
.ping-entry .code { min-width: 36px; }
.ping-entry .ms { color: var(--text-muted); min-width: 70px; text-align: right; }

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
}

.toast.visible {
    opacity: 1;
    transform: translateY(0);
}

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

.refresh-btn:hover {
    border-color: var(--text-muted);
    color: var(--text);
}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>dnsboard</h1>
        <div style="display:flex;align-items:center;gap:12px;">
            <button class="refresh-btn" onclick="refreshAll()">Refresh All</button>
            <span class="last-updated" id="lastUpdated">loading...</span>
        </div>
    </header>
    <div id="domains">
        <div class="loading"><span class="loading-spinner"></span>Fetching domain data...</div>
    </div>
</div>
<div class="toast" id="toast"></div>

<script>
const pingHistory = {};
let lastData = null;
let pollTimer = null;

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
    document.getElementById('lastUpdated').textContent =
        'updated ' + new Date().toLocaleTimeString();
}

function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('visible');
}

function hideToast() {
    document.getElementById('toast').classList.remove('visible');
}

function renderDomains(data) {
    const container = document.getElementById('domains');
    const domains = data._meta ? data._meta.domains : Object.keys(data).filter(k => k !== '_meta');

    if (!domains.length) {
        container.innerHTML = '<div class="loading">No domains to display</div>';
        return;
    }

    const existingCards = {};
    container.querySelectorAll('.card').forEach(c => {
        existingCards[c.dataset.domain] = c;
    });

    const fragment = document.createDocumentFragment();
    domains.forEach((domain, idx) => {
        const d = data[domain];
        if (!d) return;

        // Track ping history
        if (d.ping && d.ping.timestamp) {
            if (!pingHistory[domain]) pingHistory[domain] = [];
            const lastEntry = pingHistory[domain][pingHistory[domain].length - 1];
            if (!lastEntry || lastEntry.timestamp !== d.ping.timestamp) {
                pingHistory[domain].push(d.ping);
                if (pingHistory[domain].length > 20) pingHistory[domain].shift();
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

        if (!existing) {
            card.className = 'card' + alertClass;
            card.dataset.domain = domain;
            card.style.animationDelay = (idx * 0.1) + 's';
        } else {
            card.className = 'card' + alertClass;
            card.style.animationDelay = '0s';
            card.style.opacity = '1';
            card.style.transform = 'none';
        }

        card.innerHTML = buildCardContent(domain, d, isUp, isDown, sslWarn, whoisWarn);
        if (!existing) fragment.appendChild(card);
        delete existingCards[domain];
    });

    // Remove cards for domains no longer in data
    Object.values(existingCards).forEach(c => c.remove());

    // Only clear loading on first render
    if (!container.querySelector('.card')) {
        container.innerHTML = '';
    }
    container.appendChild(fragment);
}

function buildCardContent(domain, d, isUp, isDown, sslWarn, whoisWarn) {
    let html = '';

    // Header
    const dotClass = isUp ? 'up' : (isDown ? 'down' : 'unknown');
    const statusText = d.ping
        ? (d.ping.error ? d.ping.error : `${d.ping.status_code} · ${d.ping.response_time_ms}ms`)
        : '';
    html += `<div class="card-header">
        <span class="status-dot ${dotClass}"></span>
        <span class="domain-name">${esc(domain)}</span>
        <span class="status-text">${esc(statusText)}</span>
    </div>`;

    // Ping / Status section
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
    if (pings.length > 0) {
        html += '<div class="ping-log">';
        for (let i = pings.length - 1; i >= 0; i--) {
            const p = pings[i];
            const t = new Date(p.timestamp).toLocaleTimeString();
            const codeClass = p.is_up ? 'up' : 'down';
            const ms = p.response_time_ms != null ? p.response_time_ms + 'ms' : '—';
            const code = p.status_code || '—';
            html += `<div class="ping-entry">
                <span class="time">${t}</span>
                <span class="code">${badge(code, codeClass)}</span>
                <span class="ms">${ms}</span>
            </div>`;
        }
        html += '</div>';
    }
    html += '</div>';

    // SSL section
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

    // WHOIS section
    html += '<div class="section">';
    html += '<div class="section-title">WHOIS</div>';
    if (d.whois && !d.whois.error) {
        html += '<div class="data-grid">';
        html += row('Registrar', d.whois.registrar || '—');
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

    // DNS section (collapsible)
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
                val.forEach(mx => {
                    html += `<div class="dns-value">${mx.priority} ${esc(mx.exchange)}</div>`;
                });
            } else if (Array.isArray(val)) {
                val.forEach(v => {
                    html += `<div class="dns-value">${esc(String(v))}</div>`;
                });
            }
            html += '</div>';
        });
    } else {
        html += `<span class="error-msg">${esc(d.dns ? d.dns.error : 'No data')}</span>`;
    }
    html += '</details>';

    return html;
}

function row(label, value) {
    return `<div class="data-label">${esc(label)}</div><div class="data-value">${value}</div>`;
}

function badge(text, cls) {
    return `<span class="badge ${cls}">${text}</span>`;
}

function formatDate(d) {
    if (!d || d === 'None') return '—';
    try {
        const date = new Date(d);
        if (isNaN(date)) return esc(String(d));
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch { return esc(String(d)); }
}

function esc(s) {
    if (s == null) return '—';
    const div = document.createElement('div');
    div.textContent = String(s);
    return div.innerHTML;
}

// Start
fetchData();
pollTimer = setInterval(fetchData, 30000);
</script>
</body>
</html>'''
