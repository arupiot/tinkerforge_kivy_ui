#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "127.0.0.1"
PORT = 4223

debug = False
verbose = True
send_to_influx = True
columns_number = 1
reading_interval = 1.0

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_humidity import BrickletHumidity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity

from time import sleep
from os.path import join, splitext
from os import listdir
import math, time, datetime

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

from config import *
from influxdb import InfluxDBClient

tfIDs = [
    # ['h2u',216],
    # ['a54',221],
    # ['1Jk',21],
]

tfConnect = True

if tfConnect:
    tfIDs = []

imgPath = 'img'

deviceIdentifiersDict = {
    216: {
        "name": "Temperature",
        "type": "Temperature Bricklet",
        "class": BrickletTemperature,
        "unit": " ºC",
        "brick_tag": "Temperature_Sensor",
        "value_func": "get_temperature",
        "correction": "0.01*%s",
        "callback_func": "CALLBACK_TEMPERATURE",
        "variance": 1,
    },
    238: {
        "name": "Sound Intensity",
        "type": "Sound Intensity Bricklet",
        "class": BrickletSoundIntensity,
        "quantity": "sound_level",
        "unit": "dB",
        "brick_tag": "Noise_Sensor",
        "value_func": "get_intensity",
        "callback_func": "CALLBACK_INTENSITY",
        "correction": "20*math.log10(%s/1)",
        "publish_limit": 30,
        "variance": 400,
    },
    259: {
        "name": "Ambient Light",
        "type": "Ambient Light Bricklet 2.0",
        "class": BrickletAmbientLightV2,
        "quantity": "illuminance",
        "unit": "lux",
        "brick_tag": "LightingSystem_Illuminance_Sensor",
        "value_func": "get_illuminance",
        "correction": "0.01*%s",
        "callback_func": "CALLBACK_ILLUMINANCE",
    },
}

deviceIdentifiersList = [
[11, "DC Brick",""],
[13, "Master Brick",""],
[14, "Servo Brick",""],
[15, "Stepper Brick",""],
[16, "IMU Brick","sensor",["get_all_data"],[""]],
[17, "RED Brick",""],
[18, "IMU Brick 2.0","sensor",["get_all_data"],[""]],
[19, "Silent Stepper Brick",""],
[21, "Ambient Light Bricklet","sensor",["get_illuminance"],["lux"]],
[23, "Current12 Bricklet","sensor"],
[24, "Current25 Bricklet","sensor"],
[25, "Distance IR Bricklet","sensor"],
[26, "Dual Relay Bricklet","actuator"],
[27, "Humidity Bricklet","sensor",["get_humidity"],["%RH"]],
[28, "IO-16 Bricklet","sensor"],
[29, "IO-4 Bricklet","sensor"],
[210, "Joystick Bricklet","sensor"],
[211, "LCD 16x2 Bricklet","actuator"],
[212, "LCD 20x4 Bricklet","actuator"],
[213, "Linear Poti Bricklet","sensor"],
[214, "Piezo Buzzer Bricklet","actuator"],
[215, "Rotary Poti Bricklet","sensor"],
[216, "Temperature Bricklet","sensor",["get_temperature"],["ºC"]],
[217, "Temperature IR Bricklet","sensor"],
[218, "Voltage Bricklet","sensor"],
[219, "Analog In Bricklet","sensor"],
[220, "Analog Out Bricklet","actuator"],
[221, "Barometer Bricklet","sensor"],
[222, "GPS Bricklet","sensor"],
[223, "Industrial Digital In 4 Bricklet","sensor"],
[224, "Industrial Digital Out 4 Bricklet","actuator"],
[225, "Industrial Quad Relay Bricklet","actuator"],
[226, "PTC Bricklet","sensor"],
[227, "Voltage/Current Bricklet","sensor"],
[228, "Industrial Dual 0-20mA Bricklet",""],
[229, "Distance US Bricklet","sensor"],
[230, "Dual Button Bricklet","sensor"],
[231, "LED Strip Bricklet","actuator"],
[232, "Moisture Bricklet","sensor"],
[233, "Motion Detector Bricklet","sensor"],
[234, "Multi Touch Bricklet","sensor"],
[235, "Remote Switch Bricklet","sensor"],
[236, "Rotary Encoder Bricklet","sensor"],
[237, "Segment Display 4x7 Bricklet","actuator"],
[238, "Sound Intensity Bricklet","sensor", ["get_intensity"],["dB"]],
[239, "Tilt Bricklet","sensor"],
[240, "Hall Effect Bricklet","sensor"],
[241, "Line Bricklet","sensor"],
[242, "Piezo Speaker Bricklet","actuator"],
[243, "Color Bricklet","sensor"],
[244, "Solid State Relay Bricklet","actuator"],
[245, "Heart Rate Bricklet","sensor"],
[246, "NFC/RFID Bricklet","sensor"],
[249, "Industrial Dual Analog In Bricklet","sensor"],
[250, "Accelerometer Bricklet","sensor"],
[251, "Analog In Bricklet 2.0","sensor"],
[252, "Gas Detector Bricklet","sensor"],
[253, "Load Cell Bricklet","sensor"],
[254, "RS232 Bricklet",""],
[255, "Laser Range Finder Bricklet","sensor"],
[256, "Analog Out Bricklet 2.0","actuator"],
[257, "AC Current Bricklet",""],
[258, "Industrial Analog Out Bricklet",""],
[259, "Ambient Light Bricklet 2.0","",["get_illuminance"],["lux"]],
[260, "Dust Detector Bricklet","sensor"],
[261, "Ozone Bricklet","sensor"],
[262, "CO2 Bricklet","sensor"],
[263, "OLED 128x64 Bricklet","actuator"],
[264, "OLED 64x48 Bricklet","actuator"],
[265, "UV Light Bricklet","sensor"],
[266, "Thermocouple Bricklet","sensor"],
[267, "Motorized Linear Poti Bricklet","sensor"],
[268, "Real-Time Clock Bricklet",""],
[269, "Pressure Bricklet","sensor"],
[270, "CAN Bricklet",""],
[271, "RGB LED Bricklet","actuator"],
[272, "RGB LED Matrix Bricklet","actuator"],
[276, "GPS Bricklet 2.0","sensor"],
[277, "RS485 Bricklet",""],
[278, "Thermal Imaging Bricklet",""],
[282, "RGB LED Button Bricklet","sensor"],
[283, "Humidity Bricklet 2.0","sensor"],
[284, "Dual Relay Bricklet 2.0","actuator"],
[285, "DMX Bricklet","actuator"],
[286, "NFC Bricklet","sensor"],
[287, "Moisture Bricklet 2.0","sensor"],
[288, "Outdoor Weather Bricklet","sensor"],
[289, "Remote Switch Bricklet 2.0","actuator"],
[291, "Temperature IR Bricklet 2.0","sensor"],
[292, "Motion Detector Bricklet 2.0","sensor"],
[294, "Rotary Encoder Bricklet 2.0","sensor"],
[295, "Analog In Bricklet 3.0","sensor"],
[296, "Solid State Relay Bricklet 2.0","actuator"],
[21111, "Stream Test Bricklet",""],
]

deviceIDs = [i[0] for i in deviceIdentifiersList]
deviceIDs = [item for item in deviceIdentifiersDict]
if debug:
    print(deviceIDs)
    for dID in deviceIDs:
        print(deviceIdentifiersDict[dID])

def getImages(path):
    files = listdir(path)
    imgs = []
    for f in files:
        #print(f, splitext(f)[1])
        # print(splitext(f)[1].lower())
        if splitext(f)[1].lower() in ['.jpg', '.png']:
            # print(f)
            imgs.append(f)
    return(imgs)

def getIdentifier(ID):
    deviceType = ""
    # for t in deviceIdentifiers:
        # if ID[1]==t[0]:
        #     #print(ID,t[0])
        #     deviceType = t[1]
    for t in deviceIDs:
        if ID[1]==t:
            #print(ID,t[0])
            deviceType = deviceIdentifiersDict[t]["type"]
    return(deviceType)

# Tinkerforge sensors enumeration
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    tfIDs.append([uid, device_identifier])

# class sensorView(BoxLayout):
#
#     def __init__(self, **kwargs):
#         super(sensorView, self).__init__(**kwargs)
#         # self.cols = 2
#         # self.add_widget(Label(text='User Name'))
#         # self.username = TextInput(multiline=False)
#         # self.add_widget(self.username)
#         # self.add_widget(Label(text='password'))
#         # self.password = TextInput(password=True, multiline=False)
#         # self.add_widget(self.password)

class tf_UI_App(App):

    # def cb_illuminance(illuminance):
    #     print("Illuminance: " + str(illuminance/100.0) + " Lux")

    def cb_sensors(self, dt):
        # print("Illuminance: "+str(al.get_illuminance()/100))
        i = 0
        for sensor in self.sensors:
            if debug:
                # print("Sensor: "+str(dir(sensor)))
                print("Sensor type: "+str(sensor.DEVICE_IDENTIFIER))
                print(self.buttons[i].text[0:3],sensor.DEVICE_DISPLAY_NAME,sensor.get_identity().uid)
            if self.buttons[i].text[0:3]==sensor.get_identity().uid:
                quantity = getattr(sensor, deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER]["value_func"])()+1
                v = eval(deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER]["correction"] % quantity)
                unit = deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER]["unit"]
                if debug:
                    # print(quantity, deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER]["correction"] % quantity)
                    print(self.buttons[i].text[0:3], sensor.DEVICE_IDENTIFIER, sensor.DEVICE_DISPLAY_NAME, deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER], v, unit)
                if verbose:
                    print(self.buttons[i].text[0:3], sensor.DEVICE_IDENTIFIER, sensor.DEVICE_DISPLAY_NAME, v, unit)
                self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(v)+" "+unit
                #print(dir(self.buttons[i]))
                # if sensor.DEVICE_IDENTIFIER == 259:
                #     self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_illuminance()/100.0)+" lux"
                # if sensor.DEVICE_IDENTIFIER == 216:
                #     self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_temperature()/100.0)+" ºC"
                # if sensor.DEVICE_IDENTIFIER == 27:
                #     self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_humidity()/10.0)+" %RH"

                # Get timestamp
                ts = time.time()
                #print(time.time(), prev_time)
                datestr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                # Send value to InfluxDB at instantaneous interval
                if send_to_influx:
                    SENSORNAME = SHORT_IDENT+"_"+self.buttons[i].text[0:3]+"_"+deviceIdentifiersDict[sensor.DEVICE_IDENTIFIER]["brick_tag"]
                    json_body = [
                        {
                        "measurement": SENSORNAME,
                        "tags": {
                            "sensor": SENSORNAME,
                        },
                        "time": datestr,
                        "fields": {
                            "value": v,
                            }
                        }
                    ]
                    if verbose:
                        print(json_body)
                    self.influx_client.write_points(json_body)
            i += 1

    def build(self):
        self.title = 'Tinkerforge Sensors'
        # self.layout = BoxLayout(padding=10)
        self.layout = GridLayout(cols=columns_number, padding=10, spacing=10)
        self.sensors = []
        self.buttons = []
        self.ipcon = None
        self.influx_client = None

        if tfConnect:
            # Create connection and connect to brickd
            self.ipcon = IPConnection()
            self.ipcon.connect(HOST, PORT)

            # Register Enumerate Callback
            self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

            # Trigger Enumerate
            self.ipcon.enumerate()

            sleep(2)
            #raw_input("Press key to exit\n") # Use input() in Python 3

        if debug:
            print(tfIDs)

        # Connect to InfluxDB server
        if send_to_influx:
            print("Connecting to InfluxDB server %s" % INFLUX_AUTH["host"])
            # self.influx_client = InfluxDBClient(INFLUXserver, INFLUXport, INFLUXdbuser, INFLUXdbuser_password, INFLUXdbname)
            try:
                self.influx_client = InfluxDBClient(
                    host=INFLUX_AUTH["host"],
                    port=INFLUX_AUTH["port"],
                    username=INFLUX_AUTH["user"],
                    password=INFLUX_AUTH["pass"],
                    database=INFLUX_AUTH["db"],
                    ssl=INFLUX_AUTH["ssl"],
                    timeout=1,
                    retries=5,)
            except Exception as e:
                print("Error connecting to InfluxDB:")
                print(e)

        for tf in tfIDs:
            # try:
            if True:
                # print(len(tf[0]))
                if len(tf[0])<=3: # if the device UID is 3 characters it is a bricklet
                    #self.addButton(label=getIdentifier(tf))
                    if tf[1] in deviceIDs:
                        bricklet = deviceIdentifiersDict[tf[1]]["class"](tf[0],self.ipcon)
                        self.sensors.append(bricklet)
                        quantity = getattr(bricklet, deviceIdentifiersDict[tf[1]]["value_func"])()+1
                        v = eval(deviceIdentifiersDict[tf[1]]["correction"] % quantity)
                        unit = deviceIdentifiersDict[tf[1]]["unit"]
                        if debug:
                            print(quantity, deviceIdentifiersDict[tf[1]]["correction"] % quantity)
                            print(tf[0],getIdentifier(tf), deviceIdentifiersDict[tf[1]], v, unit)
                        kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(v)+" "+unit,font_size=50)
                        self.buttons.append(kv_button)
                        self.layout.add_widget(kv_button)
                    # if tf[1] == 259:
                    #     al = BrickletAmbientLightV2(tf[0], ipcon)
                    #     print(al.get_identity())
                    #     # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                    #     #al.set_illuminance_callback_period(1000)
                    #     self.sensors.append(al)
                    #     kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_illuminance()/100.0)+" lux",font_size=50)
                    #     self.buttons.append(kv_button)
                    #     self.layout.add_widget(kv_button)
                    # if tf[1] == 216:
                    #     al = BrickletTemperature(tf[0], ipcon)
                    #     print(al.get_identity())
                    #     # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                    #     #al.set_illuminance_callback_period(1000)
                    #     self.sensors.append(al)
                    #     kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_temperature()/100.0)+" ºC",font_size=50)
                    #     self.buttons.append(kv_button)
                    #     self.layout.add_widget(kv_button)
                    # if tf[1] == 27:
                    #     al = BrickletHumidity(tf[0], ipcon)
                    #     print(al.get_identity())
                    #     # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                    #     #al.set_illuminance_callback_period(1000)
                    #     self.sensors.append(al)
                    #     kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_humidity()/10.0)+" %RH",font_size=50)
                    #     self.buttons.append(kv_button)
                    #     self.layout.add_widget(kv_button)

            # except:
            #     pass
        Clock.schedule_interval(self.cb_sensors, reading_interval)

        imgs = getImages(imgPath)
        # print(imgs)
        for img in imgs:
            fn = join(imgPath,img)
            im = CoreImage(fn)
            # print(dir(im))]
            # print(im.size)
            kv_button = Button(background_normal=fn)
            # print(dir(kv_button))
            kv_button.texture_size = [100,100]#im.size
            # print(kv_button.texture_size)
            self.layout.add_widget(kv_button)

        return(self.layout)

    # def addButton(self, label):
    #     kv_button = Button(text=label)
    #     kv_label = Label(text=label)
    #     self.layout.add_widget(kv_label)

if __name__ == "__main__":
    tfApp = tf_UI_App()
    tfApp.run()
    if tfConnect:
        tfApp.ipcon.disconnect()
