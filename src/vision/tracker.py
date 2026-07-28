"""A small IoU-based tracker for announcement de-duplication."""
from dataclasses import dataclass
from .detector import Detection


def iou(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> float:
    left, top = max(first[0], second[0]), max(first[1], second[1])
    right, bottom = min(first[2], second[2]), min(first[3], second[3])
    intersection = max(0, right - left) * max(0, bottom - top)
    area_a = max(0, first[2] - first[0]) * max(0, first[3] - first[1])
    area_b = max(0, second[2] - second[0]) * max(0, second[3] - second[1])
    union = area_a + area_b - intersection
    return intersection / union if union else 0.0


@dataclass
class _Track:
    label: str
    box: tuple[int, int, int, int]
    track_id: int
    missing: int = 0


class ObjectTracker:
    def __init__(self, threshold: float = 0.3, max_missing: int = 12):
        self.threshold, self.max_missing = threshold, max_missing
        self.tracks: list[_Track] = []
        self.next_id = 1

    def update(self, detections: list[Detection]) -> list[Detection]:
        used: set[int] = set()
        for detection in detections:
            candidates = [(iou(detection.box, track.box), index, track) for index, track in enumerate(self.tracks) if track.label == detection.label and index not in used]
            match = max(candidates, default=None, key=lambda item: item[0])
            if match and match[0] >= self.threshold:
                _, index, track = match
                track.box, track.missing = detection.box, 0
                detection.track_id = track.track_id
                used.add(index)
            else:
                track = _Track(detection.label, detection.box, self.next_id)
                self.next_id += 1
                self.tracks.append(track)
                detection.track_id = track.track_id
        for index, track in enumerate(self.tracks):
            if index not in used and not any(d.track_id == track.track_id for d in detections):
                track.missing += 1
        self.tracks = [track for track in self.tracks if track.missing <= self.max_missing]
        return detections
