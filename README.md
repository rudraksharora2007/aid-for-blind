# VisionAssist

VisionAssist is an offline-first computer-vision assistant for a wearable camera. It combines webcam capture, Ultralytics YOLO object detection, approximate monocular distance estimation, EasyOCR, and offline `pyttsx3` speech to surface the most useful information around a visually impaired user.

## Features

- Continuous webcam capture with camera selection and graceful disconnect handling.
- YOLO11 (or YOLOv8) detection for people, vehicles, animals, common obstacles, and other useful objects.
- Approximate distance in metres plus `Near`, `Medium`, and `Far` ranges.
- EasyOCR text extraction with result caching and tiny-text filtering.
- Priority-based announcements, spatial language, cooldowns, and lightweight IoU tracking.
- Keyboard controls: `Q` quit, `S` toggle speech, `O` toggle OCR.
- Rich logging and a YAML configuration file.

## Architecture

`src/main.py` owns the frame pipeline: camera -> detector -> distance -> OCR -> priority/announcement -> display. Each stage is isolated in a small module under `src/`, making hardware and model integrations straightforward to replace or test.

## Installation

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

The first run may download the configured Ultralytics weights. EasyOCR may also download language data on first use. Both are cached by their respective libraries.

## Usage

Connect a webcam and run:

```bash
python src/main.py
```

Edit `config.yaml` to select another camera, tune confidence/cooldowns, disable OCR, or calibrate distance. A camera or model that cannot be opened is reported clearly and the application exits cleanly rather than fabricating results.

## Configuration

The checked-in configuration is intentionally conservative. `distance.focal_length_pixels` and `distance.known_object_heights_m` are approximate defaults; calibrate them for the camera and objects you use. The `model.path` can be changed to a local YOLO11 or YOLOv8 `.pt` file.

## Roadmap

- Depth-camera and stereo-camera support.
- More robust multi-object tracking with motion prediction.
- Configurable wake-word and haptic feedback.
- Small-device acceleration and quantized models.

## Contributing

Create a focused branch, make the smallest complete change, add or update tests, and run `pytest`. Contributions should preserve offline operation and should never expose camera frames or OCR text by default.

## License

VisionAssist is released under the MIT License. See `LICENSE`.

## Future Work

Distance estimation from a single RGB camera is inherently approximate. Production wearable deployments should validate it against the intended camera mount and add a depth sensor where safety-critical accuracy is required.
