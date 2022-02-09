import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.config import Config
import os

#custom
import db_conn

img_disp = ''

Config.set('graphics', 'resizable', True)

class CreateButton(Button):

    def on_touch_down(self, touch):
       
        if self.collide_point(*touch.pos):

            disp_popup(self.text)
            return True
      
        return super(CreateButton, self).on_touch_down(touch)

class myGrid(GridLayout):

    
    def __init__(self, **kwargs):

        super(myGrid, self).__init__(**kwargs)

        self.cols=6

        for item in os.listdir('data\\dp_img'):
            if item != 'NA.png':
                fetch_id, fetch_name, fetch_dir  = db_conn.fetch(item)
                btn = CreateButton(text=fetch_name, background_normal='data\\dp_img\\' + item, color=(1, 0, 0), bold=True, font_size=20)
                self.add_widget(btn)

class gest(RelativeLayout):

    def __init__(self, img_id, **kwargs):

        global img_disp
        img_disp = img_id
        super(gest, self).__init__(**kwargs)

        fetch_id, fetch_name, fetch_dir = db_conn.edit_gest_fetch(img_disp)

        self.cols = 1
        self.rows = 2

        self.sub_layout = GridLayout(cols=1, rows=3)

        self.btn_layout = GridLayout(cols=2, rows=1)

        self.tag = TextInput(text=fetch_name, multiline=False)
        self.link = TextInput(text=fetch_dir, multiline=False)
        self.sub_layout.add_widget(self.tag)
        self.sub_layout.add_widget(self.link)

        self.btn_save = Button(text='Save')
        self.btn_save.bind(on_press=self.saver)

        self.btn_cancel = Button(text='Cancel')
        self.btn_cancel.bind(on_press=self.canceler)

        self.btn_layout.add_widget(self.btn_save)
        self.btn_layout.add_widget(self.btn_cancel)
        

        self.sub_layout.add_widget(self.btn_layout)
        self.add_widget(self.sub_layout)

    def _update_rect(self, instance, value):

        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def saver(self, instance):

        global img_disp

        change_id, a, a = db_conn.edit_gest_fetch(img_disp)
        change_name = self.tag.text
        change_dir = self.link.text

        db_conn.change(change_id, change_name, change_dir)
        App.get_running_app().stop()

    def canceler(self, instance):
        App.get_running_app().stop()


def disp_popup(img_id):

    show = gest(img_id)
    pop_wind = Popup(title=img_id, content=show, size_hint=(None, None), size=(400, 400))

    pop_wind.open()


class dp_gest(App):

    def build(self):
        return myGrid()


def run_this_app():
    dp_gest().run()

if __name__ == '__main__':
    run_this_app()