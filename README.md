# EasyHive_Pycom_Shield
a Shield for pycom-modules with Weight, Temperature, audio and I2C sensor-connections and a powerpath manager ic

# Hardware Update to V1.1 ( from Jan 2020)
* Transistor-footprint is corrected now
* PIN 13/14 is not in use - this should prevent Pycom-Boards from blowing up if you insert them in the [wrong orientation](https://docs.pycom.io/datasheets/development/lopy/)
* board format is smaller now so it fits into [on of these boxes (2002-IP)](https://asset.re-in.de/add/160267/c1/-/en/001279792DS01/DA_Axxatronic-BIM2002-IP-BLK-Universal-Gehaeuse-100-x-50-x-25-ABS-Schwarz-1St..pdf)
* battery voltage input is now controlled via Transistor for lower energy-consumption

# additional information for Hardware
* the new design was not built and verified yet - the easyhive project is focussing to the Easyhive-M0 board 
* you can replace R5 with an 103AT Thermistor to prevent load into the battery at -0°C temperatures
* BOM for V1.1 is still not written. so you have to check things yourself and use the BOM from Version 1.0 and the schematic.

# Software
* Software is not updated yet to the new Hardware Design File. You're welcome to change that!

# copyright
Software: GPL 3.0 and following versions

Hardware: CERN OHL 1.2 and following versions


This files are distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
