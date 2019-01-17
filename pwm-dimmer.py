#!/usr/bin/python
"""
OLA to Raspberry Pi GPIO ports PWM dimmer.

Consumes five DMX channels,

  Intensity. Red, Blue. Green. White

and provides PWM-dimmed output for a RGBW LED
strip.
"""
import RPi.GPIO as IO
from ola.ClientWrapper import ClientWrapper

# GPIO pins associated with R, G, B and W channel in that order
GPIO_PORTS = [12, 13, 18, 19]
# DMX start address
START = 100
# OLA Universe
UNIVERSE = 1

IO.setwarnings(False)
IO.setmode (IO.BCM)

# Callback for new data
def new_data(data):
    intens = data[START-1]
    for (i, p) in enumerate(GPIO_PORTS):
#        print("Index {} addr {} gpio {} rvalue {} intens {} value {} cycle {}".format(
#            i, START+i, p, data[START+i], intens, intens*data[START+i]/255, intens*data[START+i]*100/255/255))
        pwm[p].ChangeDutyCycle(intens * data[START+i] * 100 / 255 / 255)

# Setup
def init_pwm():
    for p in GPIO_PORTS:
        IO.setup(p, IO.OUT)
        pwm[p] = IO.PWM(p, 100)
        pwm[p].start(0)

pwm = {}
init_pwm()
wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(UNIVERSE, client.REGISTER, new_data)
wrapper.Run()
