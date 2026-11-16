# Cortex Athlete

> **In active development.** Core structure is in place; features are being added phase by phase. See [Roadmap](#roadmap).

Is how sharp you feel before playing related to how well you perform? Cortex Athlete is a full-stack web app that lets an athlete take a quick cognitive test before a session, log how the session went, and see how the two relate over time.

## How it will work

1. **Cognitive test**: a short reaction-time test right before playing measures your reaction speed that day.
2. **Log session**: after playing, record sport-specific performance (golf and volleyball to start).
3. **Dashboard**: see cognitive results and performance side by side, with correlations reported alongside sample size and uncertainty. Correlation is never presented as causation.

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, React Router |
| Backend | Python, FastAPI, Pydantic |
| Database | SQLAlchemy 2, Alembic migrations, SQLite (dev) |
| Testing | pytest (backend), Vitest (frontend) |
| Tooling | ESLint, Git with conventional commits |

The repo is a monorepo with isolated dependencies: `frontend/` (React app) and `backend/` (FastAPI API). The database design and its reasoning are documented in [docs/schema.md](docs/schema.md).

## Current status

**Working now**
- React app with client-side routing between the Dashboard, Cognitive Test and Log Session pages
- FastAPI backend with a `/health` endpoint and environment-based CORS configuration
- Typed API client connecting the React frontend to the FastAPI backend, with HTTP error handling
- Normalized database schema (users, cognitive sessions and trials, sport sessions, golf and volleyball performance) built with SQLAlchemy models and versioned Alembic migrations, with foreign keys enforced
- Tests for the backend (pytest) and the API client (Vitest, using a mocked `fetch`)

**Next**
- Reaction-time test in the frontend

## Roadmap

- [x] Monorepo setup, React frontend scaffold and routing
- [x] FastAPI backend with health check and tests
- [x] Connect frontend to backend (typed API client)
- [x] Database schema (SQLAlchemy models, Alembic migrations)
- [ ] Reaction-time cognitive test with accurate timing
- [ ] Session logging with persistent storage
- [ ] Statistics layer: relate cognitive results to session performance
- [ ] Dashboard charts
- [ ] Synthetic data seed script for demos
- [ ] Deployment

## Running it locally

**Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
alembic upgrade head         # create or update the database schema
fastapi dev app/main.py
```

The API runs at http://127.0.0.1:8000 (interactive docs at `/docs`).

**Database:** development uses a local SQLite file (`backend/cortex.db`, not committed). Run `alembic upgrade head` after cloning and whenever new migrations are pulled. To use a different database, set the `DATABASE_URL` environment variable.

**Frontend** (in a second terminal)

```bash
cd frontend
npm install
npm run dev
```

Then open the URL Vite prints (usually http://localhost:5173).

**Tests**

```bash
cd backend
python -m pytest
```

```bash
cd frontend
npm test
```