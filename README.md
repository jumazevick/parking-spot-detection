# Parking Spot Detection

A simple computer vision project that detects **free and occupied parking spaces** from a parking lot video using Python and OpenCV.

---

## How it Works

1. The program reads a parking lot video.
2. You **draw rectangles** around each parking space.
3. The program analyzes each spot and checks its brightness.
4. Each spot is labeled:

* 🟢 **Green** → Free parking spot
* 🔴 **Red** → Occupied parking spot

---

## Installation

Clone the repository:

```bash
git clone https://github.com/jumazevick/parking-spot-detection.git
cd parking-spot-detection
```

Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

1. Put your parking video inside the **data/** folder.

Example:

```
data/parking_video.mp4
```

2. Run the program:

```bash
python main.py
```

3. When the video opens:

* Click and drag to **draw parking spots**
* Press **S** to save the spots
* Press **Q** to quit

---

## Output

The program shows the parking spots on the video:

* 🟢 Green box = Free spot
* 🔴 Red box = Occupied spot

It also displays the **total number of parking spots and how many are free**.

---

## Project Structure

```
parking-spot-detection
│
├── data/              # Parking videos
├── detection/         # Detection logic
├── model/             # Saved models
├── main.py            # Main program
├── requirements.txt   # Python libraries
└── README.md
```

---

## Technologies Used

* Python
* OpenCV
* NumPy

---

## Purpose

This project was created for **learning computer vision and parking space detection**.

Possible improvements include:

* Machine learning detection
* Better lighting handling
* Real-time camera input
