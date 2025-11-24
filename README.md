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

## Live URLs
- Backend (Render): `https://bitmascot-backend.onrender.com`  
- Frontend (Netlify): `https://<your-netlify-site-url>`