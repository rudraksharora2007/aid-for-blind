"""Approximate monocular distance estimation."""
from dataclasses import dataclass
from src.config import DistanceConfig


@dataclass(frozen=True)
class DistanceEstimate:
    meters: float | None
    band: str


class DistanceEstimator:
    def __init__(self, config: DistanceConfig):
        self.config = config

    def estimate(self, label: str, box: tuple[int, int, int, int]) -> DistanceEstimate:
        pixel_height = max(0, box[3] - box[1])
        if pixel_height == 0:
            return DistanceEstimate(None, "Unknown")
        real_height = self.config.known_object_heights_m.get(label, self.config.default_object_height_m)
        meters = (real_height * self.config.focal_length_pixels) / pixel_height
        if meters <= self.config.near_meters:
            band = "Near"
        elif meters <= self.config.medium_meters:
            band = "Medium"
        else:
            band = "Far"
        return DistanceEstimate(round(meters, 2), band)
