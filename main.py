from wiideck import *

threshold = 2.3 #g

# motion-based macros

        # Up    Right   Down    Left
cmds = [[None, None, None, None],                       # no presses
        [[S,"sfx/CrowdYay.wav"], [S,"sfx/CrowdOh.wav"], [S,"sfx/CrowdAw.wav"], [S,"sfx/coqui.mp3"]], # A press
        [[S, "sfx/heavenly-music.mp3"], [S,"sfx/air-horn.mp3"], [S,"sfx/vine-boom.mp3"], None],    # B press
        [None, None, [S, "sfx/mmm-6.mp3"], None],]         # A + B

# button-based macros

macros = {"Home" : [K,"ctrl+down"],
          "Minus": [K,"ctrl+left"],
          "Plus" : [K,"ctrl+right"]}

wiideck(cmds, g(threshold), macros)