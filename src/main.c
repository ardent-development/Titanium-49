/*** main.c *******************************************************************\
 * Contributors: twisted_nematic57                                            *
 * Copyright:    GNU GPLv3 or later (see LICENSE                              *
 * Description:  Initializes hardware and set up external interfaces; then,   *
 *               runs the main loop                                           *
\******************************************************************************/


// Includes
#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hardware/gpio.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"
#include "pico/time.h"
#include "pico/cyw43_arch.h"

#include <stdio.h>
#include <stdbool.h>

// Defines
#define GPIO_RED   14 // Modify pin numbers if needed
#define GPIO_WHITE 15

#define true 1 // VSCode problem fixing


//
// Convenience functions
//

// reverse(): reverses the order of the bits in a uint8_t
//  - b: a uint8_t to be reversed
// returns: a uint8_t containing the reversed bits
uint8_t reverse(uint8_t b) {
  b = (b & 0b11110000) >> 4 | (b & 0b00001111) << 4; // swap 4-bit halves
  b = (b & 0b11001100) >> 2 | (b & 0b00110011) << 2; // swap each pair
  b = (b & 0b10101010) >> 1 | (b & 0b01010101) << 1; // swap each bit
  return b;
}


//
// Communication Functions - defned in order of abstraction, ascending
//

// Low-level electrical signal management

// set_red(): sets the red wire to a low (0) or high (1) state
//  - state: 0 = low, 1 = high
//     - values other than 0 or 1 will result in setting to high (1)
// returns: nothing
void set_red(bool state) {
  if(state == 0) {
    gpio_set_dir(GPIO_RED,1); // Output
    gpio_put(GPIO_RED,0);
  } else { // state == 1
    gpio_set_dir(GPIO_RED,0); // Input
    gpio_pull_up(GPIO_RED);   // Pull up
  }
}

// set_white(): sets the white wire to a low (0) or high (1) state
//  - state: 0 = low, 1 = high
//     - values other than 0 or 1 will result in setting to high (1)
// returns: nothing
void set_white(bool state) {
  if(state == 0) {
    gpio_set_dir(GPIO_WHITE,GPIO_OUT); // Output
    gpio_put(GPIO_WHITE,0);
  } else { // state == 1
    gpio_set_dir(GPIO_WHITE,GPIO_IN); // Input
    gpio_pull_up(GPIO_WHITE);   // Pull up
  }
}


// Bitwise I/O

// put_bit(): sends a bit across the link
//  - bit: bool
//     - values other than 0 or 1 will result in transmission of a 1 bit
// returns: nothing
void put_bit(bool bit) {
  if(bit == 0) {
    set_red(0);
    while(gpio_get(GPIO_WHITE) == 1) {;} // Wait for other side to ack
    set_red(1);
    while(gpio_get(GPIO_WHITE) == 0) {;} // ^
  } else { // bit == 1
    set_white(0);
    while(gpio_get(GPIO_RED) == 1) {;} // Wait for other side to ack
    set_white(1);
    while(gpio_get(GPIO_RED) == 0) {;} // ^
  }
}

// get_bit(): gets a bit from the link
// returns: bool containing the bit gotten from the link
bool get_bit() {
  if(gpio_get(GPIO_RED) == 0) {
    // Bit == 0
    set_white(0);
    while(gpio_get(GPIO_RED) == 0) {;} // Wait for other side to ack
    set_white(1);
    return 0;
  } else { // red == 1
    // Bit == 1
    set_red(0);
    while(gpio_get(GPIO_WHITE) == 0) {;} // Wait for other side to ack
    set_red(1);
    return 1;
  }
}


// Bytewise I/O

// put_byte(): sends a byte across the link in little-endian order
//   - byte: a uint8_t containing the byte to be sent
// returns: nothing
void put_byte(uint8_t byte) {
	for(uint8_t i = 0; i < 8; i++) {
		put_bit((reverse(byte) << i) & 0b1);
	}
}

// get_byte(): gets a byte from the link
// returns: a uint8_t containing the byte gotten
uint8_t get_byte() {
	uint8_t byte = 0b00000000;
	for(uint8_t i = 7; i >= 0; i--) {
		byte = byte | (get_bit() >> i);
	}
}


//
// Titanium-49 Logic
//

int main() {
  set_sys_clock_hz(250*1000*1000, true); // need for speed
  stdio_init_all(); // USB + UART (8n1,115200)
  stdio_puts("\n\n\nINIT: Boot Titanium-49 v0.2.0 | Copyright 2024 Ardent"
             " Development. Released under the GPLv3 or later.\n");

  if (cyw43_arch_init()) { // Try to init CYW43439
    stdio_puts("ERROR: CYW43439 init failed. Onboard LED capabilities shall be"
               " disabled.");
  } else {
    stdio_puts("INIT: CYW43439 initialized. Infodump below.");
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1); /* Enable onboard LED (power
                                                      indicator) */
		stdio_puts("\n");
  }

  gpio_init(GPIO_RED);        // Set up the I/O wires - Red
  gpio_set_dir(GPIO_RED,GPIO_IN);
  gpio_pull_up(GPIO_RED);
  gpio_init(GPIO_WHITE);      // White
  gpio_set_dir(GPIO_WHITE,GPIO_IN);
  gpio_pull_up(GPIO_WHITE);

	set_red(1);
	set_white(1);

	put_bit(0); // 08
	put_bit(0);
	put_bit(0);
	put_bit(1);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(1); // 87
	put_bit(1);
	put_bit(1);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(1);
	put_bit(1); // 31
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(1);
	put_bit(1);
	put_bit(0);
	put_bit(0);
	put_bit(0); // 00
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);
	put_bit(0);

	return 0;
}