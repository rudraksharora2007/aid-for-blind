"""VisionAssist application entry point."""
from __future__ import annotations
import argparse
import time
import cv2
from src.camera.capture import Camera
from src.config import load_config
from src.navigation.announcer import Announcer
from src.navigation.priority import highest_priority
from src.ocr.reader import TextReader
from src.speech.speaker import Speaker
from src.utils.logger import configure_logging
from src.utils.helpers import position_for_box
from src.vision.detector import ObjectDetector
from src.vision.distance import DistanceEstimator
from src.vision.tracker import ObjectTracker


def run(config_path: str = "config.yaml") -> int:
    config = load_config(config_path)
    logger = configure_logging(config.logging.level)
    camera = Camera(config.camera, logger)
    if not camera.open():
        return 1
    detector = ObjectDetector(config.model.path, config.model.confidence_threshold, config.model.iou_threshold, config.model.device, logger)
    estimator = DistanceEstimator(config.distance)
    tracker = ObjectTracker(config.tracking.iou_threshold, config.tracking.max_missing_frames)
    reader = TextReader(config.ocr.languages, config.ocr.min_text_height, config.ocr.confidence_threshold, config.ocr.interval_seconds, config.ocr.cache_seconds, logger) if config.ocr.enabled else None
    speaker = Speaker(config.speech.enabled, config.speech.rate, config.speech.volume, logger)
    announcer = Announcer(speaker, config.speech.cooldown_seconds, config.speech.repeat_seconds, logger)
    cv2.namedWindow("VisionAssist", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("VisionAssist", config.camera.window_width, config.camera.window_height)
    speech_enabled, ocr_enabled, previous = config.speech.enabled, config.ocr.enabled, time.monotonic()
    fps = 0.0
    try:
        while True:
            frame = camera.read()
            if frame is None:
                break
            detections = tracker.update(detector.detect(frame))
            for detection in detections:
                estimate = estimator.estimate(detection.label, detection.box)
                detection.distance_m, detection.distance_band = estimate.meters, estimate.band
                detection.position = position_for_box(detection.box, frame.shape[1])
            selected = highest_priority(detections)
            if selected is not None and speech_enabled:
                announcer.announce(selected, frame.shape[1])
            if reader is not None and ocr_enabled:
                text_results = reader.read(frame)
                for result in text_results:
                    cv2.rectangle(frame, (result.box[0], result.box[1]), (result.box[2], result.box[3]), (255, 180, 0), 2)
                    cv2.putText(frame, result.text, (result.box[0], result.box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 180, 0), 2)
                    if speech_enabled:
                        announcer.announce_text(result.text)
            now = time.monotonic()
            elapsed = now - previous
            fps = 1 / elapsed if elapsed else fps
            previous = now
            cv2.imshow("VisionAssist", detector.annotate(frame, detections, fps))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s"):
                speech_enabled = not speech_enabled
                speaker.enabled = speech_enabled
                logger.info("Speech %s", "enabled" if speech_enabled else "disabled")
            if key == ord("o") and reader is not None:
                ocr_enabled = not ocr_enabled
                logger.info("OCR %s", "enabled" if ocr_enabled else "disabled")
    except KeyboardInterrupt:
        logger.info("Stopping VisionAssist")
    finally:
        camera.release()
        speaker.close()
        cv2.destroyAllWindows()
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline visual assistance from a webcam")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML configuration")
    args = parser.parse_args()
    raise SystemExit(run(args.config))


if __name__ == "__main__":
    main()
