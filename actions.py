import os
import pwd
import subprocess

import keyboard

USER = os.environ.get("SUDO_USER", os.environ.get("USER"))
UID = pwd.getpwnam(USER).pw_uid

DIR = "/home/arnal/Documents/wiideck/"


def sfx(file):
    print("sounding")
    subprocess.Popen(
        [
            "su",
            USER,
            "-c",
            f"XDG_RUNTIME_DIR=/run/user/{UID} pw-play --target sfx --volume 0.2 '{DIR+file}'",
        ],
    )


def bind(keys):
    print("binding")
    keyboard.send(keys)

