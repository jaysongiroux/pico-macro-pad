import board
import busio
import adafruit_ssd1306
import rotaryio
import displayio
import os
from adafruit_display_shapes.rect import Rect
import re

# max length is 5
cat = [
    "Pico-Pad V1.0",
    "Communication",
    "Multi-media",
    "VS-Code",
    "Figma",
    "Settings"
]

main_menu = [
    [cat[0], 25, 0, 1],
    [cat[1], 5, 16, 1],
    [cat[2], 5, 26, 1],
    [cat[3], 5, 36, 1],
    [cat[4], 5, 46, 1],
    [cat[5], 5, 56, 1]
]

map_1 = {}
map_2 = {}
map_3 = {}
map_4 = {}

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
encoder = rotaryio.IncrementalEncoder(board.GP18, board.GP19)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

last_position = None
menu_index = 1

# draw menu with no selection
def static_menu():
    display.fill(0)
    display.show()
    for menu in main_menu:
        display.text(menu[0], menu[1], menu[2], menu[3])

def remove_arrow():
    global main_menu
    temp = []
    for a in main_menu:
        t = a
        t[0] = re.sub("> ", "", t[0])
        temp.append(t)
    main_menu = temp

# add a ">" next to the option selected
def draw_select(position):
    global menu_index, main_menu
    if position > last_position:
        if menu_index > 1:
            menu_index -= 1

    else:
        if menu_index < len(cat) - 1:
            menu_index += 1

    remove_arrow()
    main_menu[menu_index][0] = main_menu[menu_index][0][:0] + "> "\
        + main_menu[menu_index][0][0:]
    static_menu()
    display.show()

static_menu()
display.show()

while True:
    position = encoder.position
    if last_position is not None and position != last_position:
        draw_select(position)

    last_position = position
