from src.config import DistanceConfig
from src.vision.distance import DistanceEstimator


def test_distance_uses_box_height_and_bands():
    estimator = DistanceEstimator(DistanceConfig(focal_length_pixels=700, known_object_heights_m={"person": 1.7}, near_meters=1.5, medium_meters=4))
    estimate = estimator.estimate("person", (0, 0, 100, 850))
    assert estimate.meters == 1.4
    assert estimate.band == "Near"


def test_zero_height_is_unknown():
    estimate = DistanceEstimator(DistanceConfig()).estimate("chair", (1, 2, 3, 2))
    assert estimate.meters is None
    assert estimate.band == "Unknown"
