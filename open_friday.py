import keyboard as k
import os, time

while True:
    if k.is_pressed("`") == True:
        os.startfile("friday.py")
        time.sleep(2)