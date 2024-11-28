cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

set(CMAKE_C_COMPILER "arm-none-eabi-gcc")
set(CMAKE_CXX_COMPILER "arm-none-eabi-g++")
set(CMAKE_ASM_COMPILER "arm-none-eabi-gcc")

project(t49_fw C CXX ASM) # C++ not used
set(PICO_PLATFORM rp2040)
set(PICO_BOARD pico_w)
set(PICO_NO_FLASH 0) # Run from flash, not SRAM

set(CMAKE_C_STANDARD 23)
set(CMAKE_CXX_STANDARD 17)

if(CMAKE_BUILD_TYPE STREQUAL "Debug") # Debug flags
  set(CMAKE_C_FLAGS " \
    ${CMAKE_C_FLAGS} \
    -save-temps \
    -time \
    -Og \
    -ggdb3 \
  ")
  message(STATUS "Debug build: Adding debug flags (-save-temps -time -Og "
                 "-ggdb3)")
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Release") # Release flags
  set(CMAKE_C_FLAGS " \
    ${CMAKE_C_FLAGS} \
    -time \
    -save-temps \
    -Oz \
    -fconserve-stack \
    -fpeephole \
    -fpeephole2 \
    -mtune=cortex-m0plus \
    -march=armv6-m \
  ")
  message(STATUS "Release build: Adding release optimization flags (-time "
                 "-save-temps -Oz -fconserve-stack -fpeephole -fpeephole2 "
                 "-march=armv6-m -mtune=cortex-m0plus)")
endif()

pico_sdk_init()

include_directories(
  ${CMAKE_SOURCE_DIR}
  ${CMAKE_CURRENT_LIST_DIR}
)

add_executable(t49_fw
  main.c
)

pico_set_program_name(t49_fw "t49_fw")
pico_set_program_version(t49_fw "0.1")

pico_enable_stdio_uart(t49_fw 1) # Default serial output configuration
pico_enable_stdio_usb(t49_fw 1) # The product is meant to be used over USB, but
                                # plain UART at 8n1/115200b is also possible

pico_add_extra_outputs(t49_fw)

target_link_libraries(t49_fw
  pico_stdlib
  pico_unique_id
  hardware_gpio
  hardware_uart
  hardware_clocks
 # tinyusb_device
 # tinyusb_board
 # pico_cyw43_arch_lwip_threadsafe_background
 # pico_lwip
  pico_cyw43_arch_none
)
