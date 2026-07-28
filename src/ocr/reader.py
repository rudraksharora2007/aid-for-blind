"""EasyOCR adapter with interval and result caching."""
from dataclasses import dataclass
import time
import cv2
import numpy as np
from src.utils.helpers import clean_text


@dataclass(frozen=True)
class TextResult:
    text: str
    confidence: float
    box: tuple[int, int, int, int]


class TextReader:
    def __init__(self, languages: list[str], min_height: int, confidence: float, interval: float, cache_seconds: float, logger):
        self.min_height, self.confidence, self.interval, self.cache_seconds, self.logger = min_height, confidence, interval, cache_seconds, logger
        self.reader = None
        self.last_run = 0.0
        self.last_success = 0.0
        self.cached: list[TextResult] = []
        try:
            import easyocr
            self.reader = easyocr.Reader(languages, gpu=False, verbose=False)
            self.logger.info("OCR initialized (%s)", ", ".join(languages))
        except Exception as exc:
            self.logger.warning("OCR unavailable: %s", exc)

    def read(self, frame: np.ndarray) -> list[TextResult]:
        now = time.monotonic()
        if now - self.last_run < self.interval:
            return self.cached
        self.last_run = now
        if self.reader is None:
            return []
        try:
            results = []
            for polygon, text, confidence in self.reader.readtext(frame):
                points = np.asarray(polygon, dtype=np.int32)
                x1, y1 = points.min(axis=0).tolist()
                x2, y2 = points.max(axis=0).tolist()
                if y2 - y1 < self.min_height or confidence < self.confidence:
                    continue
                cleaned = clean_text(text)
                if cleaned:
                    results.append(TextResult(cleaned, float(confidence), (x1, y1, x2, y2)))
            self.cached = results
            self.last_success = now
            return results
        except Exception as exc:
            self.logger.warning("OCR failed: %s", exc)
            return self.cached if now - self.last_success < self.cache_seconds else []
