from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from string import ascii_uppercase
from keras.models import model_from_json
import numpy as np
import operator
import subprocess
import cv2
import os
import time

#custom
import dp_gest
import db_conn

alpha_dict_ref = {'A':'1000.png', 'B':'1001.png', 'C':'1002.png', 'D':'1003.png', 'E':'1004.png', 'F':'1005.png', 'G':'1006.png', 'H':'1007.png', 'I':'1008.png', 'J':'NA.png', 'K':'1009.png', 'L':'1010.png', 'M':'1011.png', 'N':'1012.png', 'O':'1013.png', 'P':'1014.png', 'Q':'1015.png', 'R':'1016.png', 'S':'1017.png', 'T':'1018.png', 'U':'1019.png', 'V':'1020.png', 'W':'1021.png', 'X':'1022.png', 'Y':'1023.png', 'Z':'1024.png', 'Blank':'NA.png'}

loop_run = True

directory = 'data\\model\\'

json_file = open(directory+"model-bw.json", "r")
model_json = json_file.read()
json_file.close()
is_model = model_from_json(model_json)
is_model.load_weights(directory+"model-bw.h5")

json_file_dru = open(directory+"model-bw_dru.json" , "r")
model_json_dru = json_file_dru.read()
json_file_dru.close()
is_model_dru = model_from_json(model_json_dru)
is_model_dru.load_weights(directory+"model-bw_dru.h5")

json_file_tkdi = open(directory+"model-bw_tkdi.json" , "r")
model_json_tkdi = json_file_tkdi.read()
json_file_tkdi.close()
is_model_tkdi = model_from_json(model_json_tkdi)
is_model_tkdi.load_weights(directory+"model-bw_tkdi.h5")

json_file_smn = open(directory+"model-bw_smn.json" , "r")
model_json_smn = json_file_smn.read()
json_file_smn.close()
is_model_smn = model_from_json(model_json_smn)
is_model_smn.load_weights(directory+"model-bw_smn.h5")


class CamApp(App):

    def build(self):


        self.img1=Image()
        main_layout = GridLayout(cols=1, rows=3)
        settings_btn = Button(text='Settings', size_hint_x=None, size_hint_y=None, width=80, height=50)        
        main_layout.add_widget(self.img1)
        self.status_disp = Label()
        main_layout.add_widget(self.status_disp)
        main_layout.add_widget(settings_btn)
        settings_btn.bind(on_press=self.pressed)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return main_layout

    def update(self, dt):

        global loop_run
        
        ret, frame = self.capture.read()
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = texture1


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),2)
        th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
        ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        alpha_predicted = predictor(res)
        placeholder, name_img_disp, direc_to_open =  db_conn.fetch(alpha_dict_ref[alpha_predicted])

        if alpha_predicted == 'Blank':
            self.status_disp.text = 'NOTHING DISPLAYED'

        else:
            try:

                if os.path.exists(direc_to_open):

                    self.status_disp.text = 'Opening ___'
                    time.sleep(5)

                    for i in range(5):
                        self.status_disp.text = str(i)
                        time.sleep(1)
                subprocess.run(direc_to_open)
                App.get_running_app().stop()


            except FileNotFoundError:
                self.status_disp.text = 'Oopsie'


    def pressed(self, instance):
        App.get_running_app().stop()
        dp_gest.run_this_app()




def predictor(test_image):
        
    test_image = cv2.resize(test_image, (128,128))
    pred_img = is_model.predict(test_image.reshape(1, 128, 128, 1))
    pred_img_dru = is_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))
    pred_img_tkdi = is_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))
    pred_img_smn = is_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))
    retrieved={}
    retrieved['Blank'] = pred_img[0][0]
    inde = 1
    for i in ascii_uppercase:
        retrieved[i] = pred_img[0][inde]
        inde += 1

    retrieved = sorted(retrieved.items(), key=operator.itemgetter(1), reverse=True)
    letter_pred = retrieved[0][0]

    if(letter_pred == 'D' or letter_pred == 'R' or letter_pred == 'U'):
        retrieved = {}
        retrieved['D'] = pred_img_dru[0][0]
        retrieved['R'] = pred_img_dru[0][1]
        retrieved['U'] = pred_img_dru[0][2]
        retrieved = sorted(retrieved.items(), key=operator.itemgetter(1), reverse=True)
        letter_pred = retrieved[0][0]

    if(letter_pred == 'D' or letter_pred == 'I' or letter_pred == 'K' or letter_pred == 'T'):
        retrieved = {}
        retrieved['D'] = pred_img_tkdi[0][0]
        retrieved['I'] = pred_img_tkdi[0][1]
        retrieved['K'] = pred_img_tkdi[0][2]
        retrieved['T'] = pred_img_tkdi[0][3]
        retrieved = sorted(retrieved.items(), key=operator.itemgetter(1), reverse=True)
        letter_pred = retrieved[0][0]

    if(letter_pred == 'M' or letter_pred == 'N' or letter_pred == 'S'):
        retrieved1 = {}
        retrieved1['M'] = pred_img_smn[0][0]
        retrieved1['N'] = pred_img_smn[0][1]
        retrieved1['S'] = pred_img_smn[0][2]
        retrieved1 = sorted(retrieved1.items(), key=operator.itemgetter(1), reverse=True)
        if(retrieved1[0][0] == 'S'):
            letter_pred = retrieved1[0][0]
        else:
            letter_pred = retrieved[0][0]

    return letter_pred

if __name__ == '__main__':

    db_conn.create()
    res = CamApp().run()

    cv2.destroyAllWindows()