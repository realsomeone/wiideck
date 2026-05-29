import os
import pwd
import subprocess
import sys


if sys.platform != 'darwin':
    import keyboard as kb

    USER = os.environ.get("SUDO_USER", os.environ.get("USER"))
    UID = pwd.getpwnam(USER).pw_uid
else:
    from pynput.keyboard import Key, Controller

    kb = Controller()

DIR = os.getcwd() + os.sep

def sfx(file):
    if sys.platform != 'darwin':
        subprocess.Popen(
            ["su", USER, "-c", f"XDG_RUNTIME_DIR=/run/user/{UID} pw-play --target sfx --volume 0.2 '{DIR+file}'",],
        )
    else:
        # MacOS
        subprocess.Popen(["afplay", f"{DIR+file}"])


def bind(keys):
    for key in keys:
        kb.press(key)
    for key in keys[::-1]:
        kb.release(key)
