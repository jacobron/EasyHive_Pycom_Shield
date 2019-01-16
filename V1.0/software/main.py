import pycom
import time
import machine
from machine import Timer
from machine import SD
import os
from network import WLAN, LTE, Bluetooth #, LoRa, Sigfox
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import math
from machine import ADC
from math import pi, e, cos, sin
import cmath, math, sys
import uos #random number generator
dir(uos)
from cmath import exp, pi
from onewire import DS18X20
from onewire import OneWire
#
import socket
from hx711 import HX711

#======================================
# Garbage Collector
#======================================

import gc
gc.collect()
gc.mem_free()

pycom.heartbeat(False)
pycom.rgbled(0xff00)           # turn on the RGB LED in green colour
rep = 3

print("Startup Time")

os.uname()

#SPI using standard pins
spi = SPI(SPI.MASTER, baudrate=40000000, polarity=0, phase=0)
#arg1 = DC, arg2 = RES, arg3=CS
tft=TFT(spi,'P4','P1','P3')
#tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

v = 0
fft_print = "Startup"
tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
time.sleep_ms(5000)
tft.fill(TFT.BLACK)

print("Go")

#====================================================================================================
# Setup
#====================================================================================================

bluetooth = Bluetooth()
bluetooth.deinit()

#lte = LTE()
#LTE.deinit()

#SigFox & LoRa turned off automatically

#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
#LoRa.deinit()

#wlan = WLAN(mode=WLAN.STA)
#wlan.deinit()

#====================================================================================================
# Flash
#====================================================================================================

# print("Writing To Flash")
# f = open('/flash/saveddata.bin', 'w') # open for writing
# f.write(bytes([1,2,3,4,5,6,7,8]))
# f.close()

# print("Reading From Flash")
# f = open('/flash/saveddata.bin', 'r') # open for reading
# print(f.read())
# f.close()

#====================================================================================================
#Interrupt
#====================================================================================================

def pin_handler(arg):
    print("got an interrupt in pin %s" % (arg.id()))
    print("tareing...")
    hx1.tare()
    print("tared!")
    #machine.disable_irq()
    #machine.
    #time.sleep_ms(200)
    #machine.enable_irq()


#def timer_handler(arg):
#    print ("i")

#t = Timer.Alarm(timer_handler, 0, 0, 1, None, True)

p_in = Pin('P8', mode=Pin.IN, pull=Pin.PULL_UP)
p_in.callback(Pin.IRQ_FALLING, pin_handler)
p2_in = Pin('P11', mode=Pin.IN, pull=Pin.PULL_UP)
p2_in.callback(Pin.IRQ_FALLING, pin_handler)

#Antenna first!!!!!!!!
#sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
#s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
#s.setblocking(True)
#s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)​
#s.send(bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))

#====================================================================================================
#HX711 & Temp
#====================================================================================================

#DS18B20 data line connected to pin P9
ow = OneWire(Pin('P9'))
temp = DS18X20(ow)

hx1 = HX711('P14', 'P10', gain=128)
hx1.set_scale(48.36)
hx1.tare()
#val1 = hx1.get_units(5)




rep = 1

#====================================================================================================
#Mainloop
#====================================================================================================

while rep:
    #pycom.rgbled(0x000000)  # OFF
    #time.sleep_ms(500)
    #pycom.rgbled(0xFF0000)  # Red
    #time.sleep_ms(500)
    #tft.fill(TFT.BLACK)



        #===========
        #FOR DEEPSLEEP
        #rep = rep - 1

        hx1.set_gain(32)
        val1 = hx1.get_units(5)
        print("w1: ")
        print(val1)
        time.sleep_ms(200)

        hx1.set_gain(128)
        val2 = hx1.get_units(5)
        print("w2: ")
        print(val2)
        time.sleep_ms(200)


        temp.start_conversion()
        time.sleep(1)
        print("Temp: ")
        print(temp.read_temp_async())

    # hx1.set_gain(32)

    # val1 = hx1.get_units(5)
    # print("w1: ")
    # print(val1)
    # time.sleep_ms(200)

    # hx1.set_gain(128)

    # val2 = hx1.get_units(5)
    # print("w2: ")
    # print(val2)
    # time.sleep_ms(200)

    # temp.start_conversion()
    # time.sleep(1)
    # print("Temp: ")
    # print(temp.read_temp_async())

    # pycom.rgbled(0x000000)  # OFF
    # time.sleep_ms(500)

    # adc = ADC(0)
    #adc.init(bits=12)
    # adc_c = adc.channel(pin='P13', attn=ADC.ATTN_11DB)
    # print("ADC")
    # print(adc_c.value())

    #adc = ADC(0)
    #adc.init(bits=12)
    #adc_c = adc.channel(pin='P13', attn=ADC.ATTN_11DB)
    #rep-=1
    #for val in range(100):
    #    print(adc_c.value())

    #for i in res:
    #    print i.real

    #print("ADC")
    #print(adc_c.value())

#====================================================================================================
#Deepsleep
#====================================================================================================


time.sleep_ms(500)
pycom.rgbled(0x000000)  # OFF
time.sleep_ms(2000)
pycom.rgbled(0xFF0000)  # Red
time.sleep_ms(2000)

time.sleep_ms(5000)

tft.fill(TFT.BLACK)
print("Sleep: ")
v = 0
fft_print = "Enter Sleep"
tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
time.sleep_ms(1000)

#======================================
# Garbage Collector
#======================================

gc.collect()
gc.mem_free()

#sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
#sigfox.deinit()

#bt = Bluetooth()
#bt.deinit()

w = WLAN()
w.deinit()

lte = LTE()
lte.deinit()

time_ms = 60000
machine.deepsleep(time_ms)
