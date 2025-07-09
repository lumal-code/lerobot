import cv2
import json

with open("square_to_box.json") as f:
    SQUARE_TO_BOX = json.load(f)

def async_overlay(cam, squares: str):
    frame = cam.async_read()
    if frame is None:
        raise ValueError("Camera returned empty frame")
    
    frame = frame.copy()

    squares = squares.split()
    for square in squares:
        if square in SQUARE_TO_BOX:
            top_left, bottom_right = SQUARE_TO_BOX[square]
            cv2.rectangle(frame, tuple(top_left), tuple(bottom_right), (0, 0, 255), 2)
            cv2.rectangle(frame, tuple(top_left), tuple(bottom_right), (0, 255, 0), 2)
        else:
            print(f"[!] Square '{square}' not found in square_to_box.json")
    
    return frame