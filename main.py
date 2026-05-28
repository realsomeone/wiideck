from wiideck import *
import sys
from pynput.keyboard import Key

threshold = 2.3 #g

# motion-based macros

        # Up    Right   Down    Left
cmds = [[None, None, None, None],                       # no presses
        [[S,"sfx/CrowdYay.wav"], [S,"sfx/CrowdOh.wav"], [S,"sfx/CrowdAw.wav"], [S,"sfx/coqui.mp3"]], # A press
        [[S, "sfx/heavenly-music.wav"], [S,"sfx/air-horn.mp3"], [S,"sfx/vine-boom.wav"], None],    # B press
        [None, None, [S, "sfx/mmm-6.mp3"], None],]         # A + B

# button-based macros

macros = {"Home" : [K,[Key.ctrl, Key.up]],
          "Minus": [K,[Key.ctrl, Key.left]],
          "Plus" : [K,[Key.ctrl, Key.right]],
          "Left" : [K,[Key.left]],
          "Right": [K,[Key.right]],
          }

if sys.platform != 'darwin':
    wiideck(cmds, g(threshold), macros)
else:
    wiimac(cmds, g(threshold), macros)