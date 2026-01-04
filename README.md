# Sunshine (Sip and SunShine) — Django Restaurant Website + Ordering

A Django web app for a restaurant website with multi-language pages (EN/NL/FR) and a working ordering flow (Menu → Cart → Checkout → Confirmation/Tracking).

- App code lives in `sip-sunshine-django/`
- Static assets are already included in `sip-sunshine-django/static/`

## Features

- Multi-language content (English, Dutch, French) via `django-parler`
- CMS-style pages (home/about/blog/contact/reservation/menu)
- Cart + checkout flow (pickup/delivery/dine-in)
- Order confirmation + order tracking
- Simple FAQ chatbot endpoint + site-wide widget
- Automated testing: Django tests + Playwright UI E2E tests

## Project Layout

- `sip-sunshine-django/` — Django project
  - `sip_sunshine/` — settings + root URLs
  - `restaurant/` — main app (pages, ordering, APIs)
  - `templates/` — server-rendered HTML
  - `static/` — CSS/JS/images/fonts
  - `tests/` — integration + E2E test suite

## Quick Start (Windows)

### 1) Create venv + install deps

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Migrate + (optional) seed demo data

```powershell
python .\sip-sunshine-django\manage.py migrate
python .\sip-sunshine-django\setup_db.py
```

### 3) Create an admin user

```powershell
python .\sip-sunshine-django\manage.py createsuperuser
```

### 4) Run the server

```powershell
python .\sip-sunshine-django\manage.py runserver 8000
```

Open:
- http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Key URLs

All of these also work with language prefixes like `/nl/` and `/fr/`.

- `/menu/` — menu + “Add to Order”
- `/checkout/` — checkout entry page (cart is browser-based)
- `/orders/tracking/?order=SIP-000015` or `/orders/tracking/?order_id=15`
- `/orders/confirmation/<order_id>/`
- `/api/orders/create/` and `/api/orders/<order_id>/`
- `/api/chatbot/`

## Ordering Flow (How it Works)

- Cart is stored client-side in `localStorage` under the key `sip_sunshine_cart`
- When the user proceeds to checkout, checkout state is staged in `sessionStorage` (cart, subtotal, order type, customer details)
- Checkout posts to the backend order API and then redirects to confirmation

## Tests

### Django test suite

```powershell
python .\sip-sunshine-django\manage.py test
```

### UI E2E tests (Playwright)

1) Install the browser runtime once:

```powershell
python -m playwright install chromium
```

2) Run the UI journey tests:

```powershell
python .\sip-sunshine-django\manage.py test tests.test_ui_journey_playwright --verbosity 2
```

## Notes

- The default dev database is SQLite.
- Uploaded media for demo/menu images lives under `sip-sunshine-django/media/`.

---

If you want, I can also trim docs further (many `sip-sunshine-django/*.md` files are internal notes) and keep only the essentials for GitHub.
