import cv2
cap = cv2.VideoCapture(0)
print(f"Camera 0 opened: {cap.isOpened()}")
if cap.isOpened():
    ret, frame = cap.read()
    print(f"Frame captured: {ret}")
cap.release()