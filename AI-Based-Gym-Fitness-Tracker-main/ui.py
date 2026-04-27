import cv2
import time
from config import FONT, PROGRESS_DURATION
from utils import is_hover

def draw_menu_items(frame, items, cursor, hover_state, on_select):
    for name, rect in items.items():
        rx, ry, rw, rh = rect
        hovering = cursor and is_hover(*cursor, rect)

        if hovering:
            color = (0, 255, 0)
            font_scale = 1.5
            if hover_state[name]["start"] is None:
                hover_state[name]["start"] = time.time()
        else:
            color = (255, 255, 255)
            font_scale = 1
            hover_state[name]["start"] = None

        cv2.rectangle(frame, (rx, ry), (rx+rw, ry+rh), color, 2)
        text_size = cv2.getTextSize(name, FONT, font_scale, 2)[0]
        text_x = rx + (rw - text_size[0]) // 2
        text_y = ry + (rh + text_size[1]) // 2
        cv2.putText(frame, name, (text_x, text_y), FONT, font_scale, color, 2)

        if hover_state[name]["start"]:
            elapsed = time.time() - hover_state[name]["start"]
            progress = min(int((elapsed / PROGRESS_DURATION) * 100), 100)
            bar_x = rx
            bar_y = ry + rh + 10
            bar_width = int(rw * (progress / 100))
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + rw, bar_y + 10), (100, 100, 100), 2)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + 10), (0, 255, 0), -1)

            if progress >= 100:
                on_select(name)
                break
