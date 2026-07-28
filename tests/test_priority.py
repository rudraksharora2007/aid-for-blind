from src.navigation.priority import highest_priority
from src.vision.detector import Detection


def test_person_beats_small_objects():
    person = Detection("person", 0.9, (0, 0, 20, 100), distance_band="Far")
    cup = Detection("cup", 0.9, (0, 0, 20, 100), distance_band="Near")
    assert highest_priority([cup, person]) is person
