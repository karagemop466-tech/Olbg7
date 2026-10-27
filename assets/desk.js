/* Static snapshots are deliberately fail-closed when JS or the device clock is unavailable. */
(function (root) {
  'use strict';
  function asTime(value) { return typeof value === 'string' && value ? Date.parse(value) : NaN; }
  function state(now, snapshot, expiry, cutoff) {
    const start = asTime(snapshot), end = asTime(expiry), until = asTime(cutoff);
    if (![now, start, end].every(Number.isFinite) || end <= start || now < start) return 'clock-error';
    if (now >= end) return 'stale';
    if (cutoff !== null && (!Number.isFinite(until) || now >= until)) return 'ended';
    return 'fresh';
  }
  function utc(value) { return new Date(asTime(value)).toISOString().replace('T', ' ').replace(':00.000Z', ' UTC'); }
  function update(doc, now) {
    const body = doc.body, snapshot = body.dataset.snapshot, expiry = body.dataset.expiry;
    const global = state(now, snapshot, expiry, null);
    const strip = doc.getElementById('snapshot-status');
    const message = doc.getElementById('snapshot-message');
    if (strip && message) {
      strip.classList.toggle('stale', global !== 'fresh');
      if (global === 'fresh') {
        const minutes = Math.floor((now - asTime(snapshot)) / 60000);
        const age = minutes < 60 ? minutes + ' min' : Math.floor(minutes / 60) + ' h ' + (minutes % 60) + ' min';
        message.textContent = 'Manual snapshot began ' + utc(snapshot) + ' · age ' + age + ' · not live; no automated refresh. Recheck sources.';
      } else if (global === 'stale') {
        message.textContent = 'Snapshot expired at ' + utc(expiry) + '. Current selections and scheduled rows are hidden; no automated refresh is running.';
      } else {
        message.textContent = 'Freshness could not be established from this device clock. Current selections and scheduled rows are hidden.';
      }
    }
    doc.querySelectorAll('[data-fresh]').forEach(function (item) {
      item.classList.toggle('is-visible', state(now, snapshot, expiry, item.dataset.until || '') === 'fresh');
    });
    doc.querySelectorAll('[data-empty-for]').forEach(function (el) {
      const key = el.dataset.emptyFor;
      const count = Array.from(doc.querySelectorAll('[data-kind="' + key + '"]')).filter(function (item) {
        return item.classList.contains('is-visible');
      }).length;
      el.classList.toggle('is-visible', count === 0);
    });
    doc.querySelectorAll('[data-count-for]').forEach(function (el) {
      const key = el.dataset.countFor;
      el.textContent = String(Array.from(doc.querySelectorAll('[data-kind="' + key + '"]')).filter(function (item) {
        return item.classList.contains('is-visible');
      }).length);
    });
  }
  function nextDelay(doc, now) {
    if (!Number.isFinite(now)) return 30000;
    const times = [asTime(doc.body.dataset.snapshot), asTime(doc.body.dataset.expiry)];
    doc.querySelectorAll('[data-fresh]').forEach(function (item) { times.push(asTime(item.dataset.until)); });
    const future = times.filter(function (time) { return Number.isFinite(time) && time > now; });
    return future.length ? Math.max(1, Math.min(30000, Math.min.apply(null, future) - now)) : 30000;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { state: state, update: update, nextDelay: nextDelay };
  if (root && root.document) {
    let timer;
    const run = function () {
      if (timer !== undefined) root.clearTimeout(timer);
      const now = Date.now();
      update(root.document, now);
      timer = root.setTimeout(run, nextDelay(root.document, now));
    };
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', run); else run();
    root.addEventListener('pageshow', run);
    root.document.addEventListener('visibilitychange', run);
  }
})(typeof window !== 'undefined' ? window : null);
