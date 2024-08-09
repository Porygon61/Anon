import pyautogui
import time

print(pyautogui.size()) # print the size of the screen

pyautogui.moveTo(100, 100, duration = 1) # moveTo(x, y, duration = 0.0) moving the Mouse to the new Position

pyautogui.moveRel(0, 50, duration = 1) # moveRel(x, y, duration = 0.0) moving the Mouse relative to the old Position

print(pyautogui.position()) # print the current position of the Mouse

pyautogui.click(100, 100,clicks= 1, interval = 0.5, button='left') # click(x, y, clicks = 1, interval = 0.0, button = 'left')

pyautogui.scroll(100) # scroll(clicks = 1, x = None, y = None, xoffset = 0, yoffset = 0, duration = 0.5)

pyautogui.typewrite('Hello World') # typewrite(text, interval = 0.0)

pyautogui.typewrite('a', 'left', 'ctrlleft') # typewrite(text/button, interval = 0.0)

pyautogui.hotkey('ctrlleft', 'a') # hotkey(modifiers, key)


time.sleep(10) 
 
# makes program execution pause for 10 sec
pyautogui.moveTo(1000, 1000, duration = 1) 
 
# moves mouse to 1000, 1000.
pyautogui.dragRel(100, 0, duration = 1)
 
# drags mouse 100, 0 relative to its previous position, 
# thus dragging it to 1100, 1000
pyautogui.dragRel(0, 100, duration = 1)
pyautogui.dragRel(-100, 0, duration = 1)
pyautogui.dragRel(0, -100, duration = 1)
