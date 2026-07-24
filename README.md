# Threat Detection using Pose & FaceMesh

This project is a real-time computer vision prototype that detects possible threat-like postures using MediaPipe Pose, MediaPipe FaceMesh, and OpenCV.

Developed by Noorullah Zamindar as a side project in computer vision.

## Demo

![Demo](https://github.com/abhijeet1592006/threat-detector/blob/main/demo.gif)

## Features

- Real-time webcam capture with OpenCV.
- Full-body pose estimation with MediaPipe Pose.
- Face landmark detection with MediaPipe FaceMesh.
- Threat posture logic based on left shoulder and arm angles.
- On-screen game-style "GAME LOCKED" and "NO LOCK" labels.
- Crosshair-style visual indicator on the face landmark when a threat posture is detected.
- Clickable game overlay button that reduces virtual target HP while locked.

## Technologies Used

- Python 3
- OpenCV
- MediaPipe

## Project Structure

```text
threat-detector-main/
  app.py            # Core detection logic
  requirements.txt  # Python dependencies
  README.md         # Project documentation
  demo.gif          # Demo animation
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Press `q` to quit the webcam window.

You can adjust the detection thresholds:

```bash
python app.py --shoulder-threshold -20 --arm-threshold 15
```

You can adjust the game overlay damage:

```bash
python app.py --game-damage 10
```

Use `--camera 1` if your webcam is not camera `0`.

Game controls:

- Get a game lock using the detected pose.
- Click the on-screen `FIRE` button while locked.
- Each click reduces virtual HP until `TARGET DOWN`.
- Press `q` to quit.

## How It Works

The webcam feed is processed frame by frame. Pose landmarks are used to calculate shoulder, elbow, wrist, and hip positions. FaceMesh landmarks are used to locate the face. If the left arm and shoulder angles match the prototype game-lock posture, the app displays a lock label and draws a marker on the face. The `FIRE` button only affects virtual HP inside the demo.

## Note

This is only a computer vision prototype. It may be inaccurate and must not be used for real security, safety, law enforcement, or threat decisions.

## Author

Noorullah Zamindar
