# Cortex Athlete

> **In active development.** Core structure is in place; features are being added phase by phase. See [Roadmap](#roadmap).

Does how sharp you feel before training predict how well you perform? Cortex Athlete is a full-stack web app that lets an athlete take a quick cognitive test before a session, log how the session went, and see how the two relate over time.

## How it will work

1. **Cognitive test**: a short reaction-time test right before training measures your mental state that day.
2. **Log session**: after training, record the session and how you performed.
3. **Dashboard**: see your cognitive scores and performance side by side, and whether higher test scores line up with better sessions.

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, React Router |
| Backend | Python, FastAPI, Pydantic |
| Testing | pytest |
| Tooling | ESLint, Git with conventional commits |

The repo is a monorepo with isolated dependencies: `frontend/` (React app) and `backend/` (FastAPI API).

## Current status

**Working now**
- React app with client-side routing between the Dashboard, Cognitive Test and Log Session pages
- FastAPI backend with a `/health` endpoint and environment-based CORS configuration
- Backend tests (pytest) for the health check and CORS setup

**In progress**
- Typed API client connecting the React frontend to the FastAPI backend

## Roadmap

- [x] Monorepo setup, React frontend scaffold and routing
- [x] FastAPI backend with health check and tests
- [ ] Connect frontend to backend (typed API client) — *in progress*
- [ ] Reaction-time cognitive test with accurate timing
- [ ] Session logging with persistent storage
- [ ] Statistics layer: relate cognitive scores to session performance
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
fastapi dev app/main.py
```

The API runs at http://127.0.0.1:8000 (interactive docs at `/docs`).

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
pytest
```
