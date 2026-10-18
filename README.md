# 🚀 FastAPI Service

> High-performance FastAPI service

---

## ✨ Features

* 🐍 Python 3.13+
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
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── Dockerfile
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   └── health_check.py
│   │   ├── router.py
│   │   └── schemas
│   │       ├── __init__.py
│   │       └── health_check.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── error_handler.py
│   │   ├── logger.py
│   │   └── retry_strategy.py
│   ├── dependencies.py
│   ├── main.py
│   └── services
│       └── __init__.py
└── uv.lock
```

---

## ⚙️ Configuration

Create `.env` file:

```
APP_NAME=FastAPI Service
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
