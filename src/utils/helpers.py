"""Small geometry and text helpers."""
import re
from typing import Iterable


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def clean_text(text: str) -> str:
    """Normalize OCR text into a concise, speakable string."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s.,!?%:/'-]", "", text)).strip()


def position_for_box(box: tuple[int, int, int, int], frame_width: int) -> str:
    """Classify a box by its horizontal center."""
    center = (box[0] + box[2]) / 2
    if center < frame_width / 3:
        return "left"
    if center > frame_width * 2 / 3:
        return "right"
    return "center"


def average(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
