# OpenCV Color Change Detection System 🎨

## Overview

This project is a computer vision solution developed using Python and OpenCV for detecting color changes in real time.

The project evolved through multiple development iterations, beginning with basic color detection and progressing into a complete color change detection system capable of monitoring a Region of Interest (ROI), recording video evidence, tracking detection duration, and automatically terminating after configurable inactivity periods.

The repository includes both the final implementation and the intermediate development stages that demonstrate the engineering process behind the solution.

## Demo Video

https://www.youtube.com/watch?v=j5ihSZjRxy4

## Features

* Real-time webcam processing
* HSV-based color detection
* Region of Interest (ROI) monitoring
* Color change detection
* Automatic video recording
* Automatic recording stop after detection
* Detection timeout handling
* Video duration calculation
* Unit testing
* Multiple color detection experiments

## Technologies Used

* Python
* OpenCV
* NumPy
* unittest
* Computer Vision
* Image Processing

## Project Evolution

### Iteration 1 - Yellow Color Detection

Implemented a color detection algorithm using the HSV color space to identify yellow objects in a live camera stream.

Key concepts:

* HSV thresholding
* Noise reduction
* Contour detection
* Object highlighting

File:

* `archive/yellow_color_detection.py`

---

### Iteration 2 - Region of Interest (ROI)

Introduced a configurable Region of Interest (ROI) to focus processing on a specific section of the camera image.

Benefits:

* Reduced processing overhead
* Improved detection accuracy
* Better control over monitored areas

File:

* `archive/roi_color_detection.py`

---

### Iteration 3 - Multiple Color Detection

Expanded the solution to support multiple color detection experiments and evaluate different color classification approaches.

File:

* `archive/multi_color_detection.py`

---

### Iteration 4 - IoT Integration

Integrated the computer vision solution with:

* MQTT messaging
* CouchDB database storage
* Serial communication
* Video playback functionality

This stage explored how the color detection system could be integrated into a larger IoT ecosystem.

File:

* `archive/integrated_detection_system.py`

---

### Final Implementation - Color Change Detection System

The final implementation detects a predefined color inside an ROI and continuously monitors for color changes.

Capabilities:

* Detect predefined target color
* Monitor color disappearance or change
* Record video automatically
* Stop recording 10 seconds after a color change
* Stop program after prolonged inactivity
* Calculate recording duration
* Save video evidence for later analysis

File:

* `src/color_change_detection.py`

## How It Works

1. Camera captures live video.
2. A predefined ROI is extracted from each frame.
3. The ROI is converted from BGR to HSV color space.
4. HSV thresholds are applied to isolate the target color.
5. The percentage of matching pixels is calculated.
6. The system determines whether the expected color is present.
7. When the color changes or disappears:

   * A detection event is triggered.
   * Video recording continues for a predefined duration.
   * Evidence is saved automatically.
8. The application exits after a configurable timeout period if no color changes occur.

## Project Structure

```text
opencv-color-change-detection/
│
├── src/
│   └── color_change_detection.py
│
├── archive/
│   ├── yellow_color_detection.py
│   ├── roi_color_detection.py
│   ├── multi_color_detection.py
│   ├── integrated_detection_system.py
│   └── video_duration_tracker.py
│
├── tests/
│   ├── test_yellow_detection.py
│   └── test_color_change_detection.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python numpy
```

## Running the Final Solution

```bash
python src/color_change_detection.py
```

## Running Tests

```bash
python tests/test_yellow_detection.py
python tests/test_color_change_detection.py
```

## Applications

* Chemical reaction monitoring
* Laboratory automation
* Industrial inspection
* Quality assurance systems
* Automated visual monitoring
* Computer vision research

## Future Improvements

* Machine learning based color classification
* Adaptive thresholding
* Cloud data storage
* Dashboard visualization
* Real-time notifications
* Multi-camera support

## Author

Paras Khosla

ICT Engineer | Embedded Systems | Computer Vision | Cloud & DevOps
