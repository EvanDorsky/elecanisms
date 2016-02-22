
import usb.core
import time

class encodertest:

    def __init__(self):
        self.TOGGLE_LED1 = 1
        self.TOGGLE_LED2 = 2
        self.READ_SW1 = 3
        self.TOGGLE_LED3 = 8
        self.READ_SW2 = 9
        self.READ_SW3 = 10
        # self.WRITE_KS = 11

        self.JOY_READ_ANGLE = 5
        self.JOY_SET_MODE = 20
        self.JOY_SET_K = 21
        self.JOY_SET_WALL_LEFT = 22
        self.JOY_SET_WALL_RIGHT = 23
        self.JOY_SET_B = 24
        self.JOY_READ_VEL = 25
        self.JOY_READ_D = 26
        self.JOY_READ_DIR = 27

        self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
        if self.dev is None:
            raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
        self.dev.set_configuration()

# AS5048A Register Map
        self.ENC_NOP = 0x0000
        self.ENC_CLEAR_ERROR_FLAG = 0x0001
        self.ENC_PROGRAMMING_CTRL = 0x0003
        self.ENC_OTP_ZERO_POS_HI = 0x0016
        self.ENC_OTP_ZERO_POS_LO = 0x0017
        self.ENC_DIAG_AND_AUTO_GAIN_CTRL = 0x3FFD
        self.ENC_MAGNITUDE = 0x3FFE
        self.ENC_ANGLE_AFTER_ZERO_POS_ADDER = 0x3FFF

    def close(self):
        self.dev = None

    def toggle_led1(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED1)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED1 vendor request."

    def toggle_led2(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED2)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED2 vendor request."

    def toggle_led3(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED3)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED3 vendor request."

    def read_sw1(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW1, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW1 vendor request."
        else:
            return int(ret[0])

    def read_sw2(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW2, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW2 vendor request."
        else:
            return int(ret[0])

    def read_sw3(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW3, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW3 vendor request."
        else:
            return int(ret[0])

    def joy_read_angle(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_READ_ANGLE, 0, 0, 4)
        except usb.core.USBError:
            print "Could not send JOY_READ_ANGLE vendor request."
        else:
            return ret

    # def write_ks(self, value):
    #     try:
    #         ret = self.dev.ctrl_transfer(0xC0, self.WRITE_KS, value, 0, 2)
    #     except usb.core.USBError:
    #         print "Could not send WRITE_KS vendor request."
    #     else:
    #         return ret

    def joy_set_mode(self, value):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_SET_MODE, value, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_SET_MODE vendor request."
        else:
            return ret

    def joy_set_k(self, value):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_SET_K, value, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_SET_K vendor request."
        else:
            return ret

    def joy_set_wall_left(self, value):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_SET_WALL_LEFT, value, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_SET_WALL_LEFT vendor request."
        else:
            return 

    def joy_set_wall_right(self, value):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_SET_WALL_RIGHT, value, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_SET_WALL_RIGHT vendor request."
        else:
            return ret

    def joy_set_b(self, value):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_SET_B, value, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_SET_B vendor request."
        else:
            return ret

    def joy_read_vel(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_READ_VEL, 0, 0, 4)
        except usb.core.USBError:
            print "Could not send JOY_READ_VEL vendor request."
        else:
            return ret

    def joy_read_d(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_READ_D, 0, 0, 4)
        except usb.core.USBError:
            print "Could not send JOY_READ_D vendor request."
        else:
            return ret

    def joy_read_dir(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.JOY_READ_DIR, 0, 0, 2)
        except usb.core.USBError:
            print "Could not send JOY_READ_DIR vendor request."
        else:
            return ret
