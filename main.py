import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# list of pins to use (skipping GP15 on Pico because it's funky)
pins = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
]

MEDIA = 1  # this can be for volume, media player, brightness etc.
KEY = 2
STRING = 3
NEW_LINE = "NEW_LINE"

keymap = {
    (0): (KEY, [Keycode.LEFT_CONTROL, Keycode.C]),  # 1
    (1): (KEY, [Keycode.LEFT_CONTROL, Keycode.V]),  # 2
    (2): (KEY, [Keycode.LEFT_CONTROL, Keycode.Z]),  # 3
    (3): (MEDIA, [ConsumerControlCode.SCAN_NEXT_TRACK]),
    (4): (MEDIA, [ConsumerControlCode.PLAY_PAUSE]),  # 5
    (5): (MEDIA, [ConsumerControlCode.SCAN_PREVIOUS_TRACK]),  # 4
    (6): (STRING, ["git push", NEW_LINE]),
    (7): (STRING, ["git commit -s", NEW_LINE]),  # 8
    (8): (STRING, ["git add .", NEW_LINE]),  # 7
}
switches = [0, 1, 2, 3, 4, 5, 6, 7, 8]

for i in range(9):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    for button in range(9):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    elif keymap[button][0] == STRING:
                        for letter in keymap[button][1][0]:
                            layout.write(letter)
                        if keymap[button][1][1] == NEW_LINE:
                            kbd.press(*[Keycode.RETURN])
                            kbd.release(*[Keycode.RETURN])
                    else:
                        cc.send(keymap[button][1][0])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])
                except ValueError:
                    pass
                switch_state[button] = 0
    time.sleep(0.01)  # debounce
