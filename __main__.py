
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from time import sleep
import threading
from pygame import mixer
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import imutils

from Camera import CameraDriver

from Mqtt_Driver import Mqtt_Driver

from AirQuality import airQuality_
from Tempature import tempature_
from Humidity import humidity_

import json
from time import sleep

# test and develope for desktop
Window.size = (378, 672)


class MessageButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press(self):

        if self.id == 0:
            
            self.parent.parent.data.pop(0)
            self.parent.parent.data.insert(0, {'id':0, 'text': 'NO MESSAGE', 'size':(None, 50) })
            return
    
        for idx, dct in enumerate(self.parent.parent.data):

            if dct["id"] == self.id:
                self.parent.parent.data.pop(idx)
                return





class MainBoxLayout(BoxLayout):

    mqtt_driver = Mqtt_Driver()

    current_speed  = NumericProperty(25.0)
    last_sent_speed = -10.0

    current_volume = NumericProperty(25.0)
    last_sent_volume = -10.0

    btn_auto_start_state = 'normal'
    btn_auto_play_state  = 'normal'
    btn_auto_stop_state  = 'normal'

    

    btn_id = 1
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cameraDriver = CameraDriver()
        self.camera_thrd = threading.Thread( )

        self.pop = Popup()

        threading.Timer(interval=5, function=self.first_messageBox).start()
        
        mqtt_con_sub_thrd = threading.Timer(interval=5, function=self.mqtt_connect_subscribe)
        mqtt_con_sub_thrd.start()

        mixer.init()
 

    def mqtt_connect_subscribe(self):

        self.mqtt_driver.connect()

        self.mqtt_driver.client.subscribe("raspberry/#", qos=0)
        
        self.mqtt_driver.client.message_callback_add("raspberry/airQuality", self.update_airQuality)
        self.mqtt_driver.client.message_callback_add('raspberry/tempature', self.update_tempature)
        self.mqtt_driver.client.message_callback_add('raspberry/humidity', self.update_humidity)

        self.mqtt_driver.client.message_callback_add('raspberry/slider_speed', self.on_touch_move_sldr_speed)
        self.mqtt_driver.client.message_callback_add('raspberry/slider_volume', self.on_touch_move_sldr_volume)

        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_play_state', self.update_btn_auto_play)
        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_start_state', self.update_btn_auto_start)
        self.mqtt_driver.client.message_callback_add('raspberry/btn_auto_stop_state', self.update_btn_auto_stop)
        self.mqtt_driver.client.message_callback_add('raspberry/warning', self.update_message)
        self.mqtt_driver.client.message_callback_add('raspberry/flameDetected', self.update_message)
        self.mqtt_driver.client.message_callback_add('raspberry/vibrationDetected', self.update_message)

        self.mqtt_driver.client.message_callback_add('raspberry/startVideo', self.print_stream_status)
        self.mqtt_driver.client.message_callback_add('raspberry/stopVideo', self.stop_video)
        # self.mqtt_driver.client.message_callback_add('raspberry/warning_popup', self.show)

        self.mqtt_driver.client.loop_forever()

    def print_stream_status(self, *args):
        print("video streaming in online")

    def stop_video(self, *args):
        pass

    def on_press_btn_camera(self):

        if self.ids.btn_camera.state == 'down':

            self.camera_thrd = threading.Thread( target=self.cameraDriver.start_receiving_video )
            self.camera_thrd.start()

            self.img1=Image()
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(self.img1)

            btn_close = Button(text='CLOSE')
            btn_close.bind(on_press=self.stop_video_receiving)

            btn_Layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
            btn_Layout.add_widget(btn_close)

            btn_minimize = Button(text='MINIMIZE')
            btn_minimize.bind(on_press=self.minimize_video_receiving)

            btn_Layout.add_widget(btn_minimize)

            

            layout.add_widget(btn_Layout)

            self.pop = Popup(   title='test',
                                content=layout,
                                size_hint=(None, None),
                                size=(400, 400),
                                auto_dismiss=False
                            )

            

            self.pop.open()
            
            self.mqtt_driver.client.publish('mobil/btn_camera_start', qos=0)

            self.clck_cameraFrame = Clock.schedule_interval(self.updateVideo, 1.0/33.0)

        else:
            self.ids.btn_camera.state = 'down'
            if self.camera_thrd.is_alive():
                print("ekmlyuak")
                self.pop.open()
            
        


    def updateVideo(self, dt):

        # if not self.pop._is_open:
        #     self.cameraDriver.stop_signal = True
        

        frame = self.cameraDriver.frame

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

    def stop_video_receiving(self, *args):

        self.cameraDriver.stop_signal = True
        self.pop.dismiss()
        self.clck_cameraFrame.cancel()
        self.ids.btn_camera.state = 'normal'
        self.mqtt_driver.client.publish('mobil/btn_camera_stop', qos=0)
        
    def minimize_video_receiving(self, *args):
        self.pop.dismiss()



    def first_messageBox(self):
        self.ids.messageRV.data.append({'id':0, 'text': 'NO MESSAGE', 'size':(None, 50) })

    def update_message(self, *args):
        
        data = self.ids.messageRV.data
            
        warning = json.loads( args[2].payload.decode() )

        if warning["msg"] == 'THE BABY IS CRYING':
            text = ""
            temp = "  " + warning["sub_msg"]
            for word in temp.split(" "):
                if word == "":
                    continue

                if word[-1] == "%":
                    text += word + "  "
                elif word == "hungry:":
                    text += "hung:"
                
                elif word == "discomfort:":
                    text += "disc:"

                elif word == "belly":
                    text += "belly:"

                elif word == "pain:":
                    continue
                
                elif word == "burping:":
                    text += "burp:"

                else:
                    text += word
            
            warning["sub_msg"] = text

        if len(data) > 1:
    
            if data[1]['text'][7:] == warning['sub_msg']:
                data.pop(1)
    
        data[0]["text"] = warning["time"]+': '+warning["msg"]
                
        data.insert(1, {'id':self.btn_id, 'text':warning["time"] + ': ' + warning["sub_msg"]  })

        self.btn_id += 1

        if len(data) >= 5:  
            data.pop(-1)


        if warning["msg"] == 'THE BABY IS CRYING':
            self.play_audio('./Sounds/The baby is crying.wav')

        elif warning["msg"] == 'THE BABY WOKE UP':
            self.play_audio('./Sounds/The baby woke up.wav')

        elif warning["msg"] == "FLAME DETECTED":
            self.play_audio('./Sounds/Flame detected.wav')

    def update_airQuality(self, client, userdata, msg):
        print("123", (msg.payload))
        airQuality_[0] = int(msg.payload.decode())
       

    def update_tempature(self, client, userdata, msg):
        print("123", (msg.payload))
        tempature_[0] = float(msg.payload.decode())

    def update_humidity(self, client,userdata, msg):
        print("123", (msg.payload))
        humidity_[0] = int(msg.payload.decode())


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
            self.mqtt_driver.client.publish("mobil/btn_auto_play", payload="normal", qos=0)
        elif self.btn_auto_play_state == "normal":
            self.mqtt_driver.client.publish("mobil/btn_auto_play", payload="down", qos=0)

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

        elif self.btn_auto_stop_state == 'normal':
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

    def play_audio(self, audio_path):
        
        try:
            music = open(audio_path)
        
        except BaseException as err:
            print(err)
            return

        mixer.music.load(music)
        mixer.music.set_volume(1)
        mixer.music.play()

        

class mainApp(App):
    def build(self):
        pass


mainApp().run()