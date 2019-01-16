import pycom
import time
from machine import Pin
​from machine import SPI
# from onewire import DS18X20
# from onewire import OneWire
pycom.heartbeat(False)
# DS18B20 data line connected to pin P10
# ow = OneWire(Pin('P10'))
# temp = DS18X20(ow)
# configure the SPI master @ 2MHz
# this uses the SPI default pins for CLK, MOSI and MISO (``P10``, ``P11`` and ``P14``)
spi = SPI(0, mode=SPI.MASTER, baudrate=9600, polarity=0, phase=0)
#spi.write(bytes([0x00, 0x00, 0x00])) # send 5 bytes on the bus
#spi.read(3) # receive 5 bytes on the bus
#rbuf = bytearray(5)
#spi.write_readinto(bytes([0x01, 0x02, 0x03, 0x04, 0x05]), rbuf) # send a receive 5 bytes
while True:
    pycom.rgbled(0x000000)  # OFF
    time.sleep(1)
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    # pycom.rgbled(0x00FF00)  # Green
    # time.sleep(1)
    # pycom.rgbled(0x0000FF)  # Blue
    # time.sleep(1)
    # pycom.rgbled(0x00FFFF)  # Light Blue
    # time.sleep(1)
    # pycom.rgbled(0xFFFF00)  # Orange Blue
    # time.sleep(1)
    # pycom.rgbled(0xFFFFFF)  # White
    # time.sleep(1)
    print("Hallo")
    # print(temp.read_temp_async())
    # time.sleep(1)
    # temp.start_conversion()
    # time.sleep(1)
    print("Sens")
    print(spi.read(3))
​

