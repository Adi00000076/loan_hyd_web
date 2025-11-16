# TODO: Add Offline Mode (PWA) to Django Chit Funds App

## Steps to Complete

- [x] Create `static/manifest.json` for PWA metadata (name, icons, start URL, etc.)
- [x] Create `static/js/service-worker.js` to cache key resources (HTML, CSS, JS) for offline access
- [x] Update `core/templates/base.html` to link the manifest and register the service worker
- [x] Add PWA icons: `static/images/icon-192.png` and `static/images/icon-512.png` (placeholders; replace with actual icons)
- [x] Run `python manage.py collectstatic` to collect static files
- [x] Test the app in a browser to verify PWA installation and offline caching
- [x] Confirm offline functionality works (e.g., app loads cached content without internet)
