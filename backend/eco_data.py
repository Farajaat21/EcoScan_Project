"""Tiny prototype functions to compute an environmental score for a product.

This module is intentionally simple: it returns a deterministic pseudo-score
based on the barcode string so you can exercise the API locally and with
Postman. Replace with real data lookups / ML model later.
"""
from typing import Tuple, Dict


def compute_score(barcode: str) -> Tuple[int, Dict[str, int]]:
	"""Return (score, breakdown) where score is 0-100 and breakdown is a
	simple dict of categories.

	The function uses the barcode string to produce deterministic but varied
	outputs for testing.
	"""
	if not barcode:
		return 0, {"carbon": 0, "water": 0, "other": 0}

	# Simple deterministic hash -> numbers
	s = sum(ord(c) for c in barcode)
	carbon = (s * 31) % 50  # 0-49
	water = (s * 17) % 30   # 0-29
	other = (s * 13) % 20   # 0-19
	score = max(0, 100 - (carbon + water + other))
	breakdown = {"carbon": carbon, "water": water, "other": other}
	return int(score), breakdown
