/*** main.c *******************************************************************\
 * Contributors: twisted_nematic57                                            *
 * Copyright: GNU GPLv3 (see LICENSE)                                         *
 * Description: Initializes hardware and set up external interfaces; then,    *
 *              runs the main loop                                            *
\******************************************************************************/

#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hardware/gpio.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"
#include "pico/time.h"
#include "pico/cyw43_arch.h"

#include <stdio.h>
#include <stdbool.h>


bool system_state[] = {0};
/* Bit 0: if set, means wireless/onboard LED capabilities are unavailable
*/


int main() {
  set_sys_clock_khz(250*1000, true);
  stdio_init_all();

  sleep_ms(8000);

  if (cyw43_arch_init()) { // Try to init CYW43439
    printf("ERROR: CYW43439 init failed. LED and wireless capabilities shall be"
           " disabled.");
    system_state[0] = 1; // Later on, we will not try to use this functionality.
  } else {
    printf("INIT: CYW43439 initialized.");
  }
  if (system_state[0] == 0) { // Check: CYW43439 working?
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1); /* Enable onboard LED (power
                                                      indicator) */
  }

	int i = 0;
	while(true) {
	  printf("%d\n",i);
    i++;
  }
}