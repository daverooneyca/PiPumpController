import time
import traceback
import logging
import slack
from enum import Enum
import RPi.GPIO as GPIO
import switch_control

class SwitchState(Enum):
    OFF = 0
    ON = 1

class FloatState(Enum):
    TOP = 0
    BOTTOM = 1

# PumpControlApp
class PumpControlApp(object):
    start_delay_time   = 10.0 # Seconds
    shutoff_delay_time = 30.0 # Seconds

    pump_start_time = None
    pump_duration   = 0.0

    logger = None

    def __init__(self, switch_controller):
        self.switch_controller = switch_controller

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Setup event on pin 18 rising edge to detect when the float switch changes state
        GPIO.add_event_detect(18, GPIO.BOTH, callback=self.float_state_changed) 

        self.logger = logging.getLogger('pump_control')
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('./pump_control.log')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        
        sh = slack.SlackHandler("https://hooks.slack.com/services/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")
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def cleanup(self):
        GPIO.cleanup()

    def state_for(self, float_state):
        if(float_state == 0):
            return SwitchState.ON

        return SwitchState.OFF

    def notify(self, switch_state):
        message = ""

        if (switch_state == SwitchState.ON):
            message = "Pump ON"
        else:
            message = "Pump OFF"

            if (self.pump_duration > 0.0):
                message = message + ": %d seconds" % self.pump_duration

                self.pump_duration = 0.0

        self.logger.info(message)

    def float_state_changed(self, event):
        float_state = GPIO.input(18)
        self.logger.debug("Float State: %d" % float_state)

        switch_state = self.state_for(float_state)

        if (switch_state == SwitchState.ON):
            time.sleep(self.start_delay_time)
            self.logger.debug("Float is at top threshold: POWER ON")
            self.switch_controller.switch_on()

            if (self.pump_start_time == None):
                self.pump_start_time = time.time()
            
        if (switch_state == SwitchState.OFF):
            # Delay switching the pump off in order to account for backflow 
            time.sleep(self.shutoff_delay_time)
            self.logger.debug("Float is at bottom threshold: POWER OFF")
            self.switch_controller.switch_off()

            if (self.pump_start_time != None):
                self.pump_duration = time.time() - self.pump_start_time
                self.pump_start_time = None
            
        self.notify(switch_state)

    def start(self):
        self.logger.info("Starting Pump Controller")

        # Manually call the state changed callback in order to detect the initial state of the switch
        self.float_state_changed(None)

        try:
            while True:
                time.sleep(1)
            
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            self.logger.error("Pump control stopped by user")

        # Catch and record any other exceptions
        except:
            self.logger.critical(traceback.format_exc())

        finally:
            self.cleanup()

if __name__ == "__main__":
    app = PumpControlApp(switch_control.SwitchController())

    app.initialize()
    app.start()
