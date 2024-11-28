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
//#include "pico/cyw43_arch.h"

#include <stdio.h>
#include <stdbool.h>

const short int WHITE = 14;
const short int RED = 15;

bool system_state[] = {0};
/* Bit 0: if set, means wireless/onboard LED capabilities are unavailable
*/


int main() {
  set_sys_clock_khz(280*1000*1000, true); /* need for speed (works on every Pico
                                             board out of the box) */
  stdio_init_all(); // UART + USB, same output on both
  // if (cyw43_arch_init()) { // Try to init CYW43439
  //   printf("ERROR: CYW43439 init failed. LED and wireless capabilities shall be"
  //          " disabled.");
  //   system_state[0] = 1; // Later on, we will not try to use this functionality.
  // }
  // if (system_state[0] == 1) { // Check: CYW43439 working?
  //   cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1); /* Enable onboard LED (power
  //                                                     indicator) */
  // }

  int i;
  for(;;) {
    i++;
    printf("%d\n",i);
  }

	return 0;
}