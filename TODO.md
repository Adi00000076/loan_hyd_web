# TODO List for Django Authentication and Dashboard Setup

## 1. Rename Home to Dashboard

- [x] Rename `core/templates/home.html` to `dashboard.html`
- [x] Update `core/views.py`: rename `home` function to `dashboard`, add `@login_required` decorator, change template to 'dashboard.html'
- [x] Update `core/urls.py`: change path for home to dashboard at '/dashboard/', add new path for root that redirects based on auth

## 2. Protect Dashboard and Set Redirects

- [x] Add `LOGIN_URL = 'login'` and `LOGOUT_REDIRECT_URL = 'login'` to `jai_hanuman_chits/settings.py`
- [x] Update root URL to use a new view that redirects to login or dashboard

## 3. Update Templates and Navigation

- [x] Update `core/templates/base.html`: change nav links from 'home' to 'dashboard'
- [x] Update any other references

## 4. Test Changes

- [x] Run the server and verify login redirects to dashboard, logout works, and unauthenticated users see login
