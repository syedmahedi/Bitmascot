DayMate — AI Assistant for Daily Planning (Scaffold)

This repository contains a starter scaffold for DayMate, an AI-powered assistant that combines weather and local news to generate personalized daily plans.

Tech choices in this scaffold
- Backend: FastAPI (Python)
- Frontend: Vue 3 (via CDN for a lightweight scaffold)

Quick local run (Windows PowerShell)

1. Create and activate a Python venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies and run the API

```powershell
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Open the frontend

You can open `frontend/index.html` directly in your browser, or serve it with a static server:

```powershell
cd frontend
python -m http.server 5173
# then open http://localhost:5173 in your browser
```

Environment variables
- Copy `.env.example` to `.env` and fill API keys (do NOT commit real keys).

What's included
- `backend/` — FastAPI skeleton with endpoints: `/`, `/weather`, `/news`, `/plan` (mock implementations)
- `frontend/` — Minimal Vue (CDN) single-file `index.html` that consumes the backend
- `.env.example` — Shows required environment variables

Next steps to complete the project
- Integrate a real weather API (OpenWeatherMap or similar)
- Integrate a news API or scraping for local news
- Implement LLM-based or rule-based planning logic (backend)
- Add user interface polish and deployment configs

Refer to `requirement.txt` for full assignment requirements.
