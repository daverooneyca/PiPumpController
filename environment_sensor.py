import sys
import Adafruit_DHT
import time
import os
import io
import json
import requests
import traceback
import logging
import slack


class EnvironmentSensor(object):
   reporting_interval = 1800.0 # 30 minutes

   logger = None

   def __init__(self, sensor=11, pin=23):
      self.sensor = sensor
      self.pin = pin

      self.logger = logging.getLogger('environment_sensor')
      self.logger.setLevel(logging.INFO)

      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

      fh = logging.FileHandler('./environment_sensor.log')
      fh.setLevel(logging.INFO)
      fh.setFormatter(formatter)

      sh = slack.SlackHandler("https://hooks.slack.com/services/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")
      sh.setLevel(logging.INFO)
      sh.setFormatter(formatter)

      self.logger.addHandler(fh)
      self.logger.addHandler(sh)

      self.logger.info('Starting Environment Sensor. Reporting Interval: {0:0.1f}sec'.format(self.reporting_interval))

   def report_environment(self):
      humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

      while (humidity > 100.0):
        self.logger.warning("Spurious humidity reading... retrying")
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

      message = 'Temperature: {0:0.1f}C, Humidity: {1:0.1f}%'.format(temperature, humidity)

      self.logger.info(message)

   def start(self):
      try:
         while True:
            self.report_environment()

            time.sleep(self.reporting_interval)
         
      # Reset by pressing CTRL + C
      except KeyboardInterrupt:
         self.logger.error("Environment sensor stopped by user")

      # Catch and record any other exceptions
      except:
         self.logger.critical(traceback.format_exc())


if __name__ == "__main__":
   app = EnvironmentSensor()

   app.start()
