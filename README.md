# 🎮 Video Games Rivalry Tracker (PES / FIFA H2H)

A simple, mobile-friendly web app for tracking head-to-head (H2H) results between gamers who play PES or FIFA regularly.

Built as a Minimum Viable Product (MVP) to solve a real problem:  
**“Who is actually winning after weeks or months of playing?”**

---

## Live Demo
👉 https://videogames-rivalry-tracker.onrender.com

>  Warning: The app uses SQLite on a free Render instance. Data may reset on redeploy.

---

## Why This Project?

When friends play PES/FIFA frequently, keeping track of:
- wins
- draws
- head-to-head records  
often leads to arguments and forgotten results.

This app provides:
- a neutral record keeper
- transparent stats
- a simple UI usable on phones and computers

---

## Features

### 👥 Player Management
- Add new gamers dynamically
- Edit player names (fix spelling without breaking match history)

### ⚽ Match Recording
- Select Player A vs Player B
- Record scores and teams used
- Automatic timestamping

### Head-to-Head (H2H) Stats
- Total matches
- Wins per player
- Draws
- Clean, easy-to-read output

### 🗑 Soft Delete + Restore
- Mistaken matches can be moved to a recycle bin
- Deleted matches do **not** count in stats
- Restored matches are visibly tagged as **“Restored”**

### 📝 Feedback System
- Users can submit feedback directly in-app
- Designed to guide future improvements

### 📱 Responsive UI
- Works smoothly on desktop and mobile
- Clean, app-like interface

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Templating:** Jinja2
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

## ▶️ Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ayubaalhajimusah/videogames-rivalry-tracker.git
cd videogames-rivalry-tracker


## 📸 Screenshots

## 📸 Screenshots

### Home
![Home](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/home.png)

### Record Match
![Record Match](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/record_match.png)

### All Matches
![All Matches](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/all_matches.png)

### Head-to-Head (H2H)
![H2H](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/h2h.png)

### Recycle Bin
![Recycle Bin](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/recycle_bin.png)

### Add Player
![Add Player](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/add_player.png)

### Feedback
![Feedback](https://raw.githubusercontent.com/ayubaalhajimusah/videogames-rivalry-tracker/main/screenshots/feedback.png)
