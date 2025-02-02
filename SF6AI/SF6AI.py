import cv2
import numpy as np
import mss
import time
import pydirectinput
from ultralytics import YOLO

# Load trained YOLO model for character detection (Replace with your trained model)
model = YOLO("sf6_characters.pt")

# Capture Game Screen
def capture_screen(region=None):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(region if region else sct.monitors[1]))
        return screenshot

# Detect Health Bar (Grayscale & Thresholding)
def get_health_bar(player="P1"):
    region = {"top": 50, "left": 200, "width": 300, "height": 20} if player == "P1" else {"top": 50, "left": 1400, "width": 300, "height": 20}
    screenshot = capture_screen(region)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    health_pixels = np.sum(thresh == 255)
    max_pixels = region['width'] * region['height']
    health_ratio = health_pixels / max_pixels
    return round(health_ratio * 100, 2)  # Return health percentage

# Detect Characters Using YOLO
def detect_characters():
    screenshot = capture_screen()
    results = model(screenshot)
    positions = []
    for r in results:
        for obj in r.boxes.data:
            x1, y1, x2, y2, conf, cls = obj
            positions.append((int(x1), int(y1), int(x2), int(y2), int(cls)))
    return positions  # Returns list of character positions

# AI Inputs - Simulate Key Presses
def press_light_punch():
    pydirectinput.keyDown('j')
    pydirectinput.keyUp('j')

def hadouken():
    pydirectinput.keyDown('down')
    time.sleep(0.1)
    pydirectinput.keyDown('right')
    pydirectinput.keyUp('down')
    time.sleep(0.1)
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('j')  # Punch
    pydirectinput.keyUp('j')

# Main AI Loop
def main():
    while True:
        # Get Game Data
        p1_health = get_health_bar("P1")
        p2_health = get_health_bar("P2")
        characters = detect_characters()

        # Print Data
        print(f"P1 Health: {p1_health}% | P2 Health: {p2_health}%")
        print("Detected Characters:", characters)

        # Basic AI Logic (Press Light Punch if Opponent is Close)
        if characters:
            p1_x, _, p1_x2, _, _ = characters[0]
            p2_x, _, p2_x2, _, _ = characters[1]

            distance = abs(p1_x - p2_x)
            print("Distance Between Characters:", distance)

            if distance < 200:  # If characters are close, attack
                print("AI Decision: Light Punch")
                press_light_punch()
            else:
                print("AI Decision: Move Closer")

        time.sleep(0.1)  # Short delay to prevent spamming

if __name__ == "__main__":
    main()
