import subprocess
import keyboard
import os
import pwd

USER = os.environ.get("SUDO_USER", os.environ.get("USER"))
UID = pwd.getpwnam(USER).pw_uid

DIR = "/home/arnal/Documents/wiimote.py/"

def sfx(file):
    print("sounding")
    subprocess.Popen(
        ["su", USER, "-c", 
         f"XDG_RUNTIME_DIR=/run/user/{UID} paplay --device=sfx '{DIR+file}'"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def bind(keys):
    print("binding")
    keyboard.send(keys)