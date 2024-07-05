from socket import *
import sys
from inputs import get_gamepad
import time
import threading
import cv2, imutils
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLCDNumber
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont

global fthruster1,fthruster2,lthruster,rthruster,dthruster1,dthruster2
fthruster1 = 1500
fthruster2 = 1500
lthruster = 1500
rthruster = 1500
dthruster1 = 1500
dthruster2 = 1500

rec_array = [] 
ph_data_array = []
temp_data_array = []

global ph_data
global temp_data




address = ( '192.168.0.178', 5000) #Defind who you are talking to (must match arduino IP and port)
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.settimeout(1) #only wait 1 second for a resonse

class VideoCapture(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self._sensor_thread = threading.Thread(target=self.recieve_sensor_data, args=())
        self._sensor_thread.daemon = True
        self._sensor_thread.start()

    def initUI(self):
        self.setWindowTitle("Advanced Video Capture System")
        self.setWindowIcon(QIcon('camera_icon.png'))
        self.resize(1200, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #333333;
                color: #ffffff;
            }
            QLabel, QLCDNumber {
                font: bold 14px;
            }
            QPushButton {
                background-color: #0055ff;
                color: #ffffff;
                font: bold 14px;
                padding: 6px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #0077ff;
            }
            """)

        self.setupWidgets()
        self.setupLayout()

    def setupWidgets(self):
        self.video_label = QLabel("Original Feed")
        self.video_label.setAlignment(Qt.AlignCenter)
        # self.ml_video_label = QLabel("Processed Feed")
        # self.ml_video_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.system_status_led = QLabel()
        self.system_status_led.setFixedSize(20, 20)
        self.update_system_status_led(False)

        self.ph_lcd = QLCDNumber()
        # if(len(rec_array) == 0):
        #     self.ph_lcd.display("9.8")
        # else:
        #     self.ph_lcd.display(rec_array[0])
        self.temp_lcd = QLCDNumber()
        # self.water_pressure_lcd = QLCDNumber()
        self.water_level_lcd = QLCDNumber()
        self.water_level_lcd.display("False")

        self.start_button.clicked.connect(self.start_video)
        self.stop_button.clicked.connect(self.stop_video)

    def setupLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.video_label, 0, 0, 1, 3)
        # layout.addWidget(self.ml_video_label, 0, 3, 1, 3)
        layout.addWidget(self.start_button, 1, 0)
        layout.addWidget(self.stop_button, 1, 1)
        layout.addWidget(self.system_status_led, 1, 2, 1, 1, Qt.AlignCenter)

        sensors_info = [("pH Value:", self.ph_lcd), ("Temperature (C):", self.temp_lcd), ("Leak Detected :", self.water_level_lcd)]
        for i, (label, widget) in enumerate(sensors_info):
            layout.addWidget(QLabel(label), 2 + i, 0)
            layout.addWidget(widget, 2 + i, 1, 1, 2)

        self.setLayout(layout)

    def update_system_status_led(self, status):
        color = "green" if status else "red"
        self.system_status_led.setStyleSheet(f"QLabel {{ background-color: {color}; border-radius: 10px; }}")

    def start_video(self):
        self.video = cv2.VideoCapture("rtsp://admin:admin@192.168.1.10")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(33)

    def stop_video(self):
        self.timer.stop()
        self.video.release()

    def update_frames(self):
        ret, frame = self.video.read()
        if ret:
            original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            original_frame = imutils.resize(original_frame,height=720,width=1080)
            q_img_original = QImage(original_frame.data, original_frame.shape[1], original_frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img_original))

            # processed_frame = self.process_frame_with_ml_model(frame)
            # processed_frame = imutils.resize(processed_frame,height=720,width=1080)
            # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            # q_img_ml = QImage(original_frame.data, original_frame.shape[1], original_frame.shape[0], QImage.Format_RGB888)
            # self.ml_video_label.setPixmap(QPixmap.fromImage(q_img_ml))

    def recieve_sensor_data(self):
        global rec_array
        global ph_data_array
        global temp_data_array
        while True :
            if(len(ph_data_array) == 0):
                self.ph_lcd.display("7.8")
                self.temp_lcd.display("30")
            else :
                self.ph_lcd.display(ph_data_array[len(ph_data_array)-1][2:5])
                # print(ph_data)
                self.temp_lcd.display(str(temp_data_array[len(temp_data_array) - 1])[2:4])
                # print(temp_data)

class XboxController(object):
    MAX_TRIG_VAL = 250
    MAX_JOY_VAL = 110

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self): # return the buttons/triggers that you care about in this method
        if abs(self.RightJoystickX)<20 and abs(self.RightJoystickY)>20:
            self.surgecontrol()
            return self.RightJoystickY
        if abs(self.RightJoystickX)>20 and abs(self.RightJoystickY)<20:
            self.swaycontrol()
            return self.RightJoystickX
        if abs(self.LeftJoystickY)>20:
            # global flag
            # flag = 1
            self.heavecontrol()
            # time.sleep(2)
            return self.LeftJoystickY
        # if abs(self.RightJoystickY)<20 and abs(self.RightJoystickX)<20 and abs(self.LeftJoystickY) < 20 :
        #     self.rest()
        #     return [self.RightJoystickX,self.RightJoystickY,self.LeftJoystickY]
        # if abs(self.RightJoystickY) > 20:
        #     self.surgecontrolTest()
        #     return self.RightJoystickY
        # if abs(self.RightJoystickY) < 20 :
        #     self.restTest()
        #     return [self.RightJoystickY]
        # x = int(self.LeftJoystickX)
        # y = int(self.LeftJoystickY)
        if self.A :
            self.rest()
        # if abs(self.RightJoystickY)<20 and abs(self.RightJoystickX)<20 and abs(self.LeftJoystickY) < 20 :
        #     # if(flag):
        #     self.rest()
                
        # b = self.X # b=1, x=2
        # if self.LeftTrigger > 0 :
        #     self.rest()
        #     return self.LeftTrigger
        # r2 = self.RightTrigger
        # l3 = self.LeftThumb
        # r3 = self.RightThumb
        # r1 = self.RightBumper
        # l1 = self.LeftBumper

        # return [left,right, r1]
            
    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    if abs(self.LeftJoystickY) < 10:
                        self.LeftJoystickY = 0 
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    if abs(self.RightJoystickY) < 10:
                        self.RightJoystickY = 0
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    if abs(self.RightJoystickX) < 10:
                        self.RightJoystickX = 0
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
            
    def surgecontrol(self):
            fthruster1 = 1500
            fthruster2 = 1500
            lthruster = 1500
            rthruster = 1500
            dthruster1 = 1500
            dthruster2 = 1500
            val = self.RightJoystickY
            fthruster1 = 1500 + val
            fthruster2 = 1500 - val
            data = (str(int(fthruster1)) + "/" + str(int(fthruster2))  + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2))).encode('UTF-8') #Set data to Blue Command
            client_socket.sendto(data, address) #send command to arduino
            try:
                rec_data, addr = client_socket.recvfrom(2048) 
                #Read response from arduino
                print(rec_data) #Print the response from Arduino
            except:
                print("error")
            # print((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) +  "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))

    def swaycontrol(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1500
        rthruster = 1500
        dthruster1 = 1500
        dthruster2 = 1500
        val = self.RightJoystickX
        rthruster = 1500 + val
        lthruster = 1500 - val
        data = (str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "/").encode('UTF-8') #Set data to Blue Command
        client_socket.sendto(data, address) #send command to arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            print(rec_data) #Print the response from Arduino
        except:
            print("error")        
        # ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))
        # print(((str(fthruster1) + str(fthruster2) + str(lthruster) + str(rthruster) + str(dthruster1) + str(dthruster2) + '/').encode('UTF-8')))

    def heavecontrol(self):
        global rec_array
        global ph_data
        global ph_data_array
        global temp_data
        global temp_data_array
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1500
        rthruster = 1500
        dthruster1 = 1500
        dthruster2 = 1500
        val = self.LeftJoystickY
        dthruster1 = 1500 + val
        dthruster2 = 1500 - val
        data = (str(int(fthruster1)) + "/" + str(int(fthruster2))  + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2))).encode('UTF-8') 
        client_socket.sendto(data, address) #send command to arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            ph_data = (str(rec_data[0:4]))
            ph_data_array.append(str(ph_data))

            print(ph_data)
            temp_data = (str(rec_data[5:]))
            temp_data_array.append(str(temp_data))
            print(str(temp_data))
            for i in range(0,len(rec_array)):
                print(rec_array[i])
            # print(rec_data) #Print the response from Arduino
        except:
            print("error")        
        # ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))

    def rest(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1500
        rthruster = 1500
        dthruster1 = 1500
        dthruster2 = 1500
        data = (str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2))).encode('UTF-8') #Set data to Blue Command
        client_socket.sendto(data, address) #send command to arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            print(rec_data) #Print the response from Arduino
        except:
            print("error")        
        # global flag
        # while(flag):
        # ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))
            # flag_0 = 0
            # flag = 0

    def rotate(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1100
        rthruster = 1100
        dthruster1 = 1500
        dthruster2 = 1500
        val = self.LeftJoystickX
        if val > 0 :
            fthruster1 = 1500+val
            fthruster2 = 1500-val
        else :
            fthruster1 = 1500-val
            fthruster2 = 1500+val
        data = (str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8') #Set data to Blue Command
        client_socket.sendto(data, address) #send command to arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            print(rec_data) #Print the response from Arduino
        except:
            print("error")        
        # ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))


    def surgecontrolTest(self):
            fthruster1 = 1500
            # fthruster2 = 1500
            # lthruster = 1500
            # rthruster = 1500
            # dthruster1 = 1500
            # dthruster2 = 1500
            val = self.RightJoystickY
            fthruster1 = 1500 - val
            # fthruster2 = 1500 - val
            data = ((str(int(fthruster1)) + "*").encode('UTF-8'))
            client_socket.sendto(data, address) #send command to arduino
            try:
                rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
                print(rec_data) #Print the response from Arduino
            except:
                print("error")
            # ser.write((str(int(fthruster1)) + "*").encode('UTF-8'))
            # print(((str(fthruster1) + str(fthruster2) + str(lthruster) + str(rthruster) + str(dthruster1) + str(dthruster2) + '/').encode('UTF-8')))

    def restTest(self):
        fthruster1 = 1500
        data = ((str(int(fthruster1)) + "*").encode('UTF-8'))
        client_socket.sendto(data, address) #send command to arduino
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            print(rec_data) #Print the response from Arduino
        except:
            print("error")

        # ser.write((str(int(fthruster1)) + "*").encode('UTF-8'))

def xbox_thread():
        joy = XboxController()
        if joy:  
            while True:
                print(joy.read())
                time.sleep(0.2)
        else:
            print("Failed to initialize Xbox controller.")

def gui_thread():
    app = QApplication(sys.argv)
    
    window = VideoCapture()
    window.show()
    (app.exec_())
    

if __name__ == "__main__":
    
    xbox_thread = threading.Thread(target=xbox_thread)
    gui_thread = threading.Thread(target=gui_thread)
    xbox_thread.start()
    gui_thread.start()

    xbox_thread.join() 
    gui_thread.join()