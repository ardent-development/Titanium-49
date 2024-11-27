# Titanium-49 v0.0.4
# Contributors to this file:
#   - twisted_nematic57
# Licensed under GNU GPLv3. See /LICENSE for more info.

import machine
from time import *

print("INIT: boot")
machine.freq(250000000) # This level of OC causes no problems on every Pico board, and only speeds up the Python interpreter.
led = machine.Pin("LED", machine.Pin.OUT)
led.on() # Power indicator

gpio_red   = 14  # Modify these if needed.
gpio_white = 15  # Any GPIO should work on the RP2040.

red = machine.Pin(gpio_red, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
white = machine.Pin(gpio_white, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)



##
## Miscellaneous functions: filling holes in MicroPython
##

# reverse(string): reverses string
#  - string: string to be reversed
# returns: reversed string
#
# Note: function stolen from https://forum.micropython.org/viewtopic.php?t=5282#p30290
#  - Does not raise an exception if it is called wrongly. I could not figure out how to make it do that.
def reverse(string):
    return "" if not(string) else reverse(string[1::]) + string[0]


##
## Communication functions: defined in order of abstraction, ascending
##


## Low-level electrical signal management

# set_red(state): sets the red wire to a low (0) or high (1) state
#  - state: bool
# returns: nothing
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
# returns: nothing
def set_white(state):
    if state != 0 and state != 1:
        raise ValueError("State must be set to 0 or 1.")

    if state == 0:
        white = machine.Pin(gpio_white, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        white.off()
    if state == 1:
        white = machine.Pin(gpio_white, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
        white.on()


## Bitwise I/O

# put_bit(bit): sends a bit across the link
#  - bit: bool
# returns: nothing
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
# returns: nothing
def get_bit() -> bool:
    if red.value() == 0:
        bit = 0
        set_white(0)
        while red.value() == 0:
            pass
        set_white(1)
        return bit

    if red.value() == 1:
        bit = 1
        set_red(0)
        while white.value() == 0:
            pass
        set_red(1)
        return bit


## Bytewise I/O

# put_byte(): sends a byte across the link in little-endian order
#   - byte: a string containing a [padded if necessary] byte represented in hexadecimal - no prefix needed, should only be 2 characters
# returns: nothing
def put_byte(byte):
    if len(byte) != 2: # only accepts one byte; more than 2 hex chars = >1B; less than 2 means it must be padded with a 0
        raise ValueError("Only one byte is allowed. Single-char representable bytes must be padded with 0.")

    byte = reverse(bin(int(byte,16))[2:]) # Converts the hex to a string containing binary; then reverses it because the serial link is little-endian
    if len(byte) < 8:
        for i in range(0,8-len(byte)): # pad the right side with zeros if it's less than 8 in length
            byte = str(byte) + str("0")
    
    for each_bit in byte:
        each_bit = int(each_bit) # put_bit accepts numbers, not strings
        put_bit(each_bit)


# get_byte(): gets a byte from the link
# returns: a string containing two lowercase hexadecimal characters (the byte gotten) without a prefix
def get_byte():
    sleep_ms(5) # needed for the line to be "usable" again (idk tbh)
    byte_str = ""
    
    for i in range(8):
        byte_str = str(get_bit()) + byte_str # Get each bit of the byte and account for the little-endian nature of the link to format it into a big-endian string of 8 bits
    #return hex(int(byte_str, 2))
    return "{0:#0{1}x}".format(int(byte_str, 2),4)


##
## Titanium-49 specific logic begins here
##

set_red(1)
set_white(1)

put_byte("08") # This block is temporary.
put_byte("87") # For testing purposes only.
put_byte("31")
put_byte("00")
#sleep_ms(1)
#for i in range(32):
#    ab = get_bit()
#    print(ab)
#    #sleep_ms(10)
print(get_byte())
print(get_byte())
print(get_byte())
print(get_byte())


set_red(1)
set_white(1)

