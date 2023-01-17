

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import requests
from kivy.uix.button import Button

class MainPage(BoxLayout):

    def sent(self):
        resp = requests.post(   "http://cradle-server.herokuapp.com/predict",
                            files={"file":str.encode("euaueaeuauauaea")}
                            # data={"data":str.encode("euaueaeuauauaea")}
                            )
                    
        
        self.ids.label.text = str(resp.text)


class denemeApp(App):
    pass

denemeApp().run()