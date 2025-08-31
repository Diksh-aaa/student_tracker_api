# 🎓 Student Performance Tracker API

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red.svg)](https://docs.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.x-orange.svg)](https://docs.pydantic.dev/latest/)
[![OpenAPI Docs](https://img.shields.io/badge/Swagger-OpenAPI%203.0-85EA2D.svg?logo=swagger)](#-api-docs-swagger-ui)

FastAPI + SQLite (extendable to Postgres). Clean, modular, and ready for Swagger testing — built per the assignment PDF.

---

## ✨ Features

- Modular FastAPI project (`routers/`, `schemas`, `models`, `database`, `config`)
- Students: add, list (pagination), get, delete, search
- Scores: upsert per subject, student average, subject top scorer, department average
- SQLite by default; set `DATABASE_URL` for Postgres
- Tables auto-create on startup; interactive docs at `/docs`

## 🚀 TL;DR — Run It

```bash
# From project root
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

Windows (PowerShell):

```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> Tip: If you created `venv` instead of `.venv`, activate that and run the same Uvicorn command.

## 🗂️ Project Structure

```
.
├── app/
│   ├── core/
│   │   └── config.py           # Settings / DATABASE_URL
│   ├── routers/
│   │   ├── students.py         # Student CRUD + search
│   │   └── scores.py           # Scores upsert + analytics
│   ├── __init__.py
│   ├── database.py             # Engine + session and DI
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic v2 schemas
│   └── main.py                 # FastAPI app + router registration
├── requirements.txt
├── .env.example
└── README.md
```

## 📜 API Docs (Swagger UI)

- Run the server, then open: http://localhost:8000/docs
- JSON schema: http://localhost:8000/openapi.json

## 🧩 Endpoints Overview

| Method | Endpoint                                              | Description                            |
|------:|-------------------------------------------------------|----------------------------------------|
|  POST | `/students/`                                          | Add a new student                      |
|   GET | `/students/`                                          | List students (`skip`, `limit`)        |
|   GET | `/students/{student_id}`                              | Get student by ID                      |
|DELETE | `/students/{student_id}`                              | Remove student                         |
|   GET | `/students/search/?name={text}`                       | Search students by name                |
|  POST | `/students/{student_id}/scores/`                      | Add/update subject score (upsert)      |
|   GET | `/students/{student_id}/average-score/`               | Average score for a student            |
|   GET | `/students/top-scorer/{subject}`                      | Top scorer in a subject                |
|   GET | `/students/departments/{department}/average-score/`   | Average score for a department         |

## 🔁 Example Workflow (cURL)

Add a student
```bash
curl -X POST http://localhost:8000/students/ \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice","department":"CSE"}'
```

List students
```bash
curl http://localhost:8000/students/
```

Search by name
```bash
curl 'http://localhost:8000/students/search/?name=ali'
```

Add or update a score
```bash
curl -X POST http://localhost:8000/students/1/scores/ \
  -H 'Content-Type: application/json' \
  -d '{"subject":"math","score":91.5}'
```

Student average
```bash
curl http://localhost:8000/students/1/average-score/
```

Top scorer in subject
```bash
curl http://localhost:8000/students/top-scorer/math
```

Department average
```bash
curl http://localhost:8000/students/departments/CSE/average-score/
```

## ⚙️ Configuration

- Copy `.env.example` to `.env` and edit as needed.
- Default DB is a local SQLite file `students.db` in the project root.

Key variable:

```env
DATABASE_URL=sqlite:///./students.db
# Postgres example: postgresql+psycopg://user:pass@localhost:5432/students
```

## 🐘 Postgres (Optional)

Switch to Postgres by setting `DATABASE_URL` and installing a driver:

```bash
pip install 'psycopg[binary]'
export DATABASE_URL='postgresql+psycopg://user:password@localhost:5432/students'
uvicorn app.main:app --reload
```

Tables are created automatically on startup.

## 🧰 Tips & Troubleshooting

- ImportError: "attempted relative import with no known parent package"
  - Run from the project root with Uvicorn: `uvicorn app.main:app --reload`
  - Do not run `python app/main.py`.
- SQLite file location: created in the repo root by default (`students.db`).
- Alternative dev command: `fastapi dev app/main.py`

---

Built with ❤️ using FastAPI, SQLAlchemy and Pydantic.
# student_tracker_api
