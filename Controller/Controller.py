from inputs import get_gamepad
import math
import threading
import time
import serial

global ser,fthruster1,fthruster2,lthruster,rthruster,dthruster1,dthruster2,claw
fthruster1 = 1500
fthruster2 = 1500
lthruster = 1100
rthruster = 1100
dthruster1 = 1500
dthruster2 = 1500
claw = 100
ser = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=1,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )

class XboxController(object):
    MAX_TRIG_VAL = 400
    MAX_JOY_VAL = 165

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
            self.heavecontrol()
            return self.LeftJoystickY
        if abs(self.RightJoystickY)<20 and abs(self.RightJoystickX)<20 and abs(self.LeftJoystickY) < 20 :
            self.rest()
            return [self.RightJoystickX,self.RightJoystickY,self.LeftJoystickY]
        # x = int(self.LeftJoystickX)
        # y = int(self.LeftJoystickY)
        # a = self.A
        # b = self.X # b=1, x=2
        # l2 = self.LeftTrigger
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
            lthruster = 1100
            rthruster = 1100
            dthruster1 = 1500
            dthruster2 = 1500
            val = self.RightJoystickY
            fthruster1 = 1500 - val
            fthruster2 = 1500 - val
            ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))
            # print(((str(fthruster1) + str(fthruster2) + str(lthruster) + str(rthruster) + str(dthruster1) + str(dthruster2) + '/').encode('UTF-8')))

    def swaycontrol(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1100
        rthruster = 1100
        dthruster1 = 1500
        dthruster2 = 1500
        val = self.RightJoystickX
        rthruster = 1100 + val
        lthruster = 1100 + val
        ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))
        # print(((str(fthruster1) + str(fthruster2) + str(lthruster) + str(rthruster) + str(dthruster1) + str(dthruster2) + '/').encode('UTF-8')))

    def heavecontrol(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1100
        rthruster = 1100
        dthruster1 = 1500
        dthruster2 = 1500
        val = self.LeftJoystickY
        dthruster1 = 1500 - val
        dthruster2 = 1500 - val
        ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))

    def rest(self):
        fthruster1 = 1500
        fthruster2 = 1500
        lthruster = 1100
        rthruster = 1100
        dthruster1 = 1500
        dthruster2 = 1500
        ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))

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
        
        ser.write((str(int(fthruster1)) + "/" + str(int(fthruster2)) + "/" + str(int(lthruster)) + "/" + str(int(rthruster)) + "/" + str(int(dthruster1)) + "/" + str(int(dthruster2)) + "*").encode('UTF-8'))


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
            ser.write((str(int(fthruster1)) + "*").encode('UTF-8'))
            # print(((str(fthruster1) + str(fthruster2) + str(lthruster) + str(rthruster) + str(dthruster1) + str(dthruster2) + '/').encode('UTF-8')))

if __name__ == '__main__':
    joy = XboxController()
    while True:
        print(joy.read())
        time.sleep(0.2)