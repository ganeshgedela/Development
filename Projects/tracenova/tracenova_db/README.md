# 📦 Tracenova DB Service

Tracenova DB is a FastAPI microservice for storing and managing parsed network trace data from PCAPs, logs, KPIs, and CDRs. It supports modular protocols like packets, SIP, and trace file metadata.

---

## 🗂️ Project Structure

## 📁 Directory Structure

```
tracenova_db/
│
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── models/                  # SQLAlchemy models
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── crud/                    # Business logic and DB access
│   ├── routers/                 # API route definitions
│   ├── database/
│   │   ├── engine.py            # DB engine, session setup
│   │   └── __init__.py
│   └── tests/                   # Unit tests
│
├── Dockerfile                  # Web service Dockerfile
├── docker-compose.yml          # Combined DB + API stack
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation
```
---

## ⚙️ Configuration

Set the following environment variables via `.env` or Docker `env:`:
```env
DB_ENGINE=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=tracenova
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## 🚀 Build and Run

### 🐳 Using Docker Compose

```bash
# Build the containers
sudo docker compose build --no-cache

# Start the services
sudo docker compose up -d
```

- Backend accessible at: `http://localhost:8000`
- Swagger docs at: `http://localhost:8000/docs`

---
# Clean up
docker compose down -v

# Rebuild from scratch
docker compose build --no-cache

# Launch again
docker compose up -d

## 🧪 Running Unit Tests

```bash
# Run from container
sudo docker compose exec web pytest app/tests

# To test specific file
sudo docker compose exec web pytest app/tests/test_packet_api.py
```

Tests exist for:

- `Packet` API (`test_packet_api.py`)
- `SIP Packet` API (`test_sip_packet_api.py`)
- `Trace File Metadata` API (`test_trace_file_api.py`)
- `Client API Logic` (`test_tracenova_db_client.py`)

---

## 📘 API Endpoints Overview

### ➤ Packet APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/packet/` | POST | Create a packet |
| `/packet/` | GET  | List all packets |
| `/packet/{id}` | GET/DELETE | Get/Delete packet by ID |
| `/packet/range/` | GET | List packets in ID range |

### ➤ SIP Packet APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sip-packet/` | POST | Create SIP packet |
| `/sip-packet/` | GET  | List all SIP packets |
| `/sip-packet/{id}` | GET/DELETE | Get/Delete SIP packet by ID |
| `/sip-packet/range/` | GET | Range by ID |
| `/sip-packet/search/` | GET | Filter by `call_id` or `timestamp` |

### ➤ Trace File Metadata APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/trace-file/` | POST | Upload new trace file metadata |
| `/trace-file/` | GET | List uploaded files |
| `/trace-file/{id}` | GET/DELETE | Get/Delete by ID |

---

## 🧱 Architecture Overview

The following image illustrates Tracenova DB architecture:

![Architecture Diagram](./A_digital_diagram_in_the_image_illustrates_the_arc.png)

---

## 🧩 Tech Stack

- Python 3.11 + FastAPI
- SQLAlchemy ORM
- PostgreSQL (via Docker)
- Pydantic v2
- Pytest

---

## 🔧 Notes

- `Base.metadata.create_all()` is run on startup to auto-create tables
- Pydantic v2 is used (`model_dump()`, `ConfigDict`)
- Schema aliasing is enabled using `Field(..., alias=...)` with `populate_by_name = True`