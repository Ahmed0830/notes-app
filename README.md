# Notes App

A minimal single-page notes app built with Flask + SQLite, served via Docker.

## Stack
- **Backend**: Python / Flask
- **Database**: SQLite (persisted via Docker volume)
- **Frontend**: Vanilla HTML/CSS/JS (single file)

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes` | Fetch all notes |
| POST | `/api/notes` | Create a note `{ "content": "..." }` |
| DELETE | `/api/notes?id=<id>` | Delete a note by ID |

## Run with Docker

```bash
docker compose up --build
```

Then open http://localhost:5000

## Run locally

```bash
pip install -r requirements.txt
mkdir -p /data
python app.py
```

## Keyboard Shortcut

Press **Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows) to submit a note.
