# VisionAssist
### AI-Powered Wearable Navigation System for the Visually Impaired

> An open-source wearable assistant that uses computer vision, OCR, depth estimation, and speech synthesis to help blind and visually impaired individuals navigate the world independently.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-green.svg)
![Status](https://img.shields.io/badge/status-Active%20Development-orange)

---

## Inspiration

Over **285 million people worldwide** live with visual impairments, yet most assistive technologies remain expensive, proprietary, or limited in functionality.

VisionAssist aims to change that.

This project explores how modern AI models can be combined with affordable hardware to create an intelligent wearable capable of understanding the surrounding environment and communicating useful information in real time.

The long-term goal is to make advanced assistive technology accessible to everyone.

---

## Features

### 🚶 Intelligent Navigation
- Detects obstacles in real time
- Estimates distance to nearby objects
- Warns about hazards
- Identifies safe walking paths

### 📝 OCR & Reading Assistance
- Reads printed text aloud
- Detects signs, labels, menus and documents
- Supports multilingual text recognition

### 🎯 Object Recognition
- Identifies common everyday objects
- Announces objects using natural speech
- Provides contextual descriptions

### 🧍 Human Detection
- Detects nearby people
- Estimates relative position
- Announces approaching pedestrians

### 💬 Voice Interface
- Hands-free interaction
- Speech-to-text commands
- Natural language responses
- Text-to-speech output

### 🧠 AI Scene Understanding
- Describes surroundings
- Explains complex environments
- Answers questions about what the camera sees

---

# Project Architecture

```
Camera
   │
   ▼
Image Capture
   │
   ├──────────────► Object Detection
   │
   ├──────────────► OCR
   │
   ├──────────────► Depth Estimation
   │
   ├──────────────► Scene Analysis
   │
   ▼
Decision Engine
   │
   ▼
Priority Manager
   │
   ▼
Speech Generation
   │
   ▼
User
```

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Computer Vision | OpenCV |
| AI Models | YOLO, Vision Language Models |
| OCR | EasyOCR / PaddleOCR |
| Speech Recognition | Whisper |
| Text-to-Speech | Piper / Coqui TTS |
| Hardware | Raspberry Pi / Jetson / USB Camera |
| Interface | Voice First |

---

# Why Open Source?

Most wearable assistive devices cost hundreds or even thousands of dollars.

VisionAssist is built with the belief that accessibility should not be a luxury.

Making the project open source allows:

- researchers to improve detection accuracy
- developers to contribute new features
- makers to build affordable devices
- students to learn practical AI
- organizations to deploy localized solutions

---

# Current Goals

- [ ] Real-time obstacle detection
- [ ] OCR pipeline
- [ ] Voice assistant
- [ ] Scene description
- [ ] Navigation guidance
- [ ] Raspberry Pi optimization
- [ ] Offline inference
- [ ] Mobile companion app

---

# Future Roadmap

### Navigation
- Indoor navigation
- GPS integration
- Public transport assistance

### AI

- Personalized guidance
- Context-aware assistance
- Memory of familiar locations
- Face recognition (optional)

### Accessibility

- Multiple language support
- Low-power mode
- Offline-first operation
- Community datasets

---

# Example Workflow

1. User wears the device.
2. Camera continuously captures surroundings.
3. AI detects important objects and obstacles.
4. Text and signs are recognized using OCR.
5. Scene is summarized.
6. Critical information is prioritized.
7. Audio feedback is delivered through earphones.

Example:

> "Person approaching from your left."

> "Stairs detected three meters ahead."

> "Exit sign directly in front."

> "Chair on your right."

---

# Contributing

Contributions are always welcome.

Whether you're interested in:

- AI
- Computer Vision
- Embedded Systems
- Accessibility
- Hardware
- Documentation

feel free to open an Issue or submit a Pull Request.

---

# Why I'm Building This

This project began as a personal challenge to explore how modern AI can solve meaningful real-world problems beyond chat interfaces.

Rather than creating another AI application, I wanted to build something that could genuinely improve independence for visually impaired users using affordable hardware and open-source software.

This repository serves as both a learning platform and a long-term effort toward practical, accessible assistive technology.

---

# License

MIT License

---

## Acknowledgements

Thanks to the open-source community and the researchers behind projects including:

- OpenCV
- YOLO
- Whisper
- EasyOCR
- PaddleOCR
- Piper TTS
- Coqui TTS

whose work makes projects like VisionAssist possible.

---

**If this project interests you, consider giving it a ⭐. Every contribution helps move accessible AI forward.**
