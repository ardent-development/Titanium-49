import machine
from time import sleep

print("INIT: boot")
machine.freq(250000000) # This level of OC causes no problems on every Pico board, and only speeds up the Python interpreter.
led = machine.Pin("LED", machine.Pin.OUT)
led.on() # Power indicator

gpio_red   = 14  # Modify these if needed.
gpio_white = 15  # Any GPIO should work on the RP2040.

red = machine.Pin(gpio_red, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
white = machine.Pin(gpio_white, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)


## Communication functions: defined in order of abstraction, ascending

# set_red(state): sets the red wire to a low (0) or high (1) state
#  - state: bool
#  - returns: nothing
def set_red(state):
    if state != 0 and state != 1:
        raise ValueError("State must be set to 0 or 1.")    

    if state == 0:
        red = machine.Pin(gpio_red, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        red.off()
    if state == 1:
        red = machine.Pin(gpio_red, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        red.on()
        
# set_white(state): sets the white wire to a low (0) or high (1) state
#  - state: bool
#  - returns: nothing
def set_white(state):
    if state != 0 and state != 1:
        raise ValueError("State must be set to 0 or 1.")

    if state == 0:
        white = machine.Pin(gpio_white, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        white.off()
    if state == 1:
        white = machine.Pin(gpio_white, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        white.on()


# put_bit(bit): sends a bit across the link
#  - bit: bool
#  - returns: nothing
def put_bit(bit):
    if bit != 0 and bit != 1:
        raise ValueError("Bit must be set to 0 or 1.")    

    if bit == 0:
        set_red(0)
        while white.value() == 1:
            pass
        set_red(1)
        while white.value() == 0:
            pass
    
    if bit == 1:
        set_white(0)
        while red.value() == 1:
            pass
        set_white(1)
        while red.value() == 0:
            pass

# get_bit(): gets a bit from the link
#  - returns: bool containing the bit gotten from the link
def get_bit() -> bool:
    while red.value() == 0 or white.value() == 0:
        pass
    
    if red.value() == 0:
        bit = 0
        set_white(0)
        while red.value() == 0:
            pass
        set_white(1)

    if red.value() == 1:
        bit = 1
        set_red(0)
        while white.value() == 0:
            pass
        set_red(1)
        
    return bit


put_bit(0) # 08
put_bit(0)
put_bit(0)
put_bit(1)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)

put_bit(1) # 87
put_bit(1)
put_bit(1)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(1)

put_bit(1) # 31
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(1)
put_bit(1)
put_bit(0)
put_bit(0)

put_bit(0) # 00
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)
put_bit(0)


set_red(1)
set_white(1)
