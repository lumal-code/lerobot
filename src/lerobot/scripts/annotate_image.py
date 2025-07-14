import cv2
import json

# Constants
OUTPUT_JSON = "square_to_box.json"
FILES = "abcdefgh"
RANKS = "87654321"

# Globals
square_to_box = {}
clicks = []
current_square_index = 0
square_names = [f + r for r in RANKS for f in FILES]  # a8 to h1

def click_callback(event, x, y, flags, param):
    global clicks, current_square_index, square_to_box

    if event == cv2.EVENT_LBUTTONDOWN and current_square_index < len(square_names):
        clicks.append((x, y))
        if len(clicks) == 2:
            top_left = clicks[0]
            bottom_right = clicks[1]
            square_name = square_names[current_square_index]
            square_to_box[square_name] = [top_left, bottom_right]
            print(f"✔ Marked {square_name}: {top_left} → {bottom_right}")
            current_square_index += 1
            clicks.clear()

def annotate_image(image_path):
    global current_square_index
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Failed to load image: {image_path}")
        return

    clone = img.copy()
    cv2.namedWindow("Annotate Squares")
    cv2.setMouseCallback("Annotate Squares", click_callback)

    while True:
        display = clone.copy()
        if current_square_index < len(square_names):
            prompt = f"Mark square: {square_names[current_square_index]} (top-left, then bottom-right)"
            cv2.putText(display, prompt, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(display, "All squares annotated. Press 's' to save, or 'q' to quit.", 
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Draw all current boxes
        for sq, box in square_to_box.items():
            cv2.rectangle(display, box[0], box[1], (0, 0, 255), 1)
            label_pos = (box[0][0] + 3, box[0][1] - 5)
            cv2.putText(display, sq, label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

        cv2.imshow("Annotate Squares", display)
        key = cv2.waitKey(10) & 0xFF

        if key == ord('q'):
            print("✖ Quit without saving.")
            break
        elif key == ord('s') and current_square_index == len(square_names):
            with open(OUTPUT_JSON, "w") as f:
                json.dump(square_to_box, f, indent=2)
            print(f"✅ Saved {OUTPUT_JSON}")
            break

    cv2.destroyAllWindows()

# To run: annotate_image("your_board_image.png") at the bottom of your script

if __name__ == "__main__":
    annotate_image("/Users/luke/dev/lerobot/chess_board.png")