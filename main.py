from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models

from datetime import datetime, timezone

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/add-player", response_class=HTMLResponse)
def add_player_page(request: Request):
    return templates.TemplateResponse("add_player.html", {"request": request})

@app.get("/record-match", response_class=HTMLResponse)
def record_match_page(request: Request):
    return templates.TemplateResponse("record_match.html", {"request": request})

@app.get("/h2h-page", response_class=HTMLResponse)
def h2h_page(request: Request):
    return templates.TemplateResponse("h2h.html", {"request": request})

@app.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Add Player
@app.post("/players/")
def add_player(name: str, db: Session = Depends(get_db)):
    # Check if player already exists
    existing_player = db.query(models.Player).filter(models.Player.name == name).first()
    if existing_player:
        raise HTTPException(status_code=400, detail="Player already exists")

    new_player = models.Player(name=name)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player


# ✅ Get All Players
@app.get("/players/")
def get_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players

from datetime import datetime


# ✅ Record Match
@app.post("/matches/")
def record_match(
    player1_id: int,
    player2_id: int,
    player1_score: int,
    player2_score: int,
    player1_team: str,
    player2_team: str,
    db: Session = Depends(get_db)
):


    # Prevent same player playing themselves
    if player1_id == player2_id:
        raise HTTPException(status_code=400, detail="A player cannot play against themselves")

    # Check both players exist
    player1 = db.query(models.Player).filter(models.Player.id == player1_id).first()
    player2 = db.query(models.Player).filter(models.Player.id == player2_id).first()

    if not player1 or not player2:
        raise HTTPException(status_code=404, detail="Player not found")

    new_match = models.Match(
    player1_id=player1_id,
    player2_id=player2_id,
    player1_score=player1_score,
    player2_score=player2_score,
    player1_team=player1_team,
    player2_team=player2_team,
    date=datetime.now(timezone.utc)
)

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return {"message": "Match recorded successfully"}


# ✅ Move match to bin (soft delete)
@app.post("/matches/bin")
def move_match_to_bin(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    match.is_deleted = True
    match.deleted_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Match moved to bin"}

# ✅ Restore match from bin
@app.post("/matches/restore")
def restore_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    match.is_deleted = False
    match.deleted_at = None
    match.restored_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Match restored successfully"}


@app.get("/bin", response_class=HTMLResponse)
def bin_page(request: Request, db: Session = Depends(get_db)):
    deleted_matches = db.query(models.Match).filter(models.Match.is_deleted == True).order_by(models.Match.deleted_at.desc()).all()

    # Build view-friendly data (names)
    result = []
    for m in deleted_matches:
        p1 = db.query(models.Player).filter(models.Player.id == m.player1_id).first()
        p2 = db.query(models.Player).filter(models.Player.id == m.player2_id).first()

        result.append({
            "id": m.id,
            "date": m.date,
            "deleted_at": m.deleted_at,
            "player1_name": p1.name if p1 else "Unknown",
            "player2_name": p2.name if p2 else "Unknown",
            "player1_team": m.player1_team,
            "player2_team": m.player2_team,
            "player1_score": m.player1_score,
            "player2_score": m.player2_score
        })

    return templates.TemplateResponse("bin.html", {"request": request, "matches": result})


from fastapi import Query

# ✅ H2H Stats
@app.get("/h2h/")
def h2h(player1_id: int, player2_id: int, db: Session = Depends(get_db)):

    # 👇 Fetch players to get their names
    player1 = db.query(models.Player).filter(models.Player.id == player1_id).first()
    player2 = db.query(models.Player).filter(models.Player.id == player2_id).first()

    if not player1 or not player2:
        raise HTTPException(status_code=404, detail="Player not found")

    matches = db.query(models.Match).filter(
    (
        ((models.Match.player1_id == player1_id) & (models.Match.player2_id == player2_id)) |
        ((models.Match.player1_id == player2_id) & (models.Match.player2_id == player1_id))
    ),
    (models.Match.is_deleted == False)
).all()


    if not matches:
        return {"message": "No matches found between these players"}

    stats = {
        "player1_name": player1.name,   # 👈 added
        "player2_name": player2.name,   # 👈 added
        "player1_wins": 0,
        "player2_wins": 0,
        "draws": 0,
        "total_matches": len(matches)
    }

    for m in matches:
        if m.player1_id == player1_id:
            p1_score = m.player1_score
            p2_score = m.player2_score
        else:
            p1_score = m.player2_score
            p2_score = m.player1_score

        if p1_score > p2_score:
            stats["player1_wins"] += 1
        elif p2_score > p1_score:
            stats["player2_wins"] += 1
        else:
            stats["draws"] += 1

    return stats

@app.post("/feedback-submit")
def submit_feedback(message: str, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(message=message)
    db.add(new_feedback)
    db.commit()
    return {"message": "Thanks for your feedback!"}

@app.get("/admin/feedback", response_class=HTMLResponse)
def view_feedback(request: Request, db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()

    return templates.TemplateResponse(
        "view_feedback.html",
        {
            "request": request,
            "feedbacks": feedbacks
        }
    )

from fastapi.responses import HTMLResponse

# ✅ All Matches Page with optional player filter
@app.get("/all-matches", response_class=HTMLResponse)
def all_matches_page(request: Request, player_id: int = None, db: Session = Depends(get_db)):
    players = db.query(models.Player).all()  # Get all players for the dropdown

    if player_id:
        # Filter matches where the selected player participated
        matches_query = db.query(models.Match).filter(
            ((models.Match.player1_id == player_id) | (models.Match.player2_id == player_id)),
            (models.Match.is_deleted == False)
        ).all()
        selected_player = player_id
    else:
        matches_query = db.query(models.Match).filter(models.Match.is_deleted == False).all()
        selected_player = None

    # Prepare matches for the template
    matches = []
    for m in matches_query:
        player1 = db.query(models.Player).filter(models.Player.id == m.player1_id).first()
        player2 = db.query(models.Player).filter(models.Player.id == m.player2_id).first()

        matches.append({
            "id": m.id,
            "date": m.date,
            "restored_at": m.restored_at,
            "time_of_day": m.time_of_day,
            "player1_name": player1.name if player1 else "Unknown",
            "player2_name": player2.name if player2 else "Unknown",
            "player1_team": m.player1_team,
            "player2_team": m.player2_team,
            "player1_score": m.player1_score,
            "player2_score": m.player2_score,
            "outcome": (
                "Draw" if m.player1_score == m.player2_score else
                player1.name if m.player1_score > m.player2_score else player2.name
            )
        })

    return templates.TemplateResponse("all_matches.html", {
        "request": request,
        "matches": matches,
        "players": players,
        "selected_player": selected_player
    })


@app.post("/players/edit")
def edit_player(player_id: int, new_name: str, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    new_name = new_name.strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="New name cannot be empty")

    # prevent duplicates
    existing = db.query(models.Player).filter(models.Player.name == new_name).first()
    if existing and existing.id != player_id:
        raise HTTPException(status_code=400, detail="A player with this name already exists")

    player.name = new_name
    db.commit()
    return {"message": "Player updated successfully"}



