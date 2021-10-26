from hw import * # getting all the things from the hardware module so we can access them easily
import random
import network

import json, binascii, hashlib # for SSID and password generation

# showing the "cutie" image on startup
show_compressed(cutie_c)

#############
# WiFi config
#############

# disabling both network interfaces by default, reenable as needed
# and generating random SSID and password on the AP IF so that it's configured securely when you enable it

getrandomhex = lambda: binascii.hexlify(hashlib.sha1(str(random.getrandbits(10))).digest())

# if psk file exists, loading it, otherwise generating a new psk
try:
    with open("wifi.json", "r") as f:
        j = json.load(f)
    psk = j["psk"]
    print("psk loaded", psk)
except Exception as e:
    # psk loading failed for some reason - either nonexistent file or some weirdness
    print(e)
    psk = getrandomhex()[:12]
    with open("wifi.json", "w") as f:
        j = {"psk":psk}
        json.dump(j, f)
    print("psk generated and saved", psk)

# AP setup
ap = network.WLAN(network.AP_IF)

# static SSID that depends on the MAC address
ssid = "Nugget-"+binascii.hexlify(ap.config('mac')[2:]).decode("ascii").upper()

ap.active(True) # needed to set AP parameters
sleep(0.5) # sometimes needed so that AP config doesn't fail immediately
ap.config(essid=ssid, password=psk)
# check if right button is pressed
buttons.update()
if buttons.right:
    # Keeping AP active and showing SSID&PSK on the screen
    lcd.text(ssid, 3, 3)
    lcd.text(psk, 3, 64-(1+8))
    lcd.show()
    sleep(2)
else:
    # right button not pressed, disabling the AP
    ap.active(False)
print("SSID:", ssid, "PSK:", psk, "active:", ap.active())


# STA setup
sta = network.WLAN(network.STA_IF)
sta.active(False) # change to True to enable client mode
# uncomment and change this to connect to an AP
#sta.connect("yer router SSID", "password")

wifi_connect_timeout = 10
def wait_for_wifi_connection():
    counter = 0
    lcd.fill_rect(3, 3, 3+8*21, 3+8, 0)
    lcd.text("wifi connect "+str(wifi_connect_timeout-counter), 3, 3)
    lcd.show()
    while not sta.isconnected() and counter < wifi_connect_timeout:
        sleep(1)
        counter += 1
        lcd.fill_rect(3, 3, 3+8*21, 3+8, 0)
        lcd.text("wifi connect "+str(wifi_connect_timeout-counter), 3, 3)
        lcd.show()
    print("Connection failed" if not sta.isconnected() else "Connection successful")
    lcd.fill_rect(3, 3, 3+8*21, 3+8, 0)
    lcd.text("connect ok" if sta.isconnected() else "connect fail", 3, 3)
    lcd.show()
    sleep(0.5) # showing connection status on the screen for a bit longer
    return sta.isconnected()

# uncomment these three lines if you want to wait till you're connected to your router
#lcd.text("connecting to wifi", 3, 3)
#wait_for_wifi_connection()
#lcd.fill_rect(3, 3, 3+8*21, 3+8, 0)

#####################
# start of the script
#####################

np = get_neopixels(1) # only one Neopixel connected - increase the number if you have more

# waiting for "up" button
np[0] = (127, 0, 0)
np.write()
lcd.fill_rect(3, 3, 3+8*21, 3+8, 0)
lcd.text("press up", 3, 3)
lcd.show()
while not buttons.up:
    buttons.update()

# waiting for "right" button
np[0] = (127, 127, 0)
np.write()
lcd.fill_rect(3, 3, 3+8*len("press_up"), 3+8, 0) # quickly overwrite last message
# default font characters are 8 pixels tall and 8 pixels wide
# so, we need to clean a space that's 8 pixels tall and 8*len(last_text) pixels wide
lcd.text("press right", 3, 3)
lcd.show()
while not buttons.right:
    buttons.update()

# waiting for "down" button
np[0] = (0, 127, 0)
np.write()
lcd.fill_rect(3, 3, 3+8*len("press right"), 3+8, 0)
lcd.text("press down", 3, 3)
lcd.show()
while not buttons.down:
    buttons.update()

# waiting for "left" button
np[0] = (0, 0, 127)
np.write()
lcd.fill_rect(3, 3, 3+8*len("press down"), 3+8, 0)
lcd.text("press left", 3, 3)
lcd.show()
while not buttons.left:
    buttons.update()

# button pressed, clearing last message
lcd.fill_rect(3, 3, 3+8*10, 3+8, 0)
lcd.show()

# some "animations"

def schroedinger():
    buttons.update()
    while buttons.left:
        show_compressed(cutie_c)
        show_compressed(dead_c)
        buttons.update()
    # random image after button is released
    if random.getrandbits(1) == 1:
        show_compressed(cutie_c)

def caramelldansen():
    buttons.update()
    while buttons.right:
        np[0] = [random.getrandbits(6) for i in range(3)]
        np.write()
        sleep(0.27)
        lcd.flip(not lcd.flip_en, update=False)
        show_compressed(cutie_c)
        np[0] = [random.getrandbits(6) for i in range(3)]
        np.write()
        sleep(0.27)
        show_compressed(nyaa_c)
        buttons.update()
    # unflipping your LCD
    lcd.flip(True, update=False)

buttons.cb = {"left":schroedinger, "right":caramelldansen, "up":lambda: show_compressed(cutie_c), "down":lambda: show_compressed(dead_c)}

def button_test():
    # call this function from REPL to test your buttons' reaction time and debouncing
    # adjust buttons.debounce_time up or down accordingly
    # lower debounce time - quicker reaction to repeated keypresses
    # higher debounce time - bigger chance of button bounce
    buttons.cb = {"left":lambda: print("left"),
                  "right":lambda: print("right"),
                  "up":lambda: print("up"),
                  "down":lambda: print("down")}
    while True:
        buttons.update()

while True:
    # the buttons.update() processes button states, and executes button callbacks if any are set
    # so, you can manually check button states after calling update(),
    # or set callbacks and then just call ".update()" in a loop.
    buttons.update()

