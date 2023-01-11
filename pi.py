import RPi.GPIO as GPIO
import time


def main(typ=None):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)
    if typ == "seq":
        GPIO.setup(red1, GPIO.OUT)
        GPIO.setup(green1, GPIO.OUT)
        GPIO.setup(blue1, GPIO.OUT)
        GPIO.setup(red2, GPIO.OUT)
        GPIO.setup(green2, GPIO.OUT)
        GPIO.setup(blue2, GPIO.OUT)


def func_red():
    main()
    print("Initialising Red:")
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.cleanup()


def func_blue():
    main()
    print("Initialising blue:")
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.LOW)
    time.sleep(0.2)
    GPIO.cleanup()


def func_green():
    main()
    print("Initialising green:")
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(blue, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.cleanup()


def start(x, y, z, typ=None):
    print(x, y, z)
    if typ == "seq":
        main(typ="seq")
    else:
        main()
    GPIO.output(red, x)
    GPIO.output(blue, y)
    GPIO.output(green, z)
    if typ == "seq":
        GPIO.output(red1, x)
        GPIO.output(blue1, y)
        GPIO.output(green1, z)
        GPIO.output(red2, x)
        GPIO.output(blue2, y)
        GPIO.output(green2, z)
    if typ == "seq":
        time.sleep(0.1)
    else:
        time.sleep(4)
    # GPIO.cleanup()


def input_driven():

    try:
        while True:

            global red, blue, green

            inp = int(input("Enter the led number:"))

            if inp == 1:

                red = 11
                blue = 15
                green = 13

            if inp == 2:
                red = 29
                blue = 33
                green = 31

            if inp == 3:
                red = 35
                blue = 40
                green = 37

            while True:

                map_dict = {
                    "off": 0,
                    "green": 1,
                    "blue": 2,
                    "cyan": 3,
                    "red": 4,
                    "yellow": 5,
                    "purple": 6,
                    "white": 7,
                }

                col = input("Enter the color:")
                x = map_dict[col]
                binary = format(x, "b")

                if len(binary) == 1:
                    binary = "00" + binary

                if len(binary) == 2:
                    binary = "0" + binary
                print(binary)
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

                start(x, y, z)
                break

    except KeyboardInterrupt:
        GPIO.cleanup()


def seq():
    global red
    global blue
    global green
    global red1
    global blue1
    global green1
    global red2
    global blue2
    global green2

    red = 11
    blue = 15
    green = 13

    red1 = 29
    blue1 = 31
    green1 = 33

    red2 = 35
    blue2 = 37
    green2 = 40
    try:

        while True:

            for i in range(1, 8):
                binary = format(i, "b")

                if len(binary) == 1:
                    binary = "00" + binary
                if len(binary) == 2:
                    binary = "0" + binary
                    print(binary)
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

                start(x, y, z, typ="seq")

    except KeyboardInterrupt:
        GPIO.cleanup()


seq()
# input_driven()
