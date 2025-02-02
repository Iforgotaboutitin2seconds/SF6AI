import mss
import numpy as np
import cv2
import time
import os

# Create a folder to store screenshots
SAVE_FOLDER = "sf6_screenshots"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Capture at 30 FPS
CAPTURE_INTERVAL = 1 / 30  

def capture_frame(frame_number):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[1]))  # Full screen
        filename = os.path.join(SAVE_FOLDER, f"frame_{frame_number:04d}.png")
        cv2.imwrite(filename, screenshot)
        print(f"Saved {filename}")

# Record match automatically
def record_match():
    frame_count = 0
    try:
        while True:
            capture_frame(frame_count)
            frame_count += 1
            time.sleep(CAPTURE_INTERVAL)  # Maintain FPS
    except KeyboardInterrupt:
        print("\nRecording stopped.")
        print(f"Total frames captured: {frame_count}")

if __name__ == "__main__":
    print("Starting SF6 screenshot capture... Press CTRL+C to stop.")
    record_match()
