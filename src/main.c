/*** main.c *******************************************************************\
 * Contributors: twisted_nematic57                                            *
 * Copyright: GNU GPLv3 (see LICENSE)                                         *
 * Description: Initializes hardware and sets up external interfaces;         *
 *              contains main loop of the firmware                            *
\******************************************************************************/

#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hardware/gpio.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"
#include "pico/cyw43_arch.h"

#include <stdio.h>
#include <stdbool.h>

#define UART_ID uart0
#define BAUD_RATE 115200
#define DATA_BITS 8
#define STOP_BITS 1
#define PARITY UART_PARITY_NONE
#define UART_TX_PIN 0
#define UART_RX_PIN 1

const short int WHITE = 14;
const short int RED = 15;


int main() {
  set_sys_clock_khz(280*1000*1000, true); /* need for speed (works on every Pico
                                             board out of the box) */
  stdio_init_all(); // UART + USB, same output on both

	
}