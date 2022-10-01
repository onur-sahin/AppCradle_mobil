from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from time import sleep
import threading

from Mqtt_Driver import Mqtt_Driver

from AirQuality import airQuality_
from Tempature import tempature_
from Humidity import humidity_

from time import sleep
Window.size = (378, 672)




class MainBoxLayout(BoxLayout):

    mqtt_driver = Mqtt_Driver()

    current_speed  = NumericProperty(25.0)
    last_sent_speed = -10.0

    current_volume = NumericProperty(25.0)
    last_sent_volume = -10.0

    btn_auto_start_state = 'normal'
    btn_auto_play_state  = 'normal'
    btn_auto_stap_state  = 'normal'

    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.mqtt_driver.client.subscribe("raspberry/#", qos=0)
        
        self.mqtt_driver.client.message_callback_add("raspberry/airQuality", self.update_airQuality)
        self.mqtt_driver.client.message_callback_add('raspberry/tempature', self.update_tempature)
        self.mqtt_driver.client.message_callback_add('raspberry/humidity', self.update_humidity)

        self.mqtt_driver.client.message_callback_add('raspberry/slider_speed', self.on_touch_move_sldr_speed)
        self.mqtt_driver.client.message_callback_add('raspberry/slider_volume', self.on_touch_move_sldr_volume)

        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_play_state', self.update_btn_auto_play)
        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_start_state', self.update_btn_auto_start)
        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_stop_state', self.update_btn_auto_stop)

        # self.mqtt_driver.client.message_callback_add('raspberry/warning_popup', self.show)

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

    def on_press_btn_play(self):
    
        self.mqtt_driver.client.publish("mobil/btn_play", qos=0)

    def on_press_btn_stop_music(self):

        self.mqtt_driver.client.publish("mobil/btn_stop_music", qos=0)
        
    def on_press_btn_replay(self):

        self.mqtt_driver.client.publish("mobil/btn_replay", qos=0)
    
    def on_press_btn_next(self):
        self.mqtt_driver.client.publish("mobil/btn_next", qos=0)
       
    def on_press_btn_back(self):
        self.mqtt_driver.client.publish("mobil/btn_back", qos=0)

    def on_press_btn_auto_play(self):
        if self.btn_auto_play_state == 'down':
            self.mqtt_driver.client.publish("mobil/btn_auto_play", payload="down", qos=0)
        elif self.btn_auto_play_state == "normal":
            self.mqtt_driver.client.publish("mobil/btn_auto_play", payload="normal", qos=0)

    def update_btn_auto_play(self, *args):
    
        if args[2].payload.decode() == 'down':
            self.btn_auto_play_state ='down'
            self.ids.btn_auto_play.state = 'down'
            

        elif args[2].payload.decode() == 'normal':
            self.btn_auto_play_state = 'normal'
            self.ids.btn_auto_play.state = 'normal'

    def on_press_btn_auto_start(self):
    
        if self.btn_auto_start_state == 'down':
            self.mqtt_driver.client.publish("mobil/btn_auto_start", payload='normal', qos=0)
        elif self.btn_auto_start_state == 'normal':
            self.mqtt_driver.client.publish("mobil/btn_auto_start", payload='down', qos=0)

    def update_btn_auto_start(self, *args):
    
        if args[2].payload.decode() == 'down':
            self.btn_auto_start_state = 'down'
            self.ids.btn_auto_start.state = 'down'

        elif args[2].payload.decode() == 'normal':
            self.btn_auto_start_state = 'normal'
            self.ids.btn_auto_start.state = 'normal'


    def on_press_btn_auto_stop(self):

        if self.btn_auto_stop_state == 'down':
            self.mqtt_driver.client.publish("mobil/btn_auto_stop", payload='normal', qos=0)

        elif self.btn_auto_start_state == 'normal':
            self.mqtt_driver.client.publish("mobil/btn_auto_stop", payload='down', qos=0)


    def update_btn_auto_stop(self, *args):
    
        if args[2].payload.decode() == 'down':
            self.btn_auto_stop_state = 'down'
            self.ids.btn_auto_stop.state = 'down'

        elif args[2].payload.decode() == 'normal':
            self.btn_auto_stop_state = 'normal'
            self.ids.btn_auto_stop.state = 'normal'


    def on_touch_move_sldr_speed(self, *args):

        if len(args) == 0:
            
            self.current_speed = self.ids.slider_speed.value
            
            if abs(self.current_speed - self.last_sent_speed) > 5:
                self.mqtt_driver.client.publish("mobil/slider_speed", payload=str(self.current_speed), qos=0)
                self.last_sent_speed = self.current_speed


        else:
            self.current_speed = float(args[2].payload.decode())
            self.last_sent_speed = self.current_speed
            

    def on_touch_move_sldr_volume(self, *args):

        if len(args) == 0:
            self.current_volume = self.ids.slider_volume.value
            
            if abs(self.current_volume - self.last_sent_volume) > 5:
                self.mqtt_driver.client.publish("mobil/slider_volume", payload=self.current_volume, qos=0)
                self.last_sent_volume = self.current_volume
                

        else:
            self.current_volume = float(args[2].payload.decode())
            self.last_sent_volume = self.current_volume


    def showPopup(self, *args):
        
        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = "")
        closeButton = Button(text = "OK")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title = "",
                      content = layout,
                      size_hint =(None, None), size =(200, 200))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)        

        
class MessageBox(Popup):

    def dismiss(self):
        self.dismiss()
class mainApp(App):
   

    def build(self):
        pass


mainApp().run()