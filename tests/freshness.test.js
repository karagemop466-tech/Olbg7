'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { state, update, nextDelay } = require('../assets/desk.js');

const SNAPSHOT = '2026-10-27T05:23:00Z';
const EXPIRY = '2026-10-28T05:23:00Z';
const CUTOFF = '2026-10-27T11:00:00Z';
const begin = Date.parse(SNAPSHOT), expiry = Date.parse(EXPIRY), cutoff = Date.parse(CUTOFF);

test('global freshness requires a valid clock and well ordered times', () => {
  assert.equal(state(begin, SNAPSHOT, EXPIRY, null), 'fresh');
  assert.equal(state(expiry - 1, SNAPSHOT, EXPIRY, null), 'fresh');
  assert.equal(state(expiry, SNAPSHOT, EXPIRY, null), 'stale');
  assert.equal(state(expiry + 1, SNAPSHOT, EXPIRY, null), 'stale');
  assert.equal(state(begin - 1, SNAPSHOT, EXPIRY, null), 'clock-error');
  assert.equal(state(NaN, SNAPSHOT, EXPIRY, null), 'clock-error');
  assert.equal(state(begin, 'bad', EXPIRY, null), 'clock-error');
  assert.equal(state(begin, SNAPSHOT, 'bad', null), 'clock-error');
  assert.equal(state(begin, SNAPSHOT, SNAPSHOT, null), 'clock-error');
  assert.equal(state(begin, EXPIRY, SNAPSHOT, null), 'clock-error');
});

test('scheduled items are hidden at the event cutoff or when it is missing', () => {
  assert.equal(state(cutoff - 1, SNAPSHOT, EXPIRY, CUTOFF), 'fresh');
  assert.equal(state(cutoff, SNAPSHOT, EXPIRY, CUTOFF), 'ended');
  assert.equal(state(cutoff + 1, SNAPSHOT, EXPIRY, CUTOFF), 'ended');
  assert.equal(state(begin, SNAPSHOT, EXPIRY, ''), 'ended');
  assert.equal(state(begin, SNAPSHOT, EXPIRY, undefined), 'ended');
  assert.equal(state(begin, SNAPSHOT, EXPIRY, 'invalid'), 'ended');
  assert.equal(state(expiry, SNAPSHOT, EXPIRY, 'invalid'), 'stale');
});

class Classes {
  constructor() { this.values = new Set(); }
  toggle(name, on) { if (on) this.values.add(name); else this.values.delete(name); }
  contains(name) { return this.values.has(name); }
}
function element(dataset = {}) { return { dataset, classList: new Classes(), textContent: '' }; }
function fakeDocument() {
  const strip = element(), message = element();
  const fresh = [
    element({ kind: 'pick', until: CUTOFF }),
    element({ kind: 'event', until: EXPIRY }),
    element({ kind: 'pick', until: 'invalid' }),
    element({ kind: 'pick' }),
  ];
  const empty = [element({ emptyFor: 'pick' }), element({ emptyFor: 'event' })];
  const counts = [element({ countFor: 'pick' }), element({ countFor: 'event' })];
  return {
    body: { dataset: { snapshot: SNAPSHOT, expiry: EXPIRY } },
    getElementById: id => ({ 'snapshot-status': strip, 'snapshot-message': message }[id]),
    querySelectorAll: selector => {
      if (selector === '[data-fresh]') return fresh;
      if (selector === '[data-empty-for]') return empty;
      if (selector === '[data-count-for]') return counts;
      const match = selector.match(/^\[data-kind="(.+)"\]$/);
      return match ? fresh.filter(item => item.dataset.kind === match[1]) : [];
    },
    fresh, empty, counts, strip, message,
  };
}

test('DOM update fails closed, tracks expiry and updates visible counts', () => {
  const doc = fakeDocument();
  update(doc, begin + 60000);
  assert.deepEqual(doc.fresh.map(x => x.classList.contains('is-visible')), [true, true, false, false]);
  assert.deepEqual(doc.counts.map(x => x.textContent), ['1', '1']);
  assert.deepEqual(doc.empty.map(x => x.classList.contains('is-visible')), [false, false]);
  assert.match(doc.message.textContent, /age 1 min/);
  assert.equal(doc.strip.classList.contains('stale'), false);

  update(doc, cutoff);
  assert.deepEqual(doc.fresh.map(x => x.classList.contains('is-visible')), [false, true, false, false]);
  assert.deepEqual(doc.counts.map(x => x.textContent), ['0', '1']);
  assert.equal(doc.empty[0].classList.contains('is-visible'), true);

  update(doc, expiry);
  assert.ok(doc.fresh.every(x => !x.classList.contains('is-visible')));
  assert.ok(doc.empty.every(x => x.classList.contains('is-visible')));
  assert.match(doc.message.textContent, /Snapshot expired/);
  assert.equal(doc.strip.classList.contains('stale'), true);

  update(doc, begin - 1000);
  assert.ok(doc.fresh.every(x => !x.classList.contains('is-visible')));
  assert.match(doc.message.textContent, /could not be established/);
  assert.equal(doc.strip.classList.contains('stale'), true);
});

test('messages use the actual snapshot metadata rather than hard-coded dates', () => {
  const doc = fakeDocument();
  doc.body.dataset.snapshot = '2026-11-03T10:00:00Z';
  doc.body.dataset.expiry = '2026-11-04T10:00:00Z';
  update(doc, Date.parse('2026-11-03T10:30:00Z'));
  assert.match(doc.message.textContent, /2026-11-03 10:00 UTC/);
  update(doc, Date.parse('2026-11-04T10:00:00Z'));
  assert.match(doc.message.textContent, /2026-11-04 10:00 UTC/);
});


test('the next update is scheduled for the earliest event or snapshot boundary', () => {
  const start = Date.parse('2026-10-27T05:23:00Z');
  const doc = {
    body: {dataset: {snapshot: '2026-10-27T05:23:00Z', expiry: '2026-10-27T05:24:00Z'}},
    querySelectorAll: () => [
      {dataset: {until: '2026-10-27T05:23:10Z'}},
      {dataset: {until: '2026-10-27T05:23:15Z'}},
      {dataset: {until: 'invalid'}}
    ]
  };
  assert.equal(nextDelay(doc, start), 10000);
  assert.equal(nextDelay(doc, start + 10000), 5000);
  assert.equal(nextDelay(doc, start + 20000), 30000);
  assert.equal(nextDelay(doc, start + 59000), 1000);
  assert.equal(nextDelay(doc, NaN), 30000);
});
