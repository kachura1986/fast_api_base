# 🚀 FastAPI Service

> High-performance FastAPI service

---

## ✨ Features

* 🐍 Python 3.12+
* ⚡ FastAPI + async ready
* 📦 Modern `pyproject.toml`
* 🧠 Typed (mypy)
* 🎯 Ruff linting
* 🔁 Retry support (tenacity)
* ⚙️ Config via environment variables


---

## 📦 Installation

```bash
git clone https://github.com/yourname/fast-api.git
cd fast-api
uv sync
```

---

## ▶️ Run

```bash
uv run fast-api
```

or manually

```bash
uv run uvicorn app.main:app --reload
```

---

## 🧹 Lint

```bash
uv run ruff check .
```

---

## 🧠 Type checking

```bash
uv run mypy .
```

---

## 📁 Project structure

```
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── dependencies.py
│   └── schemas.py
│
├── tests/
├── pyproject.toml
└── README.md
```

---

## ⚙️ Configuration

Create `.env` file:

```
APP_NAME=FastAPI Service
DEBUG=true
```

---

## 🔥 Example endpoint

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```
