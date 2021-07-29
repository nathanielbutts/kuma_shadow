#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import subprocess

def shutdown(pin):
    # we will use the pin numbering to match the pins on the Pi, instead of the 
    # GPIO pin outs (makes it easier to keep track of things)

    GPIO.setmode(GPIO.BOARD)  

    # use the same pin that is used for the reset button (one button to rule them all!)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

    oldButtonState1 = True

    while True:
        buttonState1 = GPIO.input(5) #grab the current button state

    # check to see if button has been pushed
        if buttonState1 != oldButtonState1 and buttonState1 == False:
            subprocess.call("shutdown -h now", shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            oldButtonState1 = buttonState1

            time.sleep(.1)