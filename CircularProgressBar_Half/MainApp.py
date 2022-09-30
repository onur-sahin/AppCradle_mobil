from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

from circular_progress_bar import CircularProgressBar


class CircularProgressBar_FloatLayout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 0
        self.progbar.max = 360


        self.add_widget(self.progbar)

        Clock.schedule_interval(self.animate, 0.5)


    def animate(self, dt):
        self.progbar._value = 366
        self.progbar._draw()






class MainApp(App):
    pass


MainApp().run()