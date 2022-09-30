from kivy.core.text import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import Clock

from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty, ColorProperty, StringProperty

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar

humidity_ = [0]

class HumidityBoxLayout(FloatLayout):

    humidity = NumericProperty(0.0)
    temp     = NumericProperty()

    warning  = BooleanProperty(False)
    warning_color = ColorProperty([1, 0, 0, 1])
    warning_label = StringProperty()
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_interval(self.update, 0.1)

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"

        self.progbar.min = 0
        self.progbar.max = 100

        self.progbar.convert_to_percent_value = False
        
        self.progbar.label = Label(text="{}%", font_size=40)
        
        self.btn = Button()

        self.btn.bind(on_press=self.yeni)

        self.add_widget(self.btn)
        self.add_widget(self.progbar)
        
        self.warning_label = ""
        self.warning_color = (0,0,0,0)

    def yeni(self, self_button):
        print("####################")


    def update(self, dt):
        
        self.progbar.label = Label(text="{}%", font_size = self.progbar.widget_size*0.3 )

        self.humidity = humidity_[0]
        
        self.btn.size = self.size
        self.btn.pos = self.pos
        
        self.setColor()
        
        self.check_warning()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        

        self.progbar._value = self.humidity
        
        self.progbar._draw()



    def check_warning(self):
        
        
        if self.humidity < 40:
            self.warning = True
            
                    
        elif self.humidity > 60:
            self.warning = True
           
            
        else:
            self.warning = False
            

    def setColor(self):
        
        h = self.humidity
        
        if (h < 30 ):               #TOO DRY   - MAROON
            
            self.progbar.progress_color, self.warning_color = (0.5, 0, 0, 1), (0.5, 0, 0, 1) 
            self.warning_label = "TOO TRY"
            
        elif (h >= 30 and h < 40):  #DRY       - ORANGE
            self.progbar.progress_color, self.warning_color = (1, 0.645, 0, 1), (1, 0.645, 0, 1)
            self.warning_label = "DRY"
        
        elif (h >= 40 and h <= 60): #NORMAL    - GREEN
            self.progbar.progress_color, self.warning_color = (0, 1, 0, 1), (0, 1, 0, 1)
            self.warning_label = "NORMAL"
        
        elif (h > 60 and h <= 70):  #MOIST     - LIGHT BLUE
            self.progbar.progress_color, self.warning_color = (0.5, 0.5, 1, 1), (0.5, 0.5, 1, 1)
            self.warning_label = "MOIST"
            
        elif (h > 70 ) :             #TOO MOIST- DARK BLUE
            self.progbar.progress_color, self.warning_color = (0, 0, 1, 1), (0, 0, 1, 1)
            self.warning_label = "TOO MOIST"
            
     


        














