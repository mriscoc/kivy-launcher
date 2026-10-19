"""Basic example for kivy_matplotlib_widget

Note:
    MatplotFigure is used when you have only 1 axis with lines only.
    For general purpose, please use MatplotFigureSubplot widget.

"""

from kivy.utils import platform
from kivy.config import Config

#avoid conflict between mouse provider and touch (very important with touch device)
#no need for android platform
if platform != 'android':
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_on_activity')
Config.set('kivy', 'log_level', 'debug')

from kivy.lang import Builder
from kivy.app import App

import matplotlib.pyplot as plt
import kivy_matplotlib_widget #register all widgets to kivy register
import numpy as np

print("Todo Importado")

KV = '''
Screen
    figure_wgt:figure_wgt
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            size_hint_y:0.1
            Button:
                text:"home"
                on_release:app.home()
            ToggleButton:
                group:'touch_mode'
                state:'down'
                text:"pan"
                on_release:
                    app.set_touch_mode('pan')
                    self.state='down'
            ToggleButton:
                group:'touch_mode'
                text:"zoom box"
                on_release:
                    app.set_touch_mode('zoombox')
                    self.state='down'
        MatplotFigure:
            id:figure_wgt
'''

plt.style.use('dark_background')

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

class Test(App):

    def build(self):
        self.screen=Builder.load_string(KV)

        # Setup plot
        self.fig, self.ax1 = plt.subplots()
        self.ax1.set(xlabel='time (s)', ylabel='voltage (mV)', title='Test Matplot in Kivy')
        self.ax1.grid(alpha=0.5)

        return self.screen

    def on_start(self, *args):
        self.ax1.plot(t, s)
        self.screen.figure_wgt.figure = self.fig

    def set_touch_mode(self,mode):
        self.screen.figure_wgt.touch_mode=mode

    def home(self):
        self.screen.figure_wgt.home()

Test().run()