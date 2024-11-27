/*** main.c *******************************************************************\
 * Contributors: Akshat Singh                                                 *
 * Copyright: MIT License (see LICENSE)                                       *
 * Description: Initializes hardware and sets things up for the GUI and web   *
 *              interface                                                     *
\******************************************************************************/

#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hardware/gpio.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"

#include <stdio.h>
#include <stdbool.h>


int main() {
  set_sys_clock_khz(250*1000, true);
  stdio_init_all();

	int i = 0;
	while(true) {
	  printf("%d\n",i);
    i++;
  }
}