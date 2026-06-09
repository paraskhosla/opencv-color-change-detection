# OpenCV Color Change Detection System 🎨

## Overview

This project was developed as a computer vision solution for detecting color changes in real time using Python and OpenCV.

The project evolved through multiple development sprints, starting with simple color recognition and progressing toward a complete color change detection system capable of monitoring a Region of Interest (ROI), recording video evidence, tracking detection duration, and automatically terminating after a configurable timeout period.

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

### Sprint 2 - Yellow Color Detection

Implemented a color detection algorithm using the HSV color space to identify yellow objects in a live camera stream.

Key concepts:

* HSV thresholding
* Noise reduction
* Contour detection
* Object highlighting

File:

* Yellow_color_detection_using_OpenCV_Sprint_2.py

---

### Sprint 3 - Region of Interest (ROI)

Introduced a configurable Region of Interest (ROI) to focus processing on a specific section of the camera image.

Benefits:

* Reduced processing overhead
* Improved detection accuracy
* Better control over monitored area

File:

* ROI_using_OpenCV_sprint_3.py

---

### Sprint 4 - Multiple Color Detection

Expanded the system to support multiple color detection experiments and evaluate different color classification approaches.

File:

* Multiple color detection.py

---

### Sprint 5 - Final Color Change Detection System

The final implementation detects a predefined color inside an ROI and monitors for color changes.

Capabilities:

* Detect predefined target color
* Monitor color disappearance/change
* Record video automatically
* Stop recording 10 seconds after a color change
* Stop program after prolonged inactivity
* Calculate and display recording duration
* Save video evidence for later analysis

File:

* Color_change_detection_sprint_5.py

## How It Works

1. Camera captures live video.
2. A predefined ROI is extracted from each frame.
3. The ROI is converted from BGR to HSV color space.
4. Color thresholds are applied to isolate the target color.
5. The percentage of matching pixels is calculated.
6. The system determines whether the expected color is present.
7. When the color changes or disappears:

   * A detection event is triggered.
   * Video recording continues for 10 seconds.
   * Evidence is saved automatically.
8. The application exits after a configurable timeout period if no color changes occur.

## Project Structure

```text
opencv-color-detection/
│
├── Main.py
├── Yellow_color_detection_using_OpenCV_Sprint_2.py
├── ROI_using_OpenCV_sprint_3.py
├── Multiple color detection.py
├── Color_change_detection_sprint_5.py
├── Testing duration.py
│
├── Unit_Test_yellow.py
├── Unit_Test_color_change_detection.py
│
└── README.md
```

## Installation

Install dependencies:

```bash
pip install opencv-python numpy
```

## Running the Final Solution

```bash
python Color_change_detection_sprint_5.py
```

## Running Tests

```bash
python Unit_Test_yellow.py
python Unit_Test_color_change_detection.py
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
