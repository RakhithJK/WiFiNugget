# WiFiNugget

Binaries & source code for the Wi-Fi Nugget

Documentation: https://github.com/HakCat-Tech/WiFiNugget/wiki

Quickstart Setup: https://youtu.be/WAG7yCbEFtw

![Hell yeah](https://cdn.shopify.com/s/files/1/2779/8142/products/signal-2021-09-30-162945_1024x1024.jpg?v=1633047834)

## Arduino

**Pre-compiled binaries**

* `DeauthDetector.bin` - Wi-Fi deauthentication & dissociation attack detector by @AlexLynd based on @spacehuhn's deauth detector (Precompiled, flash directly with esptool)

* `Nugget_Deauther.bin` - The Wi-Fi Deauther V2.5 by @spacehuhn, modified for Nugget by @AlexLynd 

**Code**

* Wi-Fi deauthentication & disassociation attack detector by @AlexLynd based on @spacehuhn's deauth detector (See here: https://github.com/HakCat-Tech/HaxxDetector)

* Wi-Fi Deauther - Wi-Fi scanning & attack platform for the ESP8266 by @spacehuhn (See here: https://github.com/HakCat-Tech/esp8266_deauther)

## MicroPython

**Pre-compiled binaries**

* `wifinugget_upy_v2.bin` - MicroPython firmware that makes use out of WiFiNugget's basic hardware features (screen, buttons, Neopixel), includes `main.py`, `hw.py` and `sh1106.py`. Hold the right button during boot to enable AP mode!
* `wifinugget_generic_upy_v1.17.bin` - generic MicroPython firmware that was verified to work on WiFiNugget with ESP8266, build 20210902-v1.17

**Code** 

* `main.py` - Example script for using the Nugget on ESP8266 hardware. Has examples for WiFi config, screen and neopixel control and button state reading. Relies on `hw.py` for hardware functions, is the script that runs by default when you use the latest MicroPython binary
* `hw.py` - Nugget hardware definition library to make coding easier; has code for the OLED screen, buttons and the Neopixel. Also has Wemos D0-D8 pin number definitions. Is included in the firmware.
* `pack_unpack_test.py` - image compression/decompression playground&test file, for developing the compression code that makes display images consume less RAM. You don't need to store this on your Nugget.
* `upy_tests/NeopixelTest.py` - short script for testing an attached Neopixel strip
* `upy_tests/EverythingTest.py` - test of SH1106 screen, Neopixel and buttons
* `upy_tests/NeopixelTest_CircuitPython.py` - short script for testing an attached Neopixel strip (in CircuitPython, only works on S2 version of the Nugget, won't work on ESP8266)

**Libraries used**

* `sh1106.py` - [robert-hh's SH1106 library](https://github.com/robert-hh/SH1106/)

