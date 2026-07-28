"""Ultralytics YOLO detection adapter."""
from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np


TARGET_LABELS = {"person", "chair", "bicycle", "car", "bus", "motorcycle", "dog", "cat", "bottle", "cup", "backpack", "stairs"}


@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple[int, int, int, int]
    track_id: int | None = None
    distance_m: float | None = None
    distance_band: str = "Unknown"
    position: str = "center"


class ObjectDetector:
    """Load a YOLO model and convert its output to stable project objects."""
    def __init__(self, model_path: str, confidence: float, iou: float, device: str, logger):
        self.confidence, self.iou, self.device, self.logger = confidence, iou, device, logger
        self.model = None
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.logger.info("Model loaded: %s", model_path)
        except Exception as exc:
            self.logger.error("Could not load YOLO model %s: %s", model_path, exc)

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if self.model is None:
            return []
        try:
            kwargs = {"conf": self.confidence, "iou": self.iou, "verbose": False}
            if self.device != "auto":
                kwargs["device"] = self.device
            result = self.model.predict(frame, **kwargs)[0]
            names = result.names
            detections = []
            for box in result.boxes:
                label = str(names[int(box.cls[0])]).lower()
                if label not in TARGET_LABELS:
                    continue
                x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].tolist())
                detections.append(Detection(label, float(box.conf[0]), (x1, y1, x2, y2)))
            return detections
        except Exception as exc:
            self.logger.warning("YOLO inference failed: %s", exc)
            return []

    @staticmethod
    def annotate(frame: np.ndarray, detections: list[Detection], fps: float) -> np.ndarray:
        for item in detections:
            x1, y1, x2, y2 = item.box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (40, 220, 100), 2)
            distance = f" {item.distance_m:.1f}m" if item.distance_m is not None else ""
            text = f"{item.label} {item.confidence:.0%}{distance} {item.distance_band}"
            cv2.putText(frame, text, (x1, max(y1 - 8, 18)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 220, 100), 2)
        cv2.putText(frame, f"FPS: {fps:.1f}", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 255), 2)
        return frame
