"""Priority ordering for useful spoken events."""
from src.vision.detector import Detection


PRIORITIES = {"person": 100, "car": 95, "bus": 95, "motorcycle": 95, "bicycle": 90, "stairs": 85, "dog": 75, "cat": 60, "backpack": 55, "obstacle": 50, "chair": 35, "bottle": 20, "cup": 15}


def priority_for(detection: Detection) -> int:
    """Return priority, increasing with likely navigation importance."""
    value = PRIORITIES.get(detection.label, 10)
    if detection.distance_band == "Near":
        value += 15
    return value


def highest_priority(detections: list[Detection]) -> Detection | None:
    return max(detections, key=priority_for, default=None)
