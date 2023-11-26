import pyautogui as pt
import pydirectinput as pdi
from time import sleep
import os
from datetime import datetime
import pyautogui as pt
from pyscreeze import ImageNotFoundException
import cv2
import numpy as np

#Helper Functions

def nav_to_image(image, clicks, off_x=0, off_y=0):
    position = pt.locateOnScreen(image, confidence=.9)
    if position is None:
        print(f"Can't find {image}")
        return 0
    else:
        pt.moveTo(position, duration=.1)
        pt.moveRel(off_x, off_y, duration=.1)
        pt.click(clicks=clicks , interval=.3)

# Moves the character
# x = attack

def move_character(key_press, duration,action="walking"):
    pt.keyDown(key_press)
    if(action == "walking"):
        print("Walking")
    elif(action == "attack"):
        pt.keyDown("X")
        print("Attacking")

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

def loopold():
    pt.keyDown("X")
    for i in range(7):
        rotate_camera("right", 80, .01)
        print(i)
        sleep(2.5)
    pt.keyUp("X")
    pt.keyDown("X")
    sleep(2.0)
    rotate_camera("down", 150, .01)
    for k in range(7):
        rotate_camera("left", 80, .01)
        print(k)
        sleep(2.5)
    pt.keyUp("X")
    sleep(2.0)

    rotate_camera("up", 150, .01)

def is_image_on_screen(image, confidence=0.8):
    return pt.locateOnScreen(image, confidence=confidence) is not None

def check_for_bedrock_near_mouse(image, threshold=100):
    try:
        mouse_x, mouse_y = pt.position()
        region = (mouse_x-threshold, mouse_y-threshold, threshold*2, threshold*2)
        matches = list(pt.locateAllOnScreen(image, region=region, confidence=0.4))
        if matches:
            highest_confidence_match = max(matches, key=lambda e: e[1])
            return True, highest_confidence_match[1]  # Rückgabe des booleschen Wertes und der höchsten Konfidenz
        else:
            return False, 0  # Kein Match gefunden
    except ImageNotFoundException:
        return False, 0  # Kein Match gefunden und Ausnahme abgefangen

# Beispielaufruf der Funktion

# Haupt-Loop
sleep(3)
nav_to_image("images/McBacktoGame1.png", 3)

duration = 100

screenshot_dir = "./screenshot_folder"
os.makedirs(screenshot_dir, exist_ok=True)


while duration != 0:
    loopold()

    duration -= 1
    print(f"time left: {duration}")