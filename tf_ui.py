#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "127.0.0.1"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_humidity import BrickletHumidity

from time import sleep
from os.path import join, splitext
from os import listdir
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

tfIDs = [
    ['h2u',216],
    ['a54',221],
    ['1Jk',21],
]

tfConnect = True

if tfConnect:
    tfIDs = []

imgPath = 'img'

deviceIdentifiers = [
[11, "DC Brick",""],
[13, "Master Brick",""],
[14, "Servo Brick",""],
[15, "Stepper Brick",""],
[16, "IMU Brick","sensor","get_all_data"],
[17, "RED Brick",""],
[18, "IMU Brick 2.0","sensor","get_all_data"],
[19, "Silent Stepper Brick",""],
[21, "Ambient Light Bricklet","sensor","get_illuminance"],
[23, "Current12 Bricklet","sensor"],
[24, "Current25 Bricklet","sensor"],
[25, "Distance IR Bricklet","sensor"],
[26, "Dual Relay Bricklet","actuator"],
[27, "Humidity Bricklet","sensor"],
[28, "IO-16 Bricklet","sensor"],
[29, "IO-4 Bricklet","sensor"],
[210, "Joystick Bricklet","sensor"],
[211, "LCD 16x2 Bricklet","actuator"],
[212, "LCD 20x4 Bricklet","actuator"],
[213, "Linear Poti Bricklet","sensor"],
[214, "Piezo Buzzer Bricklet","actuator"],
[215, "Rotary Poti Bricklet","sensor"],
[216, "Temperature Bricklet","sensor"],
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
[238, "Sound Intensity Bricklet","sensor"],
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
[259, "Ambient Light Bricklet 2.0","","get_illuminance"],
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
    for t in deviceIdentifiers:
        if ID[1]==t[0]:
            #print(ID,t[0])
            deviceType = t[1]
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
            #print("Sensor: "+str(dir(sensor)))
            # print("Sensor type: "+str(sensor.DEVICE_IDENTIFIER))
            # print(self.buttons[i].text[0:3],sensor.DEVICE_DISPLAY_NAME,sensor.get_identity().uid)
            if self.buttons[i].text[0:3]==sensor.get_identity().uid:
                #print(dir(self.buttons[i]))
                if sensor.DEVICE_IDENTIFIER == 259:
                    self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_illuminance()/100.0)+" lux"
                if sensor.DEVICE_IDENTIFIER == 216:
                    self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_temperature()/100.0)+" ºC"
                if sensor.DEVICE_IDENTIFIER == 27:
                    self.buttons[i].text = sensor.get_identity().uid+"\n"+sensor.DEVICE_DISPLAY_NAME+"\n"+str(sensor.get_humidity()/10.0)+" %RH"

            i += 1


    def build(self):
        self.title = 'Tinkerforge Sensors'
        # self.layout = BoxLayout(padding=10)
        self.layout = GridLayout(cols=2, padding=10, spacing=10)
        self.sensors = []
        self.buttons = []

        if tfConnect:
            # Create connection and connect to brickd
            ipcon = IPConnection()
            ipcon.connect(HOST, PORT)

            # Register Enumerate Callback
            ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

            # Trigger Enumerate
            ipcon.enumerate()

            sleep(2)
            #raw_input("Press key to exit\n") # Use input() in Python 3

        print(tfIDs)
        for tf in tfIDs:
            # try:
            if True:
                # print(len(tf[0]))
                if len(tf[0])<=3:
                    print(tf[0],getIdentifier(tf))
                    #self.addButton(label=getIdentifier(tf))
                    if tf[1] == 259:
                        al = BrickletAmbientLightV2(tf[0], ipcon)
                        print(al.get_identity())
                        # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                        #al.set_illuminance_callback_period(1000)
                        self.sensors.append(al)
                        kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_illuminance()/100.0)+" lux",font_size=50)
                        self.buttons.append(kv_button)
                        self.layout.add_widget(kv_button)
                    if tf[1] == 216:
                        al = BrickletTemperature(tf[0], ipcon)
                        print(al.get_identity())
                        # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                        #al.set_illuminance_callback_period(1000)
                        self.sensors.append(al)
                        kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_temperature()/100.0)+" ºC",font_size=50)
                        self.buttons.append(kv_button)
                        self.layout.add_widget(kv_button)
                    if tf[1] == 27:
                        al = BrickletHumidity(tf[0], ipcon)
                        print(al.get_identity())
                        # al.register_callback(al.CALLBACK_ILLUMINANCE, cb_illuminance)
                        #al.set_illuminance_callback_period(1000)
                        self.sensors.append(al)
                        kv_button = Button(text=tf[0]+"\n"+getIdentifier(tf)+"\n"+str(al.get_humidity()/10.0)+" %RH",font_size=50)
                        self.buttons.append(kv_button)
                        self.layout.add_widget(kv_button)

            # except:
            #     pass
        Clock.schedule_interval(self.cb_sensors, 1.0)

        imgs = getImages(imgPath)
        # print(imgs)
        for img in imgs:
            fn = join(imgPath,img)
            im = CoreImage(fn)
            kv_button = Button(background_normal=fn)
            self.layout.add_widget(kv_button)

        return(self.layout)

    def addButton(self, label):
        kv_button = Button(text=label)
        kv_label = Label(text=label)
        self.layout.add_widget(kv_label)

if __name__ == "__main__":
    tf_UI_App().run()
    if tfConnect:
        ipcon.disconnect()
