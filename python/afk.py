import pyautogui as auto
import time
import keyboard

key = "esc"


def check_key(key):
    if keyboard.is_pressed(key) == True:
        print(f"{key} key pressed")
        return True
    else:
        return False


while True:
    auto.move(400, 0)
    if check_key(key) == True:
        break
    auto.move(-400, 0)
    if check_key(key) == True:
        break
