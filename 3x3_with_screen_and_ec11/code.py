import board
import busio
import adafruit_ssd1306
import rotaryio
import displayio
import os
from adafruit_display_shapes.rect import Rect
import re
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

MEDIA = 1
KEY = 2
STRING = 3

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# MULTI-MEDIA
page_1 = [
    [[ConsumerControlCode.MUTE], "MUTE",MEDIA],
    [[ConsumerControlCode.VOLUME_DECREMENT], "V-",MEDIA],
    [[ConsumerControlCode.VOLUME_INCREMENT], "V+",MEDIA],
    [[ConsumerControlCode.SCAN_PREVIOUS_TRACK], "PREV", MEDIA],
    [[ConsumerControlCode.PLAY_PAUSE], "PLAY", MEDIA],
    [[ConsumerControlCode.SCAN_NEXT_TRACK], "NEXT", MEDIA],
    [[Keycode.COMMAND, Keycode.LEFT_SHIFT, Keycode.A], "Z-AUDIO" ,KEY],
    [[Keycode.COMMAND, Keycode.LEFT_SHIFT, Keycode.V], "Z-VIDEO",KEY],
    [[Keycode.RIGHT_GUI, Keycode.RIGHT_SHIFT, Keycode.F13], "AUDIO",KEY], #SCRIPT TO TOGGLE BETWEEN MIC AND SPEAKER
]

page_1_format = [
    f"{page_1[0][1]}      {page_1[1][1]}       {page_1[2][1]}",
    f"{page_1[3][1]}     {page_1[4][1]}    {page_1[5][1]}",
    f"{page_1[6][1]} {page_1[7][1]} {page_1[8][1]}"
]

# OSX
page_2 = [
    [[Keycode.COMMAND, Keycode.LEFT_SHIFT, Keycode.FIVE], "SS",KEY],
    [[Keycode.COMMAND, Keycode.CONTROL, Keycode.Q], "Lock",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY]
]

page_2_format = [
    f"{page_2[0][1]}       {page_2[1][1]}     {page_2[2][1]}",
    f"{page_2[3][1]}      {page_2[4][1]}      {page_2[5][1]}",
    f"{page_2[6][1]}      {page_2[7][1]}      {page_2[8][1]}",
]

# windows
page_3 = [
    [[Keycode.WINDOWS, Keycode.L], "Lock",KEY],
    [[Keycode.WINDOWS, Keycode.LEFT_SHIFT, Keycode.S], "SS",KEY],
    [[], "n/a",KEY],
    # these short cuts are defined in soundSwitch
    [[Keycode.CONTROL, Keycode.ALT, Keycode.F10], "SPEAKER",KEY],
    [[Keycode.CONTROL, Keycode.ALT, Keycode.F12], "AT2020",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY]
]

page_3_format = [
    f"{page_3[0][1]}     {page_3[1][1]}       {page_3[2][1]}",
    f"{page_3[3][1]} {page_3[4][1]}    {page_3[5][1]}",
    f"{page_3[6][1]}      {page_3[7][1]}      {page_3[8][1]}",
]


# MISC
page_4 = [
    [["/all "], "/all", STRING], #all chat within FPS games
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY],
    [[], "n/a",KEY]
]

page_4_format = [
    f"{page_4[0][1]}     {page_4[1][1]}      {page_4[2][1]}",
    f"{page_4[3][1]}      {page_4[4][1]}      {page_4[5][1]}",
    f"{page_4[6][1]}      {page_4[7][1]}      {page_4[8][1]}",
]

pages = [page_1_format, page_2_format, page_3_format, page_4_format]
pages_object = [page_1, page_2, page_3, page_4]
page_names = ["Page 1 - MULTIMEDIA", "Page 2 - OSX", "Page 3 - WINDOWS", "Page 4 - MISCELLANEOUS"]
current_page = 0

# macro keys GPIO Pins
pins = [
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP7,
    board.GP6,
    board.GP5,
    board.GP8,
    board.GP9,
    board.GP10
]

keymap = {
    (0): (pages_object[current_page][0][2], pages_object[current_page][0][0]),
    (1): (pages_object[current_page][1][2], pages_object[current_page][1][0]),
    (2): (pages_object[current_page][2][2], pages_object[current_page][2][0]),
    (3): (pages_object[current_page][3][2], pages_object[current_page][3][0]),
    (4): (pages_object[current_page][4][2], pages_object[current_page][4][0]),
    (5): (pages_object[current_page][5][2], pages_object[current_page][5][0]),
    (6): (pages_object[current_page][6][2], pages_object[current_page][6][0]),
    (7): (pages_object[current_page][7][2], pages_object[current_page][7][0]),
    (8): (pages_object[current_page][8][2], pages_object[current_page][8][0])
}

switches = [0, 1, 2, 3, 4, 5, 6, 7, 8]

for i in range(9):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]


# Setting up encoder button
# encoder_button_pin = board.GP11
# encoder_button_input = DigitalInOut(encoder_button_pin)
# encoder_button_input.switch_to_input(pull=Pull.UP)
# encoder_button = Debouncer(encoder_button_input)

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
encoder = rotaryio.IncrementalEncoder(board.GP18, board.GP19)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

last_position = 0

def left_or_right(position, last_position):
    if position > last_position:
        return "right"
    elif position < last_position:
        return "left"
    return None

def boot_display():
    display.fill(0)
    display.text(page_names[current_page], 0, 0, 1)
    display.text(pages[current_page][0], 0, 16, 1)
    display.text(pages[current_page][1], 0, 36, 1)
    display.text(pages[current_page][2], 0, 55, 1)
    display.show()

def assignKeyMap():
    return {
        (0): (pages_object[current_page][0][2], pages_object[current_page][0][0]),
        (1): (pages_object[current_page][1][2], pages_object[current_page][1][0]),
        (2): (pages_object[current_page][2][2], pages_object[current_page][2][0]),
        (3): (pages_object[current_page][3][2], pages_object[current_page][3][0]),
        (4): (pages_object[current_page][4][2], pages_object[current_page][4][0]),
        (5): (pages_object[current_page][5][2], pages_object[current_page][5][0]),
        (6): (pages_object[current_page][6][2], pages_object[current_page][6][0]),
        (7): (pages_object[current_page][7][2], pages_object[current_page][7][0]),
        (8): (pages_object[current_page][8][2], pages_object[current_page][8][0])
    }

boot_display()

while True:
    position = encoder.position
    comparison = left_or_right(position, last_position)
    if comparison:
        if comparison == "right" and current_page < len(pages)-1:
            current_page = current_page + 1
            keymap = assignKeyMap()
            boot_display()
        elif comparison == "left" and current_page != 0:
            current_page = current_page - 1
            keymap = assignKeyMap()
            boot_display()

    last_position = position
    for button in range(9):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    elif keymap[button][0] == STRING:
                        for letter in keymap[button][1][0]:
                            layout.write(letter)
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
