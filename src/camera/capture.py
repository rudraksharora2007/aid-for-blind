"""Reliable OpenCV camera capture wrapper."""
import cv2
import numpy as np
from src.config import CameraConfig


class Camera:
    """Open and read frames from a configured webcam."""
    def __init__(self, config: CameraConfig, logger):
        self.config, self.logger = config, logger
        self.capture: cv2.VideoCapture | None = None

    def open(self) -> bool:
        self.capture = cv2.VideoCapture(self.config.index)
        if not self.capture.isOpened():
            self.logger.error("Unable to open camera index %s", self.config.index)
            self.release()
            return False
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.config.fps)
        self.logger.info("Camera initialized (index %s)", self.config.index)
        return True

    def read(self) -> np.ndarray | None:
        if self.capture is None:
            return None
        ok, frame = self.capture.read()
        if not ok:
            self.logger.warning("Camera frame unavailable; camera may be disconnected")
            return None
        return frame

    def release(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None
