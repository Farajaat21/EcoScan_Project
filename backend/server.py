from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import os

# Support running the file as a module (python -m backend.server) or as a
# script (python server.py). When run as a script, relative imports fail, so
# fall back to absolute imports from the same directory.
try:
	# Preferred when run as package from repo root: `python -m backend.server`
	from . import eco_data
	from .database import SessionLocal, engine
	from . import models
except Exception:
	# Fallback when running `python server.py` inside the backend/ folder
	import eco_data
	from database import SessionLocal, engine
	import models

from fastapi.middleware.cors import CORSMiddleware

# Create database tables (simple approach for prototype)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoScan API")

# Allow CORS for local frontend development — restrict in production
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class ScanRequest(BaseModel):
	barcode: str


class ScanResponse(BaseModel):
	barcode: str
	score: int
	breakdown: Dict[str, int]


@app.get("/api/scan", response_model=ScanResponse)
def scan_get(barcode: str):
	"""Compute a sustainability score for a barcode (quick prototype).

	You can call this from Postman as GET /api/scan?barcode=012345
	"""
	if not barcode:
		raise HTTPException(status_code=400, detail="barcode query parameter is required")

	score, breakdown = eco_data.compute_score(barcode)
	return {"barcode": barcode, "score": score, "breakdown": breakdown}


@app.post("/api/scan", response_model=ScanResponse)
def scan_post(r: ScanRequest):
	"""POST JSON { "barcode": "..." } to compute a score."""
	score, breakdown = eco_data.compute_score(r.barcode)
	return {"barcode": r.barcode, "score": score, "breakdown": breakdown}


if __name__ == "__main__":
	import uvicorn

	# Run using the app object so the script can be executed directly from
	# the `backend/` directory (`python server.py`) or from the repo root
	# (`python -m backend.server`). When using `-m` make sure you run from
	# the repository root so the `backend` package can be located.
	uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", 8000)), reload=True)
