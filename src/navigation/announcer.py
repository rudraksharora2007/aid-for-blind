"""Turn prioritized detections and OCR into throttled speech."""
import time
from src.vision.detector import Detection
from src.utils.helpers import position_for_box


class Announcer:
    def __init__(self, speaker, cooldown: float, repeat_seconds: float, logger):
        self.speaker, self.cooldown, self.repeat_seconds, self.logger = speaker, cooldown, repeat_seconds, logger
        self.last_time = 0.0
        self.last_key: tuple[str, int | None] | None = None
        self.last_text = ""
        self.last_text_time = 0.0

    def announce(self, detection: Detection, frame_width: int) -> bool:
        now = time.monotonic()
        key = (detection.label, detection.track_id)
        if now - self.last_time < self.cooldown and key == self.last_key:
            return False
        if key == self.last_key and now - self.last_time < self.repeat_seconds:
            return False
        side = position_for_box(detection.box, frame_width)
        if detection.label == "person":
            phrase = "Person approaching" if detection.distance_band == "Near" else "Person ahead"
        else:
            phrase = f"{detection.label.capitalize()}"
        suffix = " ahead" if side == "center" else f" on your {side}"
        self.speaker.speak(phrase + suffix + ".")
        self.last_time, self.last_key = now, key
        return True

    def announce_text(self, text: str) -> bool:
        """Speak a newly observed OCR string once during the cooldown window."""
        now = time.monotonic()
        if text == self.last_text and now - self.last_text_time < self.repeat_seconds:
            return False
        self.speaker.speak(f"Text ahead: {text}.")
        self.last_text, self.last_text_time = text, now
        return True
