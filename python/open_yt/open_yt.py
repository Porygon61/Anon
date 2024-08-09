import json
import os
import sys
import webbrowser as wb
import pyautogui as auto
import time
import keyboard

#------------------------------------------------------------#
# Add script to use 'install_modules' module
#script_dir = 'g:\\Privat\\All Code\\Programs'       #CHANGE DRIVE AND .BAT FILE BEFORE USE    
#if script_dir not in sys.path:
#    sys.path.append(script_dir)
#    print(f"Added {script_dir} to path")
#else:
#    print(f"{script_dir} is already in path\n")
#    print(sys.path)

import install_modules
install_modules.install_modules_of(os.path.abspath(__file__))
#------------------------------------------------------------#

# Global Variables (std)
search_bar_x, search_bar_y = -1230, 340
mouse_target_x, mouse_target_y = -1215, 775
topic = "saftiger hugo"
browser = "opera-gx"
screen_width, screen_height = 0, 0

CONFIG_FILE = r"G:\Privat\All Code\Programs\open_yt\config.json" #CHANGE DRIVE BEFORE USE

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config({
            "topics": ["saftiger hugo", "None of the above"],
            "browsers": [
                "mozilla", "firefox", "epiphany", "kfmclient", "konqueror", "kfm", "opera", "opera-gx",
                "links", "elinks", "lynx", "w3m", "windows-default", "chrome", "chromium", "chromium-browser",
                "none of the above"
            ]
        })
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)

def register_browser(name="", path="", opera_gx=True):
    if opera_gx:
        wb.register(
            "opera-gx",
            None,
            wb.BackgroundBrowser(
                "C:\\Users\\filip\\AppData\\Local\\Programs\\Opera GX\\opera.exe" #CHANGE USERNAME BEFORE USE
            ),
        )
    else:
        wb.register(name, None, wb.BackgroundBrowser(path))

def choosing():
    global topic, browser

    config = load_config()
    topics = config["topics"]
    browsers = config["browsers"]

    while True:
        print("Topics:")
        for num, t_object in enumerate(topics, start=1):
            print(f"{num}: {t_object}")
        try:
            inp = int(input("Choose Topic: "))
            if 1 <= inp < len(topics):
                topic = topics[inp - 1]
                break
            elif inp == len(topics):
                print("No Topic chosen. ", end="")
                t_registration = input("Register a new Topic? [y/n]...")
                if t_registration.lower() == 'y':
                    new_topic = input("Topic: ")
                    topics.insert(len(topics) - 1, new_topic)
                    config["topics"] = topics
                    save_config(config)
                else:
                    exit()
        except ValueError:
            print("Invalid input. Please enter a number.")

    input("Press ENTER to continue...")

    while True:
        print("Browsers:")
        for num, b_object in enumerate(browsers, start=1):
            print(f"{num}: {b_object}")
        try:
            inp = int(input("Choose Browser: "))
            if 1 <= inp < len(browsers):
                browser = browsers[inp - 1]
                if browser == "opera-gx":
                    register_browser(opera_gx=True)
                break
            elif inp == len(browsers):
                print("No browser chosen. ", end="")
                b_registration = input("Register Something? [y/n]...")
                if b_registration.lower() == 'y':
                    name = input("Name: ")
                    path = input("Path to the Browser: ")
                    register_browser(name, path)
                    browsers.insert(len(browsers) - 1, name)
                    config["browsers"] = browsers
                    save_config(config)
                else:
                    exit()
        except ValueError:
            print("Invalid input. Please enter a number.")

def mouse_configure():
    global mouse_target_x, mouse_target_y
    print("Mouse:")
    inp = input("Press Enter to check current mouse location or 'm' to manually set it... ")
    if inp == "":
        for i in range(3):
            print(i)
            time.sleep(0.7)
        mouse_target_x, mouse_target_y = auto.position()
        print(f"Mouse Position: x: {mouse_target_x}, y: {mouse_target_y}")
    elif inp.lower() == 'm':
        mouse_target_x = int(input("x: "))
        mouse_target_y = int(input("y: "))

def setup():
    global screen_height, screen_width, search_bar_x, search_bar_y, mouse_target_x, mouse_target_y
    screen_height = auto.size().height
    screen_width = auto.size().width
    print(f"Resolution: {screen_width}x{screen_height}")

    if input("Configure Mouse Click? [y/n]...").lower() == 'y':
        mouse_configure()

    choosing()

def main():
    print("Personal Mode will get activated in 5 seconds. Press SPACE to continue manually...")
    start_time = time.time()

    while True:
        if keyboard.is_pressed("space"):  # Manual Mode
            time.sleep(0.5)
            break
        if time.time() - start_time >= 5:  # Personal Mode
            setup_personal_mode()
            execution()
            break

    setup()  # Manual Mode Continued
    execution()

def setup_personal_mode():
    global search_bar_x, search_bar_y, mouse_target_x, mouse_target_y, topic, browser
    search_bar_x, search_bar_y = -1230, 340
    mouse_target_x, mouse_target_y = -1215, 775
    topic = "saftiger hugo"
    register_browser(opera_gx=True)
    browser = "opera-gx"

def execution():
    link = f'https://www.youtube.com/results?search_query={(topic.replace(" ", "+"))}'
    wb.get(browser).open(link, new=2, autoraise=True)
    #time.sleep(5)
    #auto.click(search_bar_x, search_bar_y, clicks=1, button="left")
    #auto.typewrite(topic)
    #auto.press("enter")
    time.sleep(3.5)
    auto.click(mouse_target_x, mouse_target_y, clicks=1, button="left")
    print("\nDone!\n")
    exit()

if __name__ == "__main__":
    main()
