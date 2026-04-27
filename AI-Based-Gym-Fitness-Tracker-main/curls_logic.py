import cv2
from utils import calculate_angle
from config import FONT, WIDTH, HEIGHT

# State variables
curl_stage = None
arm_stage = 'left'  # Start with left arm
rep_count = 0

def process_curls(frame, landmarks, selected_reps, selected_sets, current_rep):
    global curl_stage, arm_stage, rep_count

    def get_point(index):
        lm = landmarks[index]
        return [lm.x * WIDTH, lm.y * HEIGHT]

    # Joint points
    r_shoulder, r_elbow, r_wrist = map(get_point, [12, 14, 16])
    l_shoulder, l_elbow, l_wrist = map(get_point, [11, 13, 15])

    # Angles
    angle_r = int(calculate_angle(r_shoulder, r_elbow, r_wrist))
    angle_l = int(calculate_angle(l_shoulder, l_elbow, l_wrist))

    # Display angles
    cv2.putText(frame, f'{angle_r}°', tuple(map(int, r_elbow)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'{angle_l}°', tuple(map(int, l_elbow)), FONT, 0.8, (0, 255, 0), 2)

    # Alternating arm logic
    if arm_stage == 'left':
        cv2.putText(frame, "Do Right Arm", (WIDTH // 2 - 100, 100), FONT, 1, (255, 255, 0), 3)
        if angle_l < 50:
            curl_stage = 'up'
        elif curl_stage == 'up' and angle_l > 150:
            curl_stage = None
            arm_stage = 'right'

    elif arm_stage == 'right':
        cv2.putText(frame, "Do Left Arm", (WIDTH // 2 - 100, 100), FONT, 1, (0, 255, 255), 3)
        if angle_r < 50:
            curl_stage = 'up'
        elif curl_stage == 'up' and angle_r > 150:
            curl_stage = None
            arm_stage = 'left'
            rep_count += 1

    # Progress bars
    draw_progress_bar(frame, 20, 40, rep_count, selected_reps, "Reps", (0, 255, 0))
    draw_progress_bar(frame, 20, 80, current_rep, selected_sets, "Sets", (255, 100, 0))

    # Check completion
    if rep_count >= selected_reps:
        current_rep += 1
        rep_count = 0
        if current_rep >= selected_sets:
            show_centered_message(frame, "All Sets Completed!", (0, 255, 0))
            return current_rep, True
        else:
            show_centered_message(frame, f"Set {current_rep} Complete!", (0, 255, 0))

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

def reset_curls():
    global curl_stage, arm_stage, rep_count
    curl_stage = None
    arm_stage = 'left'
    rep_count = 0
