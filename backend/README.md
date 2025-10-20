# EcoScan Backend (FastAPI)

This directory contains a lightweight FastAPI backend you can run locally and test with Postman or any HTTP client. It supports PostgreSQL via the `DATABASE_URL` environment variable, or falls back to a local sqlite file for quick testing.

Quick start (macOS / zsh):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# If using Postgres, set DATABASE_URL, e.g.:
# export DATABASE_URL=postgresql://user:password@localhost:5432/ecoscan_dev

# Run the app
python -m backend.server
```

Open Postman and issue a GET request:

GET http://127.0.0.1:5000/api/scan?barcode=012345

Or POST JSON to `/api/scan`:

POST http://127.0.0.1:5000/api/scan
Content-Type: application/json

{
  "barcode": "012345"
}

Notes:
- The current logic in `eco_data.py` is a simple deterministic placeholder. Replace with real data sources as needed.
- If you use Postgres, ensure `psycopg2-binary` is installed and `DATABASE_URL` is set before running.
