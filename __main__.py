from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from time import sleep
import threading

from Mqtt_Driver import Mqtt_Driver

from AirQuality import airQuality_
from Tempature import tempature_
from Humidity import humidity_


Window.size = (378, 672)

class MainBoxLayout(BoxLayout):

    mqtt_driver = Mqtt_Driver()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mqtt_driver.client.subscribe("raspberry/#", qos=0)
        
        self.mqtt_driver.client.message_callback_add("raspberry/airQuality", self.update_airQuality)
        self.mqtt_driver.client.message_callback_add('raspberry/tempature', self.update_tempature)
        self.mqtt_driver.client.message_callback_add('raspberry/humidity', self.update_humidity)

        self.mqtt_thrd = threading.Thread(target=self.mqtt_driver.client.loop_forever)

        self.mqtt_thrd.start()
    
 

    def update_airQuality(self, client, userdata, msg):
       
        airQuality_[0] = int(msg.payload)

    def update_tempature(self, client, userdata, msg):
        tempature_[0] = int(msg.payload)

    def update_humidity(self, client,userdata, msg):
        humidity_[0] = int(msg.payload)


    def on_press_btn_cradle(self):
        self.mqtt_driver.client.publish("mobil/btn_cradle", qos=0)

    def on_press_btn_stop(self):
        self.mqtt_driver.client.publish("mobil/btn_stop", qos=0)
            


class mainApp(App):
    pass


mainApp().run()