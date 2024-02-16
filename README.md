# Bridge---Canyon-on-Hardware
Welcome to Bridge, the hardware adaptation of Canyon, a convolution reverb plugin. This project utilizes ELK Audio OS and the Raspberry Pi Compute Module 4, featuring three custom-designed boards (1 main board and 2 IO boards). We created this project as the foundation for a complete OpenSource Audio FX Pedal based on community's resources. 

## Overview
Bridge extends Canyon's convolution reverb into the physical realm, combining the power of ELK Audio OS/HifiBerry DAC+ADC and Raspberry Pi Compute Module 4 for a robust audio FX solution.

## Features
- **Convolution Reverb:** Achieve realistic and immersive reverb effects through Canyon.
- **Custom Hardware:** Three boards - 1 main and 2 IO boards - designed for modularity and reusability.
- **ELK Audio OS:** Leverage the efficiency of ELK Audio OS for real-time audio processing.

## Hardware
Bridge comprises the following custom-designed boards:

1. **Main Board:**
   - GPIO/HAT Connector
   - SPI Screen Connector for a [480*320 ILI9488 based screen]([url](https://www.amazon.fr/gp/product/B08NV6SNYH/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1))
   - Raspberry Pi Compute Module 4
   - ATMega328p with ICSP connector for IO management

2. **IO Boards (x2):**
   - Pots and Switches for massive fun
   - Rotary encoder

## Software
Bridge relies on serveral pieces of sotware to run :
1. **ATMega328p:**
  - Potentiometer values conversion
  - Screen management
  - Serial communication with CM4
2. **Compute Module 4:**
  - Running ELK Audio OS for real-time audio processing
  - IO management
  - OSC
  - Serial Communication with ATMega328p

## Contributing
We welcome and encourage contributions to enhance Bridge! If you have ideas, bug fixes, or new features, please open an issue or submit a pull request.

## License
The software contained in this project is licensed under the GPL3 license. The hardware is licensed under the Creative Commons v4.0.

Happy coding with Bridge!
