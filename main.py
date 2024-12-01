# Titanium-49 v0.0.8
# Contributors to this file:
#   - twisted_nematic57
# Licensed under GNU GPLv3. See /LICENSE for more info.

import machine
import rp2
import sys
from time import *

print("T49 INIT: boot")
machine.freq(125 * 1000 * 1000) # Initial low clock due to wireless chip-connected power indicator shenanigans
led = machine.Pin("LED", machine.Pin.OUT)
led.on() # Power indicator
machine.freq(280 * 1000 * 1000) # Now that the wireless chip is out of the way...

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
@micropython.native
def set_red(state):
    if state == 0:
        red = machine.Pin(gpio_red, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        red.off()
    if state == 1:
        red = machine.Pin(gpio_red, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

# set_white(state): sets the white wire to a low (0) or high (1) state
#  - state: bool
# returns: nothing
@micropython.native
def set_white(state):
    if state == 0:
        white = machine.Pin(gpio_white, mode=machine.Pin.OUT, pull=machine.Pin.PULL_UP)
        white.off()
    if state == 1:
        white = machine.Pin(gpio_white, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)


## Bitwise I/O

# put_bit(bit): sends a bit across the link
#  - bit: bool
# returns: nothing
@micropython.native
def put_bit(bit):
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
# returns: bool containing the bit gotten from the link
@micropython.viper # Repeatedly called thousands of times in screenshotting function. Absolute performance is of the essence.
def get_bit() -> bool:
    if int(red.value()) == 0:
        set_white(0)
        while int(red.value()) == 0:
            pass
        set_white(1)
        return False # 0

    if int(red.value()) == 1:
        set_red(0)
        while int(white.value()) == 0:
            pass
        set_red(1)
        return True # 1


## Bytewise I/O

# put_byte(): sends a byte across the link in little-endian order
#   - byte: a string containing a [padded if necessary] byte represented in hexadecimal - no prefix needed, should only be 2 characters
# returns: nothing
@micropython.native
def put_byte(byte):
    byte = ''.join(reversed(bin(int(byte,16))[2:])) # Converts the hex to a string containing binary; then reverses it because the serial link is little-endian
    if len(byte) < 8:
        for i in range(0,8-len(byte)): # pad the right side with zeros if it's less than 8 in length
            byte = str(byte) + str("0")

    for each_bit in byte:
        each_bit = int(each_bit) # put_bit accepts numbers, not strings
        put_bit(each_bit)


# get_byte(): gets a byte from the link
# returns: a string containing two lowercase hexadecimal characters (the byte gotten) without a prefix
@micropython.native
def get_byte():
    byte_str = ""
    while red.value() == 1 and white.value() == 1: # if the calc isn't ready to send another bit, don't try getting one!
        pass

    for i in range(8):
        byte_str = str(int(get_bit())) + byte_str # get each bit of the byte and account for the little-endian nature of the link to format it into a big-endian string of 8 bits
    #return "{0:#0{1}x}".format(int(byte_str, 2),4)[-2:]
    return byte_str


##
## Titanium-49 logic begins here
##

@micropython.viper
def geti():
    for i in range(3850):
#        while int(red.value()) == 1 and int(white.value()) == 1:
#            pass
#        print(int(get_bit()),end="")
        print(get_byte(),end="")
        while sys.stdin.readline() != "c\n":
            pass



set_red(1)
set_white(1)


while True:
    if sys.stdin.readline() == "a\n":
        put_byte("08") # This block is temporary.
        put_byte("6d") # For testing purposes only.
        put_byte("00")
        put_byte("00")
        
        x = ticks_us()
        geti()
        y = ticks_us()

        put_byte("08") # This block is temporary.
        put_byte("56")
        put_byte("00")
        put_byte("00")

        #print()
        #print(str((y-x)/1000) + "ms")
        print("")

set_red(1)
set_white(1)
