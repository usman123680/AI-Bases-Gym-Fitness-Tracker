import cv2
from utils import calculate_angle
from config import FONT, WIDTH, HEIGHT

# State
jack_stage = None
rep_count = 0

def process_jumping_jacks(frame, landmarks, selected_reps, selected_sets, current_rep):
    global jack_stage, rep_count

    def get_point(index):
        lm = landmarks[index]
        return [lm.x * WIDTH, lm.y * HEIGHT]

    # Landmarks
    l_wrist = get_point(15)
    r_wrist = get_point(16)
    l_shoulder = get_point(11)
    r_shoulder = get_point(12)
    l_hip = get_point(23)
    r_hip = get_point(24)
    l_ankle = get_point(27)
    r_ankle = get_point(28)

    # Arm angles (shoulder as vertex)
    angle_l = int(calculate_angle(l_wrist, l_shoulder, l_hip))
    angle_r = int(calculate_angle(r_wrist, r_shoulder, r_hip))

    # Ankle distance (X-axis)
    ankle_dist = abs(l_ankle[0] - r_ankle[0])

    # Display arm angles and ankle distance
    cv2.putText(frame, f'{angle_l}°', tuple(map(int, l_shoulder)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'{angle_r}°', tuple(map(int, r_shoulder)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'Dist: {ankle_dist:.2f}', (50, 150), FONT, 0.8, (255, 255, 0), 2)

    # Stage logic
    arms_up = angle_l > 150 and angle_r > 150
    legs_apart = ankle_dist > 150  # tuned for pixel values

    arms_down = angle_l < 90 and angle_r < 90
    legs_together = ankle_dist < 80  # tuned for pixel values

# Define the stage transition for a strict jumping jack rep
    if jack_stage is None:
        if arms_up and legs_apart:
            jack_stage = 'up'
    elif jack_stage == 'up':
        if arms_down and legs_together:
            jack_stage = None
            rep_count += 1


    # Show rep/set progress
    draw_progress_bar(frame, 20, 40, rep_count, selected_reps, "Reps", (0, 255, 0))
    draw_progress_bar(frame, 20, 80, current_rep, selected_sets, "Sets", (255, 100, 0))

    # Completion logic
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

def reset_jumping_jacks():
    global jack_stage, rep_count
    jack_stage = None
    rep_count = 0
