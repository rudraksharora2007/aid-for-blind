"""Typed configuration loading for VisionAssist."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


@dataclass
class CameraConfig:
    index: int = 0
    width: int = 1280
    height: int = 720
    fps: int = 30
    window_width: int = 1280
    window_height: int = 720


@dataclass
class ModelConfig:
    path: str = "yolo11n.pt"
    confidence_threshold: float = 0.45
    iou_threshold: float = 0.45
    device: str = "auto"


@dataclass
class SpeechConfig:
    enabled: bool = True
    cooldown_seconds: float = 4.0
    repeat_seconds: float = 12.0
    rate: int = 165
    volume: float = 1.0


@dataclass
class OCRConfig:
    enabled: bool = True
    languages: list[str] = field(default_factory=lambda: ["en"])
    interval_seconds: float = 2.5
    cache_seconds: float = 5.0
    min_text_height: int = 14
    confidence_threshold: float = 0.35


@dataclass
class DistanceConfig:
    focal_length_pixels: float = 700.0
    default_object_height_m: float = 1.0
    known_object_heights_m: dict[str, float] = field(default_factory=dict)
    near_meters: float = 1.5
    medium_meters: float = 4.0


@dataclass
class TrackingConfig:
    max_missing_frames: int = 12
    iou_threshold: float = 0.3


@dataclass
class LoggingConfig:
    level: str = "INFO"


@dataclass
class AppConfig:
    camera: CameraConfig = field(default_factory=CameraConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    ocr: OCRConfig = field(default_factory=OCRConfig)
    distance: DistanceConfig = field(default_factory=DistanceConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def _section(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name, {})
    return value if isinstance(value, dict) else {}


def load_config(path: str | Path = "config.yaml") -> AppConfig:
    """Load YAML configuration, retaining dataclass defaults for omissions."""
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig()
    with config_path.open(encoding="utf-8") as stream:
        raw = yaml.safe_load(stream) or {}
    return AppConfig(
        camera=CameraConfig(**_section(raw, "camera")),
        model=ModelConfig(**_section(raw, "model")),
        speech=SpeechConfig(**_section(raw, "speech")),
        ocr=OCRConfig(**_section(raw, "ocr")),
        distance=DistanceConfig(**_section(raw, "distance")),
        tracking=TrackingConfig(**_section(raw, "tracking")),
        logging=LoggingConfig(**_section(raw, "logging")),
    )
