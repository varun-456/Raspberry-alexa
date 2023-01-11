import RPi.GPIO as GPIO
import time
from threading import Thread


class Disco(Thread):
    def __init__(self, lib):
        super().__init__()
        self.lib = lib  # Current instance of th lib class

    def run(self):

        while True:
            self.lib.disco_status = "on"  # checking the status
            if self.lib.disco_stop == 0:
                for i in range(1, 8):
                    if self.lib.disco_stop == 0:
                        result = self.lib.getbinary(i)
                        x, y, z = result[0], result[1], result[2]
                        data = tuple(
                            [
                                self.lib.red,
                                self.lib.blue,
                                self.lib.green,
                                self.lib.red1,
                                self.lib.blue1,
                                self.lib.green1,
                                self.lib.red2,
                                self.lib.blue2,
                                self.lib.green2,
                            ]
                        )
                        self.lib.start(x, y, z, data, typ="all", disco=True)
                        time.sleep(0.1)
                    else:
                        self.lib.start(1, 1, 1, data, typ="all", disco=True)
                        # self.lib.start(x,y,z,data,typ='all',disco=False)
                        break
            else:
                break


"""
	1. Set the pins 
	2. Turn on the lights
	3. if type == all => disco mode else normal
	4. Display the output
"""


class Lib:
    def __init__(self):
        (
            self.red,
            self.blue,
            self.green,
            self.red1,
            self.blue1,
            self.green1,
            self.red2,
            self.blue2,
            self.green2,
        ) = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.disco_stop = 0
        self.disco_status = "off"

    """
		1. Setting up the pins
		2. Displaying the output in LEDS
	"""

    def start(self, x, y, z, data, typ=None, disco=False):

        # if self.disco_status == "on":
        # 	self.disco_stop = 1
        # elif disco == False:
        # 	self.disco_stop = 0
        # 	self.disco_status = "off"
        # else :
        # 	pass

        if typ == "all":
            self.set_pin(data, typ="all")
        else:
            self.set_pin(data)

        GPIO.output(data[0], x)
        GPIO.output(data[1], y)
        GPIO.output(data[2], z)

        if disco == True:
            GPIO.output(data[3], y)
            GPIO.output(data[4], z)
            GPIO.output(data[5], x)
            GPIO.output(data[6], z)
            GPIO.output(data[7], x)
            GPIO.output(data[8], y)

        if typ == "all":

            GPIO.output(data[3], x)
            GPIO.output(data[4], y)
            GPIO.output(data[5], z)
            GPIO.output(data[6], x)
            GPIO.output(data[7], y)
            GPIO.output(data[8], z)

    """
		1. Initilizing the pins in rasphberry pi
	"""

    def set_pin(self, data, typ=None):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(data[0], GPIO.OUT)
        GPIO.setup(data[1], GPIO.OUT)
        GPIO.setup(data[2], GPIO.OUT)

        if typ == "all":
            GPIO.setup(data[3], GPIO.OUT)
            GPIO.setup(data[4], GPIO.OUT)
            GPIO.setup(data[5], GPIO.OUT)
            GPIO.setup(data[6], GPIO.OUT)
            GPIO.setup(data[7], GPIO.OUT)
            GPIO.setup(data[8], GPIO.OUT)

    """
		1. Get the binary value for the mapped color
	"""

    def getbinary(self, color):

        binary = format(color, "b")

        if len(binary) == 1:
            binary = "00" + binary

        if len(binary) == 2:
            binary = "0" + binary
        index = 0
        for i in binary:
            if index == 0:
                if int(i) == 0:
                    x = 1
                if int(i) == 1:
                    x = 0

            if index == 1:
                if int(i) == 0:
                    y = 1
                if int(i) == 1:
                    y = 0

            if index == 2:
                if int(i) == 0:
                    z = 1
                if int(i) == 1:
                    z = 0

            index += 1
            if index == 3:
                break
        return x, y, z

    """
		1. Turning on all the lights either in disco or normal mode
	"""

    def turn_all_on(self, x, y, z, disco=False):

        self.red = 11
        self.blue = 15
        self.green = 13

        self.red1 = 29
        self.blue1 = 33
        self.green1 = 31

        self.red2 = 35
        self.blue2 = 40
        self.green2 = 37

        # Make thread for this

        if disco == True:

            self.disco_stop = 0
            dis = Disco(self)
            dis.start()

        else:
            data = tuple(
                [
                    self.red,
                    self.blue,
                    self.green,
                    self.red1,
                    self.blue1,
                    self.green1,
                    self.red2,
                    self.blue2,
                    self.green2,
                ]
            )
            self.start(x, y, z, data, typ="all")

        return "turning all lights on"

    """
		1. Turning led on 
	"""

    def led_on(
        self, number, x, y, z, LEDONE, LEDTWO, LEDTHREE, status, disco_status=None
    ):

        if self.disco_stop == 0 and disco_status == False:
            self.disco_stop = 1
            time.sleep(0.1)

        if number == "all":
            if x == 1 and y == 1 and z == 1:
                self.disco_stop = 1
            return self.turn_all_on(x, y, z)

        if number in LEDONE:

            self.red = 11
            self.blue = 15
            self.green = 13
            data = tuple([self.red, self.blue, self.green])
            self.start(x, y, z, data)
            return "turning {} lights".format(status)

        elif number in LEDTWO:

            print("hii2")
            self.red = 29
            self.blue = 33
            self.green = 31
            data = tuple([self.red, self.blue, self.green])
            self.start(x, y, z, data)
            return "turning {} lights".format(status)

        elif number in LEDTHREE:

            print("hii3")
            self.red = 35
            self.blue = 40
            self.green = 37
            data = tuple([self.red, self.blue, self.green])
            self.start(x, y, z, data)
            return "turning {} lights".format(status)

    """
		1. Turning led off
	"""

    def led_off(self, number, x, y, z, LEDONE, LEDTWO, LEDTHREE, status):

        if number in LEDONE:
            self.red = 11
            self.blue = 15
            self.green = 13
            data = tuple([self.red, self.blue, self.green])
            print(x, y, z)
            self.start(x, y, z, data)
            # return "turning {} lights".format(status)

        elif number in LEDTWO:
            print("hii2")
            self.red = 29
            self.blue = 33
            self.green = 31
            data = tuple([self.red, self.blue, self.green])
            self.start(x, y, z, data)
            return "turning {} lights".format(status)

        elif number in LEDTHREE:
            print("hii3")
            self.red = 35
            self.blue = 37
            self.green = 40
            data = tuple([self.red, self.blue, self.green])
            start(x, y, z, data)

        return "turning {} lights".format(status)
