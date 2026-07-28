from src.vision.detector import Detection
from src.vision.tracker import ObjectTracker, iou


def test_iou_and_id_stability():
    assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    tracker = ObjectTracker(threshold=0.3)
    first = tracker.update([Detection("person", 0.9, (0, 0, 100, 100))])[0]
    second = tracker.update([Detection("person", 0.9, (5, 5, 105, 105))])[0]
    assert first.track_id == second.track_id


def test_different_labels_do_not_match():
    tracker = ObjectTracker()
    person = tracker.update([Detection("person", 0.9, (0, 0, 100, 100))])[0]
    chair = tracker.update([Detection("chair", 0.9, (0, 0, 100, 100))])[0]
    assert person.track_id != chair.track_id
