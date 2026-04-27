import cv2
from utils import calculate_angle
from config import FONT, WIDTH, HEIGHT

# State
toe_touch_stage = None
rep_count = 0

def process_standing_toe_touch(frame, landmarks, selected_reps, selected_sets, current_rep):
    global toe_touch_stage, rep_count

    def get_point(index):
        lm = landmarks[index]
        return [lm.x * WIDTH, lm.y * HEIGHT]

    # Landmarks
    l_hip = get_point(23)
    r_hip = get_point(24)
    l_knee = get_point(25)
    r_knee = get_point(26)
    l_ankle = get_point(27)
    r_ankle = get_point(28)
    l_wrist = get_point(15)
    r_wrist = get_point(16)

    # Angles for checking if the legs are straight
    angle_l_leg = int(calculate_angle(l_hip, l_knee, l_ankle))
    angle_r_leg = int(calculate_angle(r_hip, r_knee, r_ankle))

    # Distance between the wrist and the ankle (for checking if hands are close to toes)
    l_hand_to_toe_dist = abs(l_wrist[1] - l_ankle[1])  # Y-axis distance
    r_hand_to_toe_dist = abs(r_wrist[1] - r_ankle[1])  # Y-axis distance

    # Display angles and distances
    cv2.putText(frame, f'Left Leg: {angle_l_leg}°', tuple(map(int, l_knee)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'Right Leg: {angle_r_leg}°', tuple(map(int, r_knee)), FONT, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f'Left Hand to Toe: {l_hand_to_toe_dist:.2f}', (50, 150), FONT, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f'Right Hand to Toe: {r_hand_to_toe_dist:.2f}', (50, 180), FONT, 0.8, (255, 255, 0), 2)

    # Check if legs are straight (threshold angle < 20 degrees)
    legs_straight = angle_l_leg > 160 and angle_r_leg > 160  # Legs are nearly straight

    # Check if hands are close to toes
    hands_touching_toes = l_hand_to_toe_dist < 100 and r_hand_to_toe_dist < 100  # Adjust the distance threshold

    # Stage logic
    if toe_touch_stage is None:
        if legs_straight and hands_touching_toes:
            toe_touch_stage = 'touched'
    elif toe_touch_stage == 'touched':
        if not hands_touching_toes:
            toe_touch_stage = None
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

def reset_standing_toe_touch():
    global toe_touch_stage, rep_count
    toe_touch_stage = None
    rep_count = 0
