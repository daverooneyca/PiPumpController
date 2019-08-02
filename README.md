# PiPumpController
Python app to control a sump pump via a Raspberry Pi

This app uses a Raspberry Pi (in my case a Pi Zero W) with a float switch to determine when a sump pump needs to be run. The float switch in this version is a simple single switch, which is why the code has some intelligence built-in to allow it to run a bit longer than when the float switch opens in order to allow the water level to drop enough.

This version was used with a submersible pump that was able to run dry. Earlier versions used an ultrasonic distance sensor and had a pump that couldn't run dry, which led to issues when spurious readings were received from the sensor.
