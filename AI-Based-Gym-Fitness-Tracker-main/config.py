import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX
PROGRESS_DURATION = 3
WIDTH, HEIGHT = 1280, 720

exercise_rects = {
    "Curls": (100, 100, 200, 100),
    "Squats": (400, 100, 200, 100),
    "Jumping Jacks": (700, 100, 250, 100),
    "Toe Touch": (1000, 100, 250, 100),
}


reps_rects = {str(i): ((i - 1) * 110 + 60, HEIGHT//2 - 50, 100, 100) for i in range(1, 11)}
sets_rects = {str(i): ((i - 1) * 110 + 60, HEIGHT//2 - 50, 100, 100) for i in range(1, 11)}