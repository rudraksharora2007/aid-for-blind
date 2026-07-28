# Hardware

VisionAssist is built as a distributed wearable system with two devices: Smart
AI Glasses and a Smart Navigation Cane. A separate processing device performs
the computationally intensive computer-vision and AI work. This separation
keeps the wearable hardware small, power-efficient, and replaceable.

## System Overview

```text
Smart AI Glasses                 Processing Device                 Smart Navigation Cane
     ESP32-CAM  <──── Wi-Fi / BLE ────>  VisionAssist AI  <──── Wi-Fi / BLE ────>  ESP32-C3 Mini
  camera and audio I/O                 inference and logic                 sensors and haptics
```

The glasses capture and transmit camera frames to the processing device. The
processing device runs computer vision and AI models, combines visual results
with cane sensor data, and sends navigation commands to the cane. The cane
converts those commands into sensor updates and silent haptic feedback.

## Smart AI Glasses

The glasses use an **ESP32-CAM** as their primary controller.

| Component | Function |
| --- | --- |
| **ESP32-CAM** | Main controller; captures frames, streams images, handles Wi-Fi communication, and controls onboard peripherals. |
| **OV2640 camera** | Integrated with the ESP32-CAM; captures images for object detection, OCR, and scene understanding. |
| **MEMS microphone** | Captures voice commands and provides an input path for future speech-recognition support. |
| **Bone-conduction / open-ear speaker** | Provides audio feedback, navigation instructions, OCR reading, and scene descriptions while keeping the user aware of ambient sound. |
| **Li-ion battery** | Portable power source for the glasses electronics. |
| **TP4056 charging module** | Provides USB charging and battery protection. |

### Processing Boundary

The ESP32-CAM is responsible for **image acquisition and communication only**.
It captures images from the OV2640 and transfers them over Wi-Fi or BLE; it
does not need to run the AI inference pipeline. Inference can run on a
connected computer, Raspberry Pi, or a future edge AI device with suitable
acceleration. This boundary allows the camera hardware to remain inexpensive
while models can evolve independently.

## Smart Navigation Cane

The cane uses an **ESP32-C3 Mini** as its low-power controller.

### Controller Responsibilities

- Reads obstacle sensors.
- Controls haptic feedback.
- Sends sensor data to the glasses or processing device.
- Supports low-power operation.
- Provides Bluetooth and/or Wi-Fi communication.

### Hardware

| Component | Function |
| --- | --- |
| **HC-SR04 ultrasonic sensor** | Detects obstacles below camera height using ultrasonic ranging. |
| **VL53L0X ToF sensor** | Provides precise short-range distance measurements. |
| **Vibration motor** | Delivers silent haptic feedback for nearby obstacles and navigation alerts. |
| **Push button** | Supports emergency/SOS activation and manual interaction. |
| **RGB status LED** | Indicates battery status, connection status, and system state. |
| **Li-ion battery** | Portable power source for the cane electronics. |

## Communication

The preferred architecture uses the processing device as the coordination and
inference hub:

```text
ESP32-CAM
    │
    │ Wi-Fi / BLE
    ▼
Processing Device
    │
    │ Wi-Fi / BLE
    ▼
ESP32-C3 Mini
```

The processing device receives camera frames from the ESP32-CAM, runs
computer-vision and AI models, and sends navigation commands to the ESP32-C3
Mini. The cane reports sensor readings and receives feedback commands; the
ESP32-C3 Mini then controls the vibration motor, status LED, and local sensor
interfaces.

The exact transport and message format can be selected independently of the
hardware. Wi-Fi is suitable for higher-throughput image streaming, while BLE
is useful for low-power control and telemetry. A deployment may use either
protocol or both, depending on range, bandwidth, and power requirements.

## Hardware Responsibilities

| Subsystem | Responsibilities |
| --- | --- |
| **ESP32-CAM** | Camera control, image capture, video streaming, and wireless communication. |
| **ESP32-C3 Mini** | Sensor management, haptic feedback, obstacle detection, status LEDs, and emergency button handling. |
| **Processing Device** | YOLO object detection, OCR, scene understanding, navigation logic, and speech synthesis. |

## Advantages

This distributed architecture was chosen because it provides:

- **Low cost:** Commodity microcontrollers and sensors keep the entry cost low.
- **Lightweight design:** The wearables do not need a full computer or large cooling system.
- **Modularity:** Glasses, cane electronics, communication, and inference are separate modules.
- **Easy repair:** Individual sensors or controllers can be replaced without rebuilding the complete system.
- **Simple upgrades:** A more capable processing device or improved model can be added without redesigning the wearables.
- **Low power consumption:** The ESP32-C3 Mini can remain focused on sensing and event handling, while the glasses perform only capture and communication.
- **Distributed processing:** Camera acquisition, obstacle sensing, and AI inference are separated into clear responsibilities.
- **Future acceleration:** The processing-device boundary makes it straightforward to adopt a Raspberry Pi accelerator, NPU, GPU, or another edge AI platform.

## Bill of Materials

Prices are approximate Indian retail prices and vary by supplier, board
revision, battery capacity, and purchase quantity. The OV2640 is normally
bundled with an ESP32-CAM; its price is shown as a replacement/reference cost
and is not added a second time to the estimate.

| Component | Quantity | Approx. unit price (INR) | Estimated cost (INR) | Notes |
| --- | ---: | ---: | ---: | --- |
| ESP32-CAM | 1 | 700 | 700 | Primary glasses controller; typically includes OV2640. |
| ESP32-C3 Mini | 1 | 350 | 350 | Cane controller. |
| OV2640 camera | 1 | 250 | Included | Integrated with the ESP32-CAM; replacement price is approximately ₹250. |
| HC-SR04 ultrasonic sensor | 1 | 100 | 100 | Cane obstacle sensing. |
| VL53L0X ToF sensor | 1 | 350 | 350 | Short-range precision ranging. |
| MEMS microphone | 1 | 150 | 150 | Glasses voice input. |
| Bone-conduction speaker | 1 | 500 | 500 | Open-ear audio feedback. |
| Vibration motor | 1 | 30 | 30 | Cane haptic feedback. |
| TP4056 charging module | 2 | 30 | 60 | One charging/protection module per Li-ion battery. |
| Li-ion battery | 2 | 250 | 500 | One battery for the glasses and one for the cane. |
| Push button | 1 | 10 | 10 | Cane emergency/manual input. |
| RGB LED | 1 | 10 | 10 | Cane status indicator. |
| **Estimated hardware total** |  |  | **₹2,760** | Excludes enclosure, wiring, connectors, mounting hardware, and the processing device. |

The total includes two TP4056 modules, one for each battery. It excludes the
processing device because its price depends on whether the deployment uses an
existing computer, Raspberry Pi, or dedicated edge AI hardware.

## Power and Integration Notes

- The battery voltage, regulator requirements, and charging current should be
  verified against the selected ESP32-CAM, ESP32-C3 Mini, speaker, and sensor
  boards before assembly.
- The HC-SR04 is a 5 V module in many versions; use appropriate level shifting
  or a compatible supply when connecting it to the ESP32-C3 Mini.
- The vibration motor should be driven through a transistor or motor driver,
  not directly from a microcontroller GPIO pin.
- Battery protection and charging should be tested independently before the
  electronics are enclosed in the wearable devices.
