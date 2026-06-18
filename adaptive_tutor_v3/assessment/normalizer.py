from __future__ import annotations

from difflib import SequenceMatcher
from fractions import Fraction
import re


def normalize_text(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


def try_parse_fraction(value: str):
    cleaned = normalize_text(value)
    match = re.fullmatch(r"(-?\d+)\s*/\s*(-?\d+)", cleaned)
    if not match:
        return None
    return Fraction(int(match.group(1)), int(match.group(2)))


def semantic_match(left: str, right: str) -> float:
    left_n = normalize_text(left)
    right_n = normalize_text(right)
    if left_n == right_n:
        return 1.0
    left_frac = try_parse_fraction(left_n)
    right_frac = try_parse_fraction(right_n)
    if left_frac is not None and right_frac is not None:
        return 1.0 if left_frac == right_frac else 0.0
    return SequenceMatcher(None, left_n, right_n).ratio()
