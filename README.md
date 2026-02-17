# PES H2H Tracker ⚽

A simple mobile-friendly MVP web app for tracking PES/FIFA match results and Head-to-Head (H2H) stats among friends.

## Why this exists
Friends play many games and later argue about who leads the head-to-head. This app keeps records clearly and fairly.

## Features (MVP)
- Add players
- Record matches (players, teams used, scores, timestamp)
- View Head-to-Head (H2H) stats between any two players
- View all matches with filtering
- Soft delete matches (Recycle Bin) + restore
- Feedback page for user suggestions
- “Restored” badge for transparency when a binned match is restored

## Tech Stack
- FastAPI (Python)
- SQLite + SQLAlchemy
- Jinja2 Templates (server-rendered pages)
- Vanilla JavaScript (fetch API)
- Mobile-first CSS UI (simple app-like UI)

## Future Improvements
- User accounts / roles
- Leaderboards + streaks
- Export results to CSV
- Multi-group support (different friend circles)

## Run Locally (Windows)
```bash
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
