import sys
import time 
import logging
import RPi.GPIO as GPIO

class SwitchController(object):
    current_switch_state = False # off
    power_pin = 0

    def __init__(self, power_pin=17):
        GPIO.setmode(GPIO.BCM) 
 
        self.power_pin = power_pin
 
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.output(self.power_pin, True)

    def switch_off(self):
        GPIO.output(self.power_pin, True)
        self.current_switch_state = False # off

    def switch_on(self):
        GPIO.output(self.power_pin, False)
        self.current_switch_state = True # on

    def is_on(self):
        return self.current_switch_state == True

    def is_off(self):
        return self.current_switch_state == False

    def cleanup(self):
        GPIO.cleanup()

