import cv2
from utils import calculate_angle
from config import FONT, WIDTH, HEIGHT

# State variables
squat_stage = None
squat_count = 0

def process_squats(frame, landmarks, selected_reps, selected_sets, current_rep):
    global squat_stage, squat_count

    def get_point(index):
        lm = landmarks[index]
        return [lm.x * WIDTH, lm.y * HEIGHT]

    # Joint points
    r_hip, r_knee, r_ankle = map(get_point, [24, 26, 28])
    l_hip, l_knee, l_ankle = map(get_point, [23, 25, 27])

    # Knee angles
    angle_r_knee = int(calculate_angle(r_hip, r_knee, r_ankle))
    angle_l_knee = int(calculate_angle(l_hip, l_knee, l_ankle))
    avg_knee_angle = (angle_r_knee + angle_l_knee) // 2

    # Update squat stage
    if avg_knee_angle < 90:
        squat_stage = 'down'
    elif squat_stage == 'down' and avg_knee_angle > 160:
        squat_stage = 'up'
        squat_count += 1

    # Display angles on screen
    cv2.putText(frame, f'{angle_r_knee}°', tuple(map(int, r_knee)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'{angle_l_knee}°', tuple(map(int, l_knee)), FONT, 0.8, (0, 255, 0), 2)

    # Progress bars
    draw_progress_bar(frame, 20, 40, squat_count, selected_reps, "Reps", (0, 255, 0))
    draw_progress_bar(frame, 20, 80, current_rep, selected_sets, "Sets", (255, 100, 0))

    # Check completion
    if squat_count >= selected_reps:
        current_rep += 1
        squat_count = 0
        if current_rep >= selected_sets:
            show_centered_message(frame, "All Sets Completed!", (0, 255, 0))
            return current_rep, True
        else:
            show_centered_message(frame, f"Set {current_rep + 1} Complete!", (0, 255, 0))

    return current_rep, False

def draw_progress_bar(frame, x, y, current, total, label, color):
    pct = current / total
    cv2.rectangle(frame, (x, y), (x + 200, y + 20), (100, 100, 100), 2)
    cv2.rectangle(frame, (x, y), (x + int(200 * pct), y + 20), color, -1)
    cv2.putText(frame, f'{label}: {current}/{total}', (x, y - 5), FONT, 0.6, color, 2)

def show_centered_message(frame, text, color):
    text_size = cv2.getTextSize(text, FONT, 1.5, 4)[0]
    position = (WIDTH // 2 - text_size[0] // 2, HEIGHT // 2)
    cv2.putText(frame, text, position, FONT, 1.5, color, 4)

def reset_squats():
    global squat_stage, squat_count
    squat_stage = None
    squat_count = 0
