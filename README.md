# Titanium-49

Capture your TI-89 Titanium's screen and send keypresses from your computer with this Raspberry Pi Pico (W)-based device.

At the moment this project is fairly bespoke and cannot transfer programs, apps, or upgrade the OS. It can *only* remotely control the calculator and capture screenshots. [As of the latest commit, this functionality is still WIP.]

It also does not make use of the RP2040's PIO system. That may be implemented in the future, if proven to be faster than the CPU wiggling pins alone.

## History

The creator of the project sometimes found a need to get screenshots of their TI-89 Titanium at school, but the Chromebook that was given to them would not run TI-Connect or TILP. Their Windows "laptop" was not at all portable, and their only portable Linux computer was unbearably slow due to its use of an HDD as an OS drive. So, the project was created. Never again would anyone have to carry around a bulky computer just for doing funky things with calculators.

It is called Titanium-49 because "TI-89 **Titanium**" and half of 8 is 4. I didn't bother to divide the 9 by 2 because that's a non-integer and Titanium-44.5 sounds weird. As you can tell, not much thought went into naming this project.

A rewrite was attempted in C in the name of increasing performance, but that endeavor was unsuccessful and the project was switched back to MicroPython. The pins would simply not wiggle correctly. However, after more optimization and taking advantage of both of the RP2040's cores, acceptable performance was achieved in MicroPython itself.

## Credits

* twisted_nematic57 (Akshat Singh): main developer

### Special Thanks

* calc84maniac for helping to clear up some confusion about the bitwise getting routine
* Timothy 'Geekboy1011' Keller for his [PIO-based project](https://github.com/geekbozu/PicoSilverLink) and some informational help
* [Cemetech](https://cemetech.net) for being the welcoming one-stop shop for calculator development
