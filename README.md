# pico-macro-pad
Make a macro-pad using a Raspberry pi pico and circuit python

<img src="git_assets/macro-pad.jpg" alt="macro-pad" width="300">
___

## 1. Wiring Diagram
![wiring](git_assets/wiring.jpg)

## [2. STL via thingiverse](https://www.thingiverse.com/thing:4816077)

## 3. Code
1. download circuitPython [here](https://circuitpython.org/board/raspberry_pi_pico/)
2. follow instructions to install circuit python onto your Raspberry pi pico
3. clone repo - `git clone https://github.com/jaysongiroux/pico-macro-pad.git`
4. copy main.py, boot.py and lib/ onto your pico
5. reboot

## Macros
`main.py` can be edited to use different macros, supporting strings, key combinations and media control keys

```
# String:
(8): (STRING, ["git add .", NEW_LINE]),  # 7

# Media:
(5): (MEDIA, [ConsumerControlCode.SCAN_PREVIOUS_TRACK])

# Key combination:
(0): (KEY, [Keycode.LEFT_CONTROL, Keycode.C]),  # 1
```