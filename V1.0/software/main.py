import pycom
import time
import machine
from machine import Timer
from machine import SD
import os
from network import WLAN, LTE, Bluetooth, LoRa, Sigfox 
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import math
from machine import ADC
from math import pi, e, cos, sin
import cmath, math, sys
import fft
import uos #random number generator
dir(uos)
from cmath import exp, pi
from onewire import DS18X20
from onewire import OneWire
from network import Sigfox
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
    #machine.disable_irq()
    #machine.
    #time.sleep_ms(200)
    #machine.enable_irq()


#def timer_handler(arg):
#    print ("i")
    
#t = Timer.Alarm(timer_handler, 0, 0, 1, None, True)

p_in = Pin('P8', mode=Pin.IN, pull=Pin.PULL_UP)
p_in.callback(Pin.IRQ_FALLING, pin_handler)

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

hx1 = HX711('P14', 'P10', gain=32)
hx1.set_scale(48.36)
hx1.tare()
#val1 = hx1.get_units(5)

#hx2 = HX711('P14', 'P10', gain=128)
#hx2.set_scale(48.36)
#hx2.tare()
#val2 = hx2.get_units(5)

#====================================================================================================
#FFT
#====================================================================================================

t_seconds = 0
t_seconds_wait = 0
sample_state = 0
sample_N = 1024
sample_buffer = [None] * sample_N #0-99

#https://forum.pycom.io/topic/2384/measuring-current-with-the-adc
#recommended max f_s = 6kHz

f_s = 4000
adc_res = 4096
int_fft_flag = 0

t_sec_wait = 15
t_wait = f_s * t_sec_wait

#https://forum.pycom.io/topic/170/lopy-wipy-2-esp32-specs-and-performance/8

adc_mic = ADC(0)
adc_mic.init(bits=12)

adc_mic_c = adc_mic.channel(pin='P13', attn=ADC.ATTN_11DB) 

#==================================
# Reduce ADC Res
#==================================

# adc_mic = ADC(bits=9)
# adc_mic.init()
# adc_mic_c = adc_mic.channel(pin='P13', attn=ADC.ATTN_11DB) 
# adc_res = 512


#==================================
# Reduce FFT Res for Display
#==================================
f_s = 2000
sample_N = 256
t_sec_wait = 5
sample_buffer = [None] * sample_N #0-99
t_wait = round(f_s * t_sec_wait)

def timer_handler(alarm):
    global t_seconds
    global t_seconds_wait
    global t_wait
    global sample_state
    global sample_buffer
    global sample_N
    global adc_mic
    global adc_mic_c
    global adc_res    
    global int_fft_flag

    if sample_state == 0:
        sample_buffer[t_seconds] = (adc_mic_c.value() / adc_res)
        t_seconds = t_seconds + 1
        if t_seconds == sample_N:
            print("sample period has passed")
            int_fft_flag = 1
            t_seconds = 0
            sample_state = 1
    elif sample_state == 1:
        t_seconds_wait = t_seconds_wait + 1
        if t_seconds_wait == t_wait:
            print("waiting period has passed")
            t_seconds_wait = 0
            sample_state = 0
            #alarm.cancel()
            #alarm.callback(None) # stop counting after 10 seconds

#https://rosettacode.org/wiki/Fast_Fourier_transform#Python 
#Window_size power of 2! ofc
def fft(x):
    N = len(x)
    if N <= 1: return x
    even = fft(x[0::2])
    odd =  fft(x[1::2])
    T= [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)]
 
def print_fft(x):
    global sample_N
    global f_s

    #print( ' '.join("%5.3f" % abs(f) for f in fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0])) )
    #a = [None] * 16
    #a = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    fft_buffer = [None] * sample_N #0-99
    fft_buffer = (' '.join("%5.3f" % abs(f) for f in fft(x)))
    #print(fft_buffer)
    fft_buffer = fft(x)
    for i in range(0, round(sample_N / 2)):
        freq = i * (f_s / sample_N)
        print("Freq: %6.1f Val: %5.3f" % (freq, abs(fft_buffer[i])))
    #print(abs(fft_buffer[0]))
    #print(abs(fft_buffer[round(sample_N / 2)]))
    #print(abs(fft_buffer[sample_N - 1]))

def print_sel_fft(x):
    global sample_N
    global f_s

    #print( ' '.join("%5.3f" % abs(f) for f in fft([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0])) )
    #a = [None] * 16
    #a = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    fft_buffer = [None] * sample_N #0-99
    fft_buffer = (' '.join("%5.3f" % abs(f) for f in fft(x)))
    #print(fft_buffer)
    fft_buffer = fft(x)
    for i in range(5, 15):
        freq = i * (f_s / sample_N)
        print("Freq: %6.1f Val: %5.3f" % (freq, abs(fft_buffer[i])))
    #print(abs(fft_buffer[0]))
    #print(abs(fft_buffer[round(sample_N / 2)]))
    #print(abs(fft_buffer[sample_N - 1]))


def print_440Hz_fft(x):
    global sample_N
    global f_s

    f_int = f_s / sample_N
    min_range = round(415 / f_int)
    max_range = round(475 / f_int) + 1

    fft_buffer = [None] * sample_N #0-99
    fft_buffer = (' '.join("%5.3f" % abs(f) for f in fft(x)))

    fft_buffer = fft(x)
    tft.fill(TFT.BLACK)
    
    v = 0
    fft_print = "FFT:"
    tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
    v += sysfont["Height"]
    for i in range(min_range, max_range):
        freq = i * (f_s / sample_N)
        fft_print = "Freq:%3.0f Val:%2.2f" % (freq, abs(fft_buffer[i]))
        tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
        v += sysfont["Height"]
    
def draw_440Hz_fft(x):
    global sample_N
    global f_s

    f_int = f_s / sample_N
    min_range = round(415 / f_int)
    max_range = round(475 / f_int) + 1

    fft_buffer = [None] * sample_N #0-99
    fft_buffer = (' '.join("%5.3f" % abs(f) for f in fft(x)))

    fft_buffer = fft(x)
    tft.fill(TFT.BLACK)
    
    v = 0
    fft_print = "FFT:"
    tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
    v += sysfont["Height"]
    color = TFT.RED
    for i in range(min_range, max_range):
        freq = i * (f_s / sample_N)
        fft_print = "Freq:%4.0f" % (freq)
        tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
        if round(abs(fft_buffer[i])) <= 0.5:
            color = TFT.GREEN
        elif round(abs(fft_buffer[i])) <= 1:
            color = TFT.YELLOW
        else: 
            color = TFT.RED
        tft.fillrect((60, v), ((round(abs(fft_buffer[i]*50))), sysfont["Height"]), color)
        v += sysfont["Height"]

def print_440Hz_fft_text(min_f, max_f, skip):
    global sample_N
    global f_s

    f_int = f_s / sample_N
    min_range = round(min_f / f_int)
    max_range = round(max_f / f_int) + 1

    tft.fill(TFT.BLACK)

    v = 0
    fft_print = "FFT:"
    tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
    v += sysfont["Height"]
    color = TFT.RED
    for i in range(min_range, max_range, skip):
        freq = i * (f_s / sample_N)
        fft_print = "Freq:%4.0f" % (freq)
        tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
        v += sysfont["Height"]
    

#can draw 20 FFT lines    
def draw_440Hz_fft_fast(x, min_f, max_f, skip):
    global sample_N
    global f_s

    f_int = f_s / sample_N
    min_range = round(min_f / f_int)
    max_range = round(max_f / f_int) + 1

    fft_buffer = [None] * sample_N #0-99
    fft_buffer = (' '.join("%5.3f" % abs(f) for f in fft(x)))

    fft_buffer = fft(x)
    tft.fillrect((60, 0), (tft.size()[0], tft.size()[1]-(sysfont["Height"] * 2)), TFT.BLACK)
    v = sysfont["Height"]
    for i in range(min_range, max_range, skip):
        if round(abs(fft_buffer[i])) <= 0.5:
            color = TFT.GREEN
        elif round(abs(fft_buffer[i])) <= 1:
            color = TFT.YELLOW
        else: 
            color = TFT.RED
        tft.fillrect((60, v), ((round(abs(fft_buffer[i]*50))), sysfont["Height"]), color)
        v += sysfont["Height"]
    
######################################
# Start Timer to do FFT
######################################

def init_Timer():
    global f_s
    alarm_adc = Timer.Alarm(timer_handler, 1 / f_s, periodic=True)

init_Timer()

#SPI using standard pins for DISPLAY after using SPI for HX711
spi = SPI(SPI.MASTER, baudrate=40000000, polarity=0, phase=0)

print_440Hz_fft_text(0, 900, 8)

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
    
    if int_fft_flag == 1:
        #print_440Hz_fft(sample_buffer)
        #draw_440Hz_fft(sample_buffer)
        #SPI using standard pins for DISPLAY after using SPI for HX711
        spi = SPI(SPI.MASTER, baudrate=40000000, polarity=0, phase=0)
        draw_440Hz_fft_fast(sample_buffer, 0, 900, 8)
        int_fft_flag = 0
        
        #===========
        #FOR DEEPSLEEP
        #rep = rep - 1

        hx1 = HX711('P14', 'P10', gain=32)
        val1 = hx1.get_units(5)
        print("w1: ")
        print(val1)
        time.sleep_ms(200)

        #SPI using standard pins for DISPLAY after using SPI for HX711
        spi = SPI(SPI.MASTER, baudrate=40000000, polarity=0, phase=0)
        tft.fillrect((0, (tft.size()[1] - (sysfont["Height"] * 2))), (tft.size()[0], tft.size()[1]), TFT.BLACK)

        v = tft.size()[1] - (sysfont["Height"] * 2)
        fft_print = "Weight: %4.1f" % (val1)
        tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)
        v += sysfont["Height"]

        temp.start_conversion()
        time.sleep(1)
        print("Temp: ")
        print(temp.read_temp_async())

        fft_print = "Temp: %4.1f" % (temp.read_temp_async())
        tft.text((0, v), fft_print, TFT.WHITE, sysfont, 1)

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