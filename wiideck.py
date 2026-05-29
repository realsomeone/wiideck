import time
import actions

K = 1
S = 0

def g(g): # to wii
    return 100*g

# def upthresh():
#     global gs, thresh
#     gs += 0.1
#     thresh = g(gs)

# def downthresh():
#     global gs, thresh
#     gs -= 0.1
#     thresh = g(gs)

def wiideck(actionmatrix, thresh, xtras):
    import wiimote

    input("Press SYNC, then hit enter... ")
    mote = wiimote.find()[0]
    wm = wiimote.connect(mote[0])

    print("connected!")
    
    mainloop(actionmatrix, thresh, xtras, wm)
    
def mainloop(actionmatrix, thresh, xtras, wm):
    
    wm.leds[3] = True
    saved = time.time()
    time.sleep(1)
    curr = wm.accelerometer
    last = tuple(curr[i] for i in range(3))
    cooldown = 0.250
    
    while True:
        d = False
        now = time.time()

        if wm.buttons["A"]:
            wm.leds[0] = True
            mod1 = True
        else:
            wm.leds[0] = False
            mod1 = False
        
        if wm.buttons["B"]:
            wm.leds[1] = True
            mod2 = True
        else:
            wm.leds[1] = False
            mod2 = False
        
        diffx = curr[0] - last[0]
        diffz = curr[2] - last[2]
        last = tuple(curr[i] for i in range(3))

        if now - saved > cooldown:

            act = -1

            if abs(diffx) > abs(diffz):
                if diffx < thresh*-1:
                    act = 3; d = True
                elif diffx > thresh:
                    act = 1; d = True
            else:
                if diffz < thresh*-1:
                    act = 0; d = True
                elif diffz > thresh:
                    act = 2; d = True

        mod = (1 if mod1 else 0) + (2 if mod2 else 0)

        for bt in xtras:
            if wm.buttons[bt]:
                wm.rumbler.rumble(0.2)
                execute(xtras[bt])
                while wm.buttons[bt]:
                    time.sleep(1/50)

        if act != -1:
            res = actionmatrix[mod][act]
            if res is not None:
                wm.rumbler.rumble(0.2)
                execute(res)

        if d:
            act = -1
            saved = time.time()
        
        time.sleep(1/50)
        
def execute(action):
    if action[0] == K: actions.bind(action[1])
    else: actions.sfx(action[1])

def wiimac(actionmatrix, thresh, xtras):
    import macwiimote as wiimote
    
    input("Connect WiiMote with WiiMacMote and press enter...")
    wm = wiimote.connect()
    
    print("connected!")

    mainloop(actionmatrix, thresh, xtras, wm)