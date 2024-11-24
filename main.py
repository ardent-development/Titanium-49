import machine
from time import sleep

print("INIT: boot")
machine.freq(250000000)
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

red = machine.Pin(14, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
white = machine.Pin(15, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
print("Set to in")
red = machine.Pin(14, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
white = machine.Pin(15, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
print("Set to out")

def put(bit):
    if bit is 1:
        red = machine.Pin(14, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        
def red_0():
    red = machine.Pin(14, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
    red.on()
    
def red_1():
    red = machine.Pin(14, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    #red.on()
    
def white_0():
    red = machine.Pin(15, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
    red.on()
    
def white_1():
    red = machine.Pin(15, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    #red.on()
