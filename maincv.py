import cv2
import numpy as np
import pyautogui as pt
from datetime import datetime
import imutils
import os
from time import sleep


def rotate_camera(direction,value, duration):
    if direction == 'left':
        pt.moveRel(-value, 0, duration=duration)  # Bewege die Maus nach links
    elif direction == 'right':
        pt.moveRel(value, 0, duration=duration)  # Bewege die Maus nach rechts
    elif direction == 'up':
        pt.moveRel(0, -value, duration=duration)
    elif direction == 'down':
        pt.moveRel(0, value, duration=duration)
    else:
        print("Invalid direction")

def check_for_bedrock_with_opencv(screenshot_path, bedrock_template_path):
    image = cv2.imread(screenshot_path)
    template = cv2.imread(bedrock_template_path)
    h, w = template.shape[:-1]
    
    # Hier können Sie die Skalen und Winkel anpassen, um die Erkennung zu optimieren
    for scale in np.linspace(0.5, 1.5, 20):
        resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
        for angle in range(0, 360, 10):
            rotated_template = imutils.rotate_bound(resized_template, angle)
            res = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            if loc[0].size > 0:
                return True, res.max()
    return False, 0

screenshot_dir = "./screenshot_folder"
os.makedirs(screenshot_dir, exist_ok=True)

duration = 5  # Beispiel für die Dauer
while duration != 0:
    pt.keyDown("x")
    for i in range(7):
        mouse_x, mouse_y = pt.position()
        thresholda = 80
        region = (mouse_x - thresholda, mouse_y - thresholda, thresholda * 2, thresholda * 2)
        screenshot = pt.screenshot(region=region)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        bedrock_template_path = "images/bedrock.png"
        found, confidence = check_for_bedrock_with_opencv(screenshot_path, bedrock_template_path)
        if found:
            print(f"Bedrock gefunden mit einer Konfidenz von {confidence}")
            rotate_camera("right", 80, .01)
        else:
            print(f"Kein Bedrock gefunden, Konfidenz ist {confidence}")
        
        sleep(0.1)
    duration -= 1
    print(f"time left: {duration}")
