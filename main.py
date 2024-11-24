import machine
from time import sleep

print("INIT: boot")
machine.freq(250000000)
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
a = 0

def red_0():
    red = machine.Pin(14, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
    red.off()
    
def red_1():
    red = machine.Pin(14, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    #red.on()
    
def white_0():
    white = machine.Pin(15, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
    white.off()
    
def white_1():
    white = machine.Pin(15, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    #white.on()



def put(bit):
    if bit == 0:
        red_0()
        while white == 1:
            a += 1
        red_1()
        while white == 0:
            a += 1

    if bit == 1:
        white_0()
        while red == 1:
            a += 1
        white_1()
        while red == 0:
            a += 1

def get():
    while red == 0 and white == 0:
        a += 1
    
    if red == 0:
        bit = 0
        white_0()
        while red == 0:
            a += 1
        white_1()

    if red == 1:
        bit = 1
        red_0()
        while white == 0:
            a += 1
        red_1()
        
    return bit
