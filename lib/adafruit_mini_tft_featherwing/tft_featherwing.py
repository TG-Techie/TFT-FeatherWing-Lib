# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2017-2018 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# We have a lot of attributes for this complex library.
# pylint: disable=too-many-instance-attributes

"""
`adafruit_mini_tft_featherwing.joywing`
====================================================

CircuitPython driver for `Mini Color TFT with Joystick FeatherWing
<https://www.adafruit.com/product/3321>`_.

* Author(s): hexthat
"""

from adafruit_mini_tft_featherwing.st7735r import ST7735R
from adafruit_seesaw import seesaw as ss
from adafruit_seesaw import digitalio as dio
from adafruit_seesaw import pwmout as pwm
from micropython import const
import board
import busio
import digitalio
import sys
# pylint: disable=wrong-import-position
try:
    lib_index = sys.path.index("/lib")        # pylint: disable=invalid-name
    if lib_index < sys.path.index(".frozen"):
        # Prefer frozen modules over those in /lib.
        sys.path.insert(lib_index, ".frozen")
except ValueError:
    # Don't change sys.path if it doesn't contain "lib" or ".frozen".
    pass

__version__ = "0.0.0-auto.0"


class Joywing:     # pylint: disable=too-many-public-methods
    """Represents a single mini tft featherwing. Do not use more than one at
       a time."""
    def __init__(self, _disp_sck = board.SCK, _disp_mosi = board.MOSI, _disp_miso = board.MISO, _disp_cs = board.D5, _disp_dc = board.D6, adress = 94):
        # Only create the joywing module member when we're aren't being imported by Sphinx
        if ("__module__" in dir(digitalio.DigitalInOut) and
                digitalio.DigitalInOut.__module__ == "sphinx.ext.autodoc"):
            return
        
        #SPI
        self._disp_sck = _disp_sck
        self._disp_mosi = _disp_mosi
        self._disp_miso = _disp_miso
        # DS and CS pins
        self._disp_cs = _disp_cs
        self._disp_dc = _disp_dc
        
        #I2C
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._seesaw = ss.Seesaw(self._i2c, adress)
        self._backlight_pin = pwm.PWMOut(self._seesaw, 5)
        self._disp_rst = dio.DigitalIO(self._seesaw, 8)
        self._disp_spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        
        # pylint: disable=bad-whitespace
        self._BUTTON_RIGHT = const(7)
        self._BUTTON_DOWN = const(4)
        self._BUTTON_UP = const(2)
        self._BUTTON_LEFT = const(3)
        self._BUTTON_B = const(9)
        self._BUTTON_A = const(10)
        self._BUTTON_SEL = const(11)
        # pylint: enable=bad-whitespace
        self._button_mask = const((1 << self._BUTTON_RIGHT) |
                            (1 << self._BUTTON_DOWN) |
                            (1 << self._BUTTON_UP) |
                            (1 << self._BUTTON_LEFT) |
                            (1 << self._BUTTON_B) |
                            (1 << self._BUTTON_A) |
                            (1 << self._BUTTON_SEL))
        self._seesaw.pin_mode_bulk(self._button_mask, self._seesaw.INPUT_PULLUP)

        # initilise stuff
        # start backlight in off position
        self._backlite = (self._backlight_pin)
        self._backlite.duty_cycle = 0xffff

        # setup the display as a car named "disp"
        self._disp = ST7735R(self._disp_spi, cs=digitalio.DigitalInOut(self._disp_cs), dc=digitalio.DigitalInOut(self._disp_dc),
                       rst=(self._disp_rst), rotation=3)
        self._disp.y_offset = 24
        # clear screen
        self._clear()

    def _clear(self):
        self._disp.fill(0)
    
    '''
    def backlight_off(self):
        self._backlite.duty_cycle = 255
    
    
    def backlight_on(self):
        self._backlite.duty_cycle = 0'''
        
    @property
    def backlight(self):
        return self._backlite.duty_cycle
    
    @backlight.setter
    def backlight(self, value):
        self._backlite.duty_cycle = int(255*  max( 0, min( 1, (1-value) )) )
        
    
    @property
    def button_up(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_UP):
            return True
        else:
            return False

    @property
    def button_down(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_DOWN):
            return True
        else:
            return False

    @property
    def button_right(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_RIGHT):
            return True
        else:
            return False

    @property
    def button_left(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_LEFT):
            return True
        else:
            return False

    @property
    def button_a(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_A):
            return True
        else:
            return False

    @property
    def button_b(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_B):
            return True
        else:
            return False

    @property
    def button_sel(self):
        buttons = self._seesaw.digital_read_bulk(self._button_mask)
        if not buttons & (1 << self._BUTTON_SEL):
            return True
        else:
            return False


wing = Joywing() # pylint: disable=invalid-name
"""Object that is automatically created on import.

   To use, simply import it from the module:

   .. code-block:: python

     from adafruit_mini_tft_featherwing.joywing import wing
"""