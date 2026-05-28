import threading
import time

import hid


def connect():
    """
    automagically tries both variants of the Wiimote,
    Normal and Plus Inside
    """
    dev = hid.device()
    try:
        dev.open(1406, 816)
    except:
        dev.open(1406, 774)

    return WiiMote(dev)


class Accelerometer(object):
    MODES = [0x31, 0x33]

    def __init__(self, wiimote):
        self._state = [0.0, 0.0, 0.0]
        self._wiimote = wiimote
        self._com = wiimote._com

    def __len__(self):
        return len(self._state)

    def __repr__(self):
        return repr(self._state)

    def __getitem__(self, axis):
        if 0 <= axis <= 2:
            return self._state[axis]
        else:
            return [0]

    def handle(self, data):
        x_tmp, y_tmp, z_tmp = data[3:6]
        x = (x_tmp << 2) + ((data[1] & 0b01100000) >> 5)
        y = (y_tmp << 2) + ((data[2] & 0b00100000) >> 4)
        z = (z_tmp << 2) + ((data[2] & 0b01000000) >> 5)
        self._state = [x, y, z]


class Buttons(object):
    BTNS = {
        "Left":  0x0100,
        "Right": 0x0200,
        "Down":  0x0400,
        "Up":    0x0800,
        "Plus":  0x1000,
        "Home":  0x0080,
        "Minus": 0x0010,
        "A":     0x0008,
        "B":     0x0004,
        "1":     0x0002,
        "2":     0x0001,
    }

    def __init__(self, wiimote):
        self._wiimote = wiimote
        self._com = wiimote._com
        self._state = {}
        for btn in list(self.BTNS.keys()):
            self._state[btn] = False

    def __len__(self):
        return len(self._state)

    def __repr__(self):
        return repr(self._state)

    def __getitem__(self, btn):
        if btn in self._state:
            return self._state[btn]
        else:
            raise KeyError

    def handle(self, data):
        btn_bytes = (data[1] << 8) + data[2]
        new_state = {}
        for btn, mask in list(self.BTNS.items()):
            new_state[btn] = bool(mask & btn_bytes)
        self._update(new_state)

    def _update(self, new_state):
        for btn, state in list(new_state.items()):
            if self._state[btn] != state:
                self._state[btn] = state


class LEDs(object):
    def __init__(self, wiimote):
        self.state = [False, False, False, False]
        self._com = wiimote._com
        self.wiimote = wiimote
        
    def __getitem__(self, led_no):
        if 0 <= led_no <= 3:
            return self.state[led_no]
        else:
            return False
    
    def __setitem__(self, led_no, val):
        new_led_state = self.state
        try:
            new_led_state[led_no] = True if val else False
            self.set_leds(new_led_state)
        except:
            print("LED failure!")

    def set_leds(self, ledlist):
        for num, val in enumerate(ledlist):
            self.state[num] = True if val else False
        out = 0x0 
        for val, st in zip([0x10, 0x20, 0x40, 0x80], self.state):
            if st:
                out += val
        self._com.send(0x11, out)


class Rumbler(object):
    def __init__(self, wiimote):
        self.state = False
        self.wiimote = wiimote

    def set_rumble(self, st):
        self.state = st
        self.wiimote._com.set_rumble(st)

    def rumble(self, length=0.5):
        t = threading.Timer(length, self.set_rumble, [False])
        t.start()
        self.set_rumble(True)


class Comms(threading.Thread):
    def __init__(self, wiimote):
        threading.Thread.__init__(self)
        self.wiimote = wiimote
        self.lastsent = None

    def send(self, *bytes):
        # print("sending", bytes)
        self.wiimote.device.write(bytes)
        if self.lastsent is None or bytes != self.lastsent:
            self.lastsent = bytes

    def run(self):
        self.running = True
        while self.running:
            data = self.wiimote.device.read(32)
            self.process(data)
            time.sleep(0.001)

    def process(self, data):
        self.wiimote.buttons.handle(data)
        if len(data) > 3: 
            self.wiimote.accelerometer.handle(data)

    def set_rumble(self, state):
        if state:
            bit = 0x01
        else:
            bit = 0x00
        self.send(0x10, bit)


class WiiMote(object):
    def __init__(self, dev):
        self.device = dev
        self.device.write([0x12,0x00,0x31])
        self._com = Comms(self)
        self.leds = LEDs(self)
        self.accelerometer = Accelerometer(self)
        self.buttons = Buttons(self)
        self.rumbler = Rumbler(self)

        self._com.start()

