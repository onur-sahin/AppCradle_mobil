from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import Clock
from kivy.core.text import Label as core_Label
from kivy.uix.label import Label
from kivy.graphics import Line, Rectangle, Color
from kivy.properties import ColorProperty, StringProperty

from kivy.metrics import dp

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar


tempature_ = [0]

class TempatureBoxLayout(FloatLayout):

    tempature = NumericProperty()
    
    warning = BooleanProperty(False)
    fnt_size =  NumericProperty(10)
    warning_color = ColorProperty([1, 0, 0, 1])
    warning_label = StringProperty("Normal")
    

    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.1)

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 0
        self.progbar.max = 44
        self.progbar.convert_to_percent_value = False
        
        self.progbar.label = core_Label(text="{}\u00B0C", font_size = 30 )
        
        self.btn = Button()
      
        self.btn.bind(on_press=self.yeni)
                         
        self.add_widget(self.btn)
        self.add_widget(self.progbar)
        

        
    def yeni(self, self_button):
        print("#################")
      



    def update(self, dt):
            
        self.progbar.label = core_Label(text="{}\u00B0C", font_size = self.progbar.widget_size*0.3 )
        
        self.btn.size = self.size
        self.btn.pos = self.pos
        
        self.tempature = tempature_[0]
        
        self.setColor()
        
        self.check_warning()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        

        self.progbar._value = self.tempature
        
        self.progbar._draw()
        
        # self.warning_label = "norm"
        
        # self.warning_color = (1, 0, 0, 1)
        
        
        
        
    def check_warning(self):
        
        
        if self.tempature < 20:
            self.warning = True
            
                    
        elif self.tempature > 26:
            self.warning = True
           
            
        else:
            self.warning = False
            

    def setColor(self):
        
        t = self.tempature
        
        if (t < 18 ):               #TOO COLD - BLUE
            
            self.progbar.progress_color, self.warning_color = (0, 0, 1, 1), (0, 0, 1, 1)
            self.warning_label = "TOO COLD"
            
        elif (t >= 18 and t < 20):  #COLD     - TURQUAZ
            self.progbar.progress_color, self.warning_color = (0, 0.9, 0.9, 1), (0, 0.9, 0.9, 1)
            self.warning_label = "COLD"
        
        elif (t >= 20 and t <= 24): #NORMAL   - GREEN
            self.progbar.progress_color, self.warning_color = (0, 1, 0, 1), (0, 1, 0, 1)
            self.warning_label = "NORMAL"
        
        elif (t > 24 and t <= 26):  #WARM     - YELLOW
            self.progbar.progress_color, self.warning_color = (0.996, 0.945, 0.376, 0.7), (0.996, 0.945, 0.376, 0.7)
            self.warning_label = "WARM"
            
        elif (t >26 and t <=28 ) :  #HOT      - ORANGE
            self.progbar.progress_color, self.warning_color = (1, 0.645, 0, 1), (1, 0.645, 0, 1)
            self.warning_label = "HOT"
            
        elif (t > 28 and t <= 32):  #TOO HOT  - RED
            self.progbar.progress_color, self.warning_color = (1, 0, 0, 1), (1, 0, 0, 1)
            self.warning_label = "TOO HOT"
        
        elif (t > 32):              #VERY HOT  - MAROON
            self.progbar.progress_color, self.warning_color = (0.5, 0, 0, 1), (0.5, 0, 0, 1)
            self.warning_label = "VERY HOT"






