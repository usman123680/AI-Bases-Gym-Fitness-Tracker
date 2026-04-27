import cv2
import time
from config import WIDTH, HEIGHT, exercise_rects, reps_rects, sets_rects
from detection import hands, pose, drawing, mp_pose, mp_hands
from ui import draw_menu_items
from pose_logic import process_squats, reset_squats
from curls_logic import process_curls, reset_curls
from jumping_jacks import process_jumping_jacks, reset_jumping_jacks
from standing_toe_touch import process_standing_toe_touch, reset_standing_toe_touch

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# App state
mode = "exercise"
selected_exercise = selected_reps = selected_sets = None
current_set = current_rep = 0
freeze_start = start_time = final_time = None

# Hover state
hover_state = {name: {"start": None} for name in exercise_rects}
rep_hover = {str(i): {"start": None} for i in range(1, 11)}
set_hover = {str(i): {"start": None} for i in range(1, 11)}

# UI navigation functions
def go_to_reps(name):
    global mode, selected_exercise
    selected_exercise = name
    mode = "reps"

def go_to_sets(rep_count):
    global mode, selected_reps
    selected_reps = int(rep_count)
    mode = "sets"

def go_to_done(set_count):
    global mode, selected_sets, current_rep, start_time, final_time
    selected_sets = int(set_count)
    current_rep = 0
    if selected_exercise == "Curls":
        reset_curls()
    elif selected_exercise == "Squats":
        reset_squats()
    elif selected_exercise == "Jumping Jacks":
        reset_jumping_jacks()
    elif selected_exercise == "Standing Toe Touch":
        reset_standing_toe_touch()

    start_time = time.time()
    final_time = None
    mode = "done"


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_hands = hands.process(rgb)
    result_pose = pose.process(rgb)

    # Detect cursor
    cursor = None
    if result_hands.multi_hand_landmarks:
        h, w, _ = frame.shape
        index_finger = result_hands.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        cursor = (int(index_finger.x * w), int(index_finger.y * h))
        cv2.circle(frame, cursor, 10, (0, 255, 255), -1)

    # UI logic
    if mode == "exercise":
        draw_menu_items(frame, exercise_rects, cursor, hover_state, go_to_reps)
    elif mode == "reps":
        draw_menu_items(frame, reps_rects, cursor, rep_hover, go_to_sets)
    elif mode == "sets":
        draw_menu_items(frame, sets_rects, cursor, set_hover, go_to_done)
    elif mode == "done" and selected_exercise:
        elapsed = time.time() - start_time
        timer_text = f"Time: {int(elapsed)}.{int((elapsed % 1) * 1000):03d}s"
        text_size = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        cv2.putText(frame, timer_text, (WIDTH - text_size[0] - 10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if result_pose.pose_landmarks:
            drawing.draw_landmarks(frame, result_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = result_pose.pose_landmarks.landmark

            if selected_exercise == "Squats":
                current_rep, done = process_squats(frame, landmarks, selected_reps, selected_sets, current_rep)
            elif selected_exercise == "Curls":
                current_rep, done = process_curls(frame, landmarks, selected_reps, selected_sets, current_rep)
            elif selected_exercise == "Jumping Jacks":
                current_rep, done = process_jumping_jacks(frame, landmarks, selected_reps, selected_sets, current_rep)
            elif selected_exercise == "Standing Toe Touch":
                current_rep, done = process_standing_toe_touch(frame, landmarks, selected_reps, selected_sets, current_rep)


            if done:
                final_time = time.time() - start_time
                freeze_start = time.time()
                mode = "freeze"
    elif mode == "freeze":
        frame[:] = (0, 0, 0)
        cv2.putText(frame, "All Sets Completed!", (WIDTH // 2 - 200, HEIGHT // 2 - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)

        if final_time is not None:
            time_str = f"Total Time: {int(final_time)}.{int((final_time % 1) * 1000):03d}s"
            cv2.putText(frame, time_str, (WIDTH // 2 - 150, HEIGHT // 2 + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

        if time.time() - freeze_start >= 5:
            mode = "exercise"

    cv2.imshow("Fitness App", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()