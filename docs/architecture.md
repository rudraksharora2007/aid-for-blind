# Architecture

VisionAssist deliberately keeps hardware and inference boundaries small:

1. `camera.capture.Camera` owns the OpenCV device and returns either a valid frame or `None`.
2. `vision.detector.ObjectDetector` owns Ultralytics and emits typed `Detection` values.
3. `vision.distance.DistanceEstimator` converts box height into an explicitly approximate distance.
4. `vision.tracker.ObjectTracker` assigns short-lived IDs using class-aware IoU matching.
5. `ocr.reader.TextReader` throttles EasyOCR and retains recent results between inference calls.
6. `navigation.priority` chooses the one event most worth speaking in the current frame.
7. `navigation.announcer.Announcer` applies cooldowns and generates spatial speech.
8. `speech.speaker.Speaker` keeps the UI loop responsive by speaking on a worker thread.

The application does not persist camera frames, OCR output, or audio. Model weights are supplied by Ultralytics and are ignored by Git.
