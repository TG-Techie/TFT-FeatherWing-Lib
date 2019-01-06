from adafruit_mini_tft_featherwing.rgb import colorst as color
from adafruit_mini_tft_featherwing.joywing import wing

# wing._disp.
"""
wing._disp.pixel(x, y, color=None)
wing._disp.rect(x, y, width, height, color)
wing._disp.fill(color=0)
wing._disp.hline(x, y, width, color)
wing._disp.vline(x, y, height, color)
wing._disp.text_dimension(x, y, text, size = 1)
wing._disp.text(x, y, text, color(255,255,255), background = color(0,0,0), size = 1, rect_extension = 0, italics = 0)
wing._disp.scroll(x, y, str, color(255,255,255), background = None, size = 1)
wing._disp.round_rect(x, y, width, height, r, color)
"""

# backlight control
"""
wing.backlight_off
wing.backlight_on
"""

wing.backlight_on
wing._disp.pixel(0,0, 255)
wing._disp.rect(5, 5, 150, 50, color(75, 200, 50))
wing._disp.scroll(20, 15, "hello", color(0,70,255), background = None, size = 3)
wing._disp.text(10,55,"This test shows \n if it is working",color(255,255,255), background = color(0,0,0), size = 1, rect_extension = 0, italics = 0)

while True:
    if wing.button_a:
        print("Button A pressed")
    if wing.button_b:
        print("Button B pressed")
    if wing.button_right:
        print("Button Right pressed")
    if wing.button_left:
        print("Button Left pressed")
    if wing.button_up:
        print("Button Up pressed")
    if wing.button_down:
        print("Button Down pressed")
    if wing.button_sel:
        print("Button Select pressed")