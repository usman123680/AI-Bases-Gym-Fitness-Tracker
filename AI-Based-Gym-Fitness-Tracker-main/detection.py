import mediapipe as mp

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1)
pose = mp_pose.Pose()
