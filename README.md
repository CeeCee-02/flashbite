# FLASHBITE 🍔⚡

A location-based food delivery platform built for the Nigerian market.

**Tech stack:** Django 5 · DRF · Channels · Next.js 15 · Supabase PostgreSQL · Upstash Redis · Paystack · Leaflet.js

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Environment Variables Reference](#environment-variables-reference)
- [API Docs](#api-docs)
- [Testing](#testing)
- [Deployment](#deployment)
- [Build Milestones](#build-milestones)
- [Contributing](#contributing)

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| Node.js | 20 LTS |
| Git | any recent |
| Redis | 7+ (or use Upstash in cloud) |

---

## Quick Start

### 1. Clone

```bash
git clone <repo-url>
cd FLASHBITE
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Set up environment variables
cp .env.example .env
# → Open .env and fill in every value (see Environment Variables section below)

# Run database migrations
python manage.py migrate

# (Optional) Create a superuser for the Django admin
python manage.py createsuperuser

# Start the dev server
python manage.py runserver
```

In separate terminals, start the async workers:

```bash
# Terminal 2 — Celery worker
celery -A config worker --loglevel=info

# Terminal 3 — Celery beat scheduler
celery -A config beat --loglevel=info
```

> **Note:** WebSockets (Django Channels) require Daphne in production.
> In local development, `runserver` is fine for HTTP-only testing.

### 3. Frontend Setup

```bash
cd frontend

npm install

cp .env.example .env.local
# → Open .env.local and fill in every value

npm run dev
```

Frontend runs on **http://localhost:3000**
Backend API runs on **http://localhost:8000**

---

## Project Structure

```
FLASHBITE/
├── backend/                        # Django 5 + DRF + Channels
│   ├── accounts/                   # Auth, custom User model, JWT, email verify
│   │   ├── views.py                # register, login, logout, me, password-reset
│   │   ├── serializers.py
│   │   ├── models.py               # Custom User (UUID PK, role field)
│   │   ├── emails.py               # Resend transactional emails
│   │   └── tests/                  # pytest test suite (auth, register, email)
│   ├── restaurants/                # Restaurant profiles + menus
│   ├── foods/                      # Food items + categories
│   ├── orders/                     # Order lifecycle management
│   ├── riders/                     # Rider profiles + dispatch logic
│   ├── payments/                   # Paystack integration (raw HTTP via httpx)
│   ├── tracking/                   # Real-time GPS via WebSockets / Channels
│   ├── notifications/              # Resend email notifications
│   ├── core/                       # Shared utilities, base models, exception handler
│   ├── wallets/                    # [SCAFFOLD — v2]
│   ├── analytics/                  # [SCAFFOLD — v2]
│   ├── reviews/                    # [SCAFFOLD — pending]
│   ├── support/                    # [SCAFFOLD — v2]
│   ├── chat/                       # [SCAFFOLD — v2]
│   ├── config/                     # Django project config (settings, urls, asgi, wsgi)
│   │   └── settings/
│   │       ├── base.py             # Shared settings (loaded by dev + prod)
│   │       ├── dev.py              # Local overrides
│   │       └── prod.py             # Production (Render) overrides
│   └── requirements/
│       ├── base.txt                # Pinned production dependencies
│       ├── dev.txt                 # base + pytest, factory-boy, ipython
│       └── prod.txt                # base + django-celery-beat
│
├── frontend/                       # Next.js 15 App Router
│   ├── app/
│   │   ├── (customer)/             # Customer web app routes
│   │   ├── (restaurant)/           # Restaurant portal routes
│   │   ├── (rider)/                # Rider portal routes
│   │   ├── verify-email/           # Email verification page
│   │   ├── reset-password/         # Password reset page
│   │   ├── layout.tsx              # Root layout (Navbar, Footer)
│   │   └── page.tsx                # Marketing landing page
│   ├── components/                 # Shared UI components (Navbar, etc.)
│   ├── hooks/                      # Shared React hooks
│   ├── lib/                        # API client, utilities
│   ├── services/                   # Typed API service layer
│   └── store/                      # Zustand global state
│
└── infra/
    ├── supervisor/                 # supervisord.conf (Daphne + Celery ×2)
    ├── docker/                     # Dockerfile.backend (local dev only)
    ├── nginx/                      # Nginx config (if self-hosted)
    └── deployment/
        └── render.yaml             # Render.com IaC deployment config
```

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key (generate a strong random string) | `django-insecure-...` |
| `DJANGO_DEBUG` | Debug mode — **must be `False` in production** | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `localhost,127.0.0.1` |
| `DATABASE_URL` | Supabase/PostgreSQL connection string | `postgresql://user:pass@db.supabase.co:5432/postgres` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xxxx.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (server-side only) | `eyJ...` |
| `REDIS_URL` | Upstash Redis URL (TLS in production) | `rediss://default:token@host.upstash.io:6379` |
| `JWT_SIGNING_KEY` | Separate signing key for JWT tokens | (random secret) |
| `RESEND_API_KEY` | Resend.com API key for transactional email | `re_...` |
| `PAYSTACK_SECRET_KEY` | Paystack secret key | `sk_live_...` |
| `PAYSTACK_PUBLIC_KEY` | Paystack public key | `pk_live_...` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | `http://localhost:3000,https://flashbite.ng` |

### Frontend (`frontend/.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | `http://localhost:8000/api` |
| `NEXT_PUBLIC_WS_BASE_URL` | WebSocket base URL | `ws://localhost:8000/ws` |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://xxxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon/public key | `eyJ...` |
| `NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY` | Paystack public key (client-side) | `pk_test_...` |
| `NEXT_PUBLIC_MAP_TILE_URL` | OpenStreetMap tile URL for Leaflet.js | `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` |

> **Security:** Never commit `.env` or `.env.local`. Both are listed in `.gitignore`.

---

## API Docs

Interactive API documentation (Swagger UI) is available once the backend is running:

```
http://localhost:8000/api/docs/
```

The OpenAPI schema is auto-generated by **drf-spectacular**.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register a new user (customer / restaurant / rider) |
| `POST` | `/api/auth/verify-email/` | Verify email with OTP code |
| `POST` | `/api/auth/login/` | Obtain JWT access + refresh tokens |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `POST` | `/api/auth/logout/` | Blacklist refresh token |
| `GET/PATCH` | `/api/auth/me/` | Get / update current user profile |
| `POST` | `/api/auth/password-reset/request/` | Request password reset email |
| `POST` | `/api/auth/password-reset/confirm/` | Confirm password reset with OTP |
| `GET` | `/api/restaurants/` | List all restaurants (public, searchable) |
| `GET` | `/api/restaurants/<slug>/` | Get restaurant detail + menu categories |
| `GET/POST/PATCH` | `/api/restaurants/me/` | Manage own restaurant profile (restaurant role only) |
| `GET` | `/api/health/` | Health check endpoint (used by Render) |

---

## Testing

Tests live in each app's `tests/` directory and use **pytest + pytest-django**.

```bash
cd backend

# Run all tests with coverage report
pytest --cov=. -v

# Run a specific test file
pytest accounts/tests/test_auth.py -v

# Run tests matching a keyword
pytest -k "register" -v
```

Test factories use **factory-boy** + **Faker**. Coverage is measured with **pytest-cov**.

---

## Deployment

The backend is deployed to **Render.com** via `infra/deployment/render.yaml`.
The frontend is deployed to **Vercel** (or any Next.js-compatible host).

### Render (Backend)

1. Push your code to GitHub.
2. In the Render dashboard → **New → Blueprint** → connect your repo.
3. Render detects `render.yaml` and configures the service automatically.
4. Go to the service's **Environment** tab and add every `sync: false` secret manually.

**What Render runs on each deploy:**

```bash
pip install -r requirements/prod.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

Then starts processes via Supervisor:
- **Daphne** — ASGI server (HTTP + WebSocket)
- **Celery worker** — async task queue
- **Celery beat** — periodic task scheduler

### Vercel (Frontend)

1. Import the repo in Vercel, set **root directory** to `frontend`.
2. Build command: `npm run build`
3. Output directory: `.next`
4. Add all `NEXT_PUBLIC_*` environment variables in the Vercel dashboard.

### Production Checklist

- [ ] `DJANGO_DEBUG=False`
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] `CORS_ALLOWED_ORIGINS` includes your Vercel domain
- [ ] All secrets filled in Render environment variables
- [ ] Supabase database has PostGIS enabled (if using geo features)
- [ ] Upstash Redis TLS URL used (`rediss://`)
- [ ] Resend sending domain verified
- [ ] Paystack live keys configured (after going live)

---

## Build Milestones

| # | Feature | Status |
|---|---------|--------|
| M1 | Authentication (register, login, JWT, email verify, password reset) | 🔨 In progress |
| M2 | Restaurant Management (profiles, menus, categories) | 🔨 In progress |
| M3 | Food Items & Categories | 🔨 In progress |
| M4 | Ordering (cart → order lifecycle) | ⏳ Pending |
| M5 | Payments (Paystack — initialize, webhook, verify) | ⏳ Pending |
| M6 | Rider System (profiles, dispatch) | ⏳ Pending |
| M7 | Real-Time Tracking (WebSockets + Leaflet.js) | ⏳ Pending |
| M8 | Notifications (Resend emails — order updates, receipts) | ⏳ Pending |
| M9 | Production Deployment (Render + Vercel) | ✅ Configured |
| V2 | Wallets, Analytics, Reviews, Support, In-app Chat | 🗓 Planned |

---

## Contributing

1. **Branch naming:** `feat/<name>`, `fix/<name>`, `chore/<name>`
2. **Commit style:** Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`)
3. **Before opening a PR:**
   - Run `pytest --cov=. -v` — all tests must pass
   - Run `npm run lint` in the `frontend/` directory
4. **Python style:** Black + isort
5. **TypeScript style:** Prettier + ESLint

---

## License

Private project. All rights reserved.
