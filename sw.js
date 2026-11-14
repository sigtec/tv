// Service Worker: hält die App-Hülle offline bereit.
// Streams und Senderliste laufen bewusst NICHT über den Cache
// (die Senderliste puffert die Seite selbst im localStorage).
const CACHE = 'tv-v1';
const HLS_URL = 'https://cdn.jsdelivr.net/npm/hls.js@1.7.4/dist/hls.min.js';
const SHELL = [
  './',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/favicon.png',
  HLS_URL
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Seite selbst: erst Netz (damit Updates sofort ankommen), sonst Cache
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put('./', copy));
          return res;
        })
        .catch(() => caches.match('./'))
    );
    return;
  }

  // Eigene Dateien und die fest versionierte hls.js: erst Cache
  if (url.origin === location.origin || req.url === HLS_URL) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
  }
  // alles andere (Streams, Logos, Senderliste) geht direkt ans Netz
});
