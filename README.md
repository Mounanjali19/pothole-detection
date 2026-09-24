# Pothole Detection & Mapping System

A Flask-based pothole detection application powered by a custom **YOLOv11n** object-detection model. Users can upload road images, detect potholes, view inference results, and visualize detected pothole locations on a dashboard.

## Features

- Pothole detection using a custom-trained YOLOv11n model
- Image upload through a Flask web interface
- Detection count used as a simple severity indicator
- Automatic approximate geolocation using IP-based location lookup
- Pothole metadata stored as JSON
- Interactive dashboard using Leaflet
- Separate output page showing model inference results
- Video-ingestion prototype using YOLO tracking

## Project Structure

```text
.
├── app.py
├── best.pt
├── python_file_for_video_ingestion.py
├── requirements.txt
├── templates/
│   ├── dashboard.html
│   ├── output.html
│   └── uploader.html
├── static/
│   ├── pothole_data.json
│   └── output_images/
├── inputs/
└── confusion_matrix.png
```

## Dataset & Training

The model was trained using a pothole image dataset sourced from Roboflow.

Roboflow dataset:
https://universe.roboflow.com/aimlprojects/pothole-detection-w3iq7-1msjv

Example training command used in Google Colab:

```bash
!yolo model=yolo11n.pt task=detect mode=train epochs=20 imgsz=640 data=location_of_dataset
```

The trained weights are included as `best.pt` for local inference.

## Installation

Use Python 3.10+ and create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

### Pages

- `/` or `/uploader` — upload an image and run detection
- `/dashboard` — view the pothole map/dashboard
- `/output` — view the latest detection output

## Video Detection Prototype

`python_file_for_video_ingestion.py` contains an OpenCV + YOLO tracking prototype for processing a video stream and classifying potholes into low, medium, or high severity based on detected bounding-box area relative to the frame area.

## Severity Logic

For the video prototype, severity is estimated from the bounding-box area:

```text
area_ratio = bounding_box_area / frame_area

area_ratio > 0.10  -> high
area_ratio > 0.02  -> medium
otherwise           -> low
```

This is a prototype heuristic rather than a clinical or engineering-grade road-condition measurement.

## Notes

- `best.pt` is the trained YOLO model used for inference.
- Runtime uploads and generated inference images are ignored by Git.
- The application uses IP-based geolocation, so location is approximate and depends on the external `ipinfo.io` service.
- For production deployment, debug mode should be disabled and stronger validation/storage should be added.
