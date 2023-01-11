import logging
import os
import time

from flask import Flask
from flask_ask import Ask, request, session, question, statement
from lib_class import Lib


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

STATUSON = ["on", "high", "all"]
STATUSOFF = ["off", "low"]

LEDONE = ["1", "1st"]
LEDTWO = ["2", "second"]

LEDTHREE = ["3", "3rd"]
COLOUR = ["green", "blue", "cyan", "red", "yellow", "purple", "white"]

# Creating a object for library
rp = Lib()


@ask.launch
def launch():
    speech_text = "Welcome to Raspberry Pi Automation."
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent(
    "GpioIntent", mapping={"status": "status", "number": "number", "colour": "colour"}
)
def Gpio_Intent(number, colour, room, status):

    print("Status", status)
    disco = False
    if status == None:
        status = "on"
    else:
        status = "off"

    if colour == None:
        colour = "off"

    if colour == "disco":
        disco = True

    print(number)
    print(status)
    print(colour)

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

    if disco == True:
        rp.turn_all_on(0, 0, 0, disco=True)  # Turning on the disco mode
        return statement("Disco turned on")

    if colour not in map_dict:
        return statement("Sorry not possible.")

    color = map_dict[colour]
    result = rp.getbinary(color)  # Getting binary value for the number

    x, y, z = result[0], result[1], result[2]
    print(x, y, z)
    print("status:", status)

    if status in STATUSON:
        print("i am going to on")
        data = rp.led_on(
            number, x, y, z, LEDONE, LEDTWO, LEDTHREE, status, False
        )  # Turning on the LED
        return statement("Okay")

    elif status in STATUSOFF:
        print("i am going to off")
        data = rp.led_off(
            number, x, y, z, LEDONE, LEDTWO, LEDTHREE, status
        )  # Turning off the LED
        return statement("Okay")

    else:
        return statement("Sorry not possible.")


@ask.intent("AMAZON.HelpIntent")
def help():
    speech_text = "You can say hello to me!"
    return (
        question(speech_text)
        .reprompt(speech_text)
        .simple_card("HelloWorld", speech_text)
    )


@ask.session_ended
def session_ended():
    return statement("Okay")


if __name__ == "__main__":
    if "ASK_VERIFY_REQUESTS" in os.environ:
        verify = str(os.environ.get("ASK_VERIFY_REQUESTS", "")).lower()
        if verify == "false":
            app.config["ASK_VERIFY_REQUESTS"] = False
    app.run(debug=True)
