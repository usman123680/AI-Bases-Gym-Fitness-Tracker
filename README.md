# 🏋️ AI-Powered Gym Fitness Tracker

An intelligent, real-time fitness tracking application that uses **computer vision**, **pose estimation**, and **AI chatbot integration** to deliver a personal trainer experience — right from your webcam.

> Built by **Zain Ul Abideen** (2023-CS-826) & **Usman Nazar** (2023-CS-823)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Supported Exercises](#supported-exercises)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Results & Performance](#results--performance)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [References](#references)

---

## Overview

The AI-Powered Gym Fitness Tracker bridges the gap between **accessible technology** and **intelligent fitness coaching**. Using only a standard webcam, the system can:

- Detect and count exercise repetitions in real-time using pose estimation
- Navigate menus using hand gestures — no keyboard or mouse required
- Provide workout guidance, nutrition advice, and motivation through an AI chatbot

This project demonstrates how combining **computer vision** and **conversational AI** can create a low-cost, intelligent alternative to expensive personal training or fitness subscriptions.

---

## Features

- 🎯 **Real-Time Exercise Detection** — Recognizes 4 exercises using joint-angle calculations
- 🔢 **Repetition & Set Counting** — Tracks reps per set with debouncing logic for accuracy
- ⏱️ **Exercise Timer** — Tracks time taken per exercise to complete a set
- 🖐️ **Gesture-Based Navigation** — Control the UI by hovering your index finger over on-screen buttons
- 🤖 **AI Chatbot Assistant** — Powered by Google Gemini API for fitness Q&A and workout advice
- 📡 **Flask REST API** — Seamless communication between the web frontend and Python backend
- 🧩 **Modular Design** — Easily extendable with new exercises, gestures, or AI integrations

---

## Tech Stack

| Layer | Technology |
|---|---|
| Pose & Hand Tracking | [MediaPipe](https://mediapipe.dev) |
| Video Processing | [OpenCV](https://opencv.org) |
| Backend Logic | [Python](https://docs.python.org) |
| Web Framework | [Flask](https://flask.palletsprojects.com) |
| Frontend | HTML, CSS, JavaScript |
| AI Chatbot | Google Gemini API |

---

## Supported Exercises

### 🦵 Squats
Tracks the **knee joint angle** to detect full squat cycles.
- Standing: knee angle > 160°
- Squatting: knee angle < 90°

### 💪 Bicep Curls
Tracks the **elbow joint angle** for both left and right arms independently.
- Extended: elbow angle > 150°
- Flexed: elbow angle < 40°

### 🤸 Jumping Jacks
Tracks **shoulder angles** and **ankle distance** simultaneously.
- Arms up: shoulder angle > 150° | Legs apart: ankle distance > 150px
- Arms down: shoulder angle < 90° | Legs together: ankle distance < 80px

### 🙆 Standing Toe Touches
Monitors **leg extension** and **wrist-to-ankle vertical distance**.
- Legs straight: leg angle > 160°
- Hands near toes: Y-distance between wrist and ankle < 100px

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│               Web Frontend (HTML/CSS/JS)    │
│  - Exercise selection via gesture UI        │
│  - Chatbot interface                        │
└─────────────────┬───────────────────────────┘
                  │  Flask REST API
┌─────────────────▼───────────────────────────┐
│            Python Backend                  │
│  ┌─────────────┐   ┌──────────────────────┐ │
│  │ OpenCV      │   │ MediaPipe            │ │
│  │ (Webcam /   │──▶│ Pose + Hand Tracking │ │
│  │  Video I/O) │   └──────────┬───────────┘ │
│  └─────────────┘              │             │
│                    ┌──────────▼───────────┐ │
│                    │ Exercise Logic       │ │
│                    │ (Angle Calculation & │ │
│                    │  Rep Counting)       │ │
│                    └──────────────────────┘ │
└─────────────────────────────────────────────┘
                  │  Gemini API
┌─────────────────▼───────────────────────────┐
│           AI Chatbot (Google Gemini)        │
│  - Multi-turn conversations                 │
│  - Fitness Q&A, nutrition, motivation       │
└─────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.8+
- Webcam
- Google Gemini API Key

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gym-fitness-tracker.git
   cd gym-fitness-tracker
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Gemini API key**

   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

---

## Usage

1. **Launch the app** using the Start button on the web interface.
2. **Select an exercise** by hovering your index finger over the desired option on screen.
3. **Choose reps and sets** using the same gesture-based navigation.
4. **Begin your workout** — the system will count your reps, track your sets, and display elapsed time.
5. **Ask the chatbot** any fitness question in the chat panel (e.g., *"What muscles do squats target?"*, *"Suggest a post-workout meal"*).

> 💡 **Tip:** Ensure good lighting and a clear background for best pose detection accuracy. Stand fully in frame before starting.

---

## Results & Performance

| Component | Expected Accuracy |
|---|---|
| Squat Detection | 85–90% |
| Bicep Curl Detection | ~90% |
| Jumping Jack Detection | 88–92% |
| Standing Toe Touch Detection | 85–90% |
| Gesture Recognition (UI Nav) | ~90% |
| Chatbot Response Quality | 85–90% |

- Real-time feedback is overlaid on the webcam feed using OpenCV.
- System maintains **15–25 FPS** on consumer-grade hardware.
- Debouncing logic prevents false repetition counts during slow or partial movements.

---

## Limitations

- **Background Clutter:** Accuracy drops with cluttered or dynamic backgrounds.
- **Partial Occlusion:** Wearing loose clothing or being partially out of frame may affect landmark detection.
- **Chatbot Scope:** The chatbot is suited for general fitness guidance and is not a substitute for professional medical or nutrition advice.
- **Exercise Variety:** Currently limited to 4 exercises; complex movements like push-ups or lunges are not yet supported.

---

## Future Scope

- 🏃 **More Exercises** — Add yoga poses, lunges, push-ups, and advanced movements
- 👤 **User Personalization** — Learn individual patterns and adapt routines to user goals
- 📱 **Mobile App** — Extend to iOS/Android using the device's native camera
- 🔊 **Voice Feedback** — Real-time audio correction and encouragement using NLP
- ☁️ **Cloud Sync** — Save workout history and progress across devices

---

## References

- MediaPipe — [https://mediapipe.dev](https://mediapipe.dev)
- Flask — [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
- Python — [https://docs.python.org](https://docs.python.org)
- OpenCV — [https://opencv.org](https://opencv.org)

---

## License

This project was developed as an academic project. Please contact the authors for usage permissions.

---

<p align="center">Made with 💪 by Zain Ul Abideen & Usman Nazar</p>
