import sys
import time
from ctypes import *

class RiApi:
    def __init__(self):
        self.lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")        
        self.errTextC = create_string_buffer(1000)  # Текст ошибки. C type: char*
        self.i2c = c_int()
        self.pwm = c_int()


    def init(self):
        self.lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_CreateBasic.argtypes = [POINTER(c_int), c_char_p]
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        descriptor = c_int()

        errCode = self.lib.RI_SDK_InitSDK(1, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

        errCode = self.lib.RI_SDK_CreateBasic(descriptor, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)
#        print("descriptor: ", descriptor.value)

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), self.pwm, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), self.i2c, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

        errCode = self.lib.RI_SDK_LinkPWMToController(self.pwm, self.i2c, c_uint8(0x40), self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

    def add_servo(self, servo, servo_type, channel):
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        errCode = self.lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), servo, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

        errCode = self.lib.RI_SDK_LinkServodriveToController(servo, self.pwm, channel, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

    def turn_by_pulse(self, servo, dt):
        errCode = self.lib.RI_SDK_exec_ServoDrive_TurnByPulse(servo, dt, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

    def turn_by_angle(self, servo, angle, speed):
        errCode = self.lib.RI_SDK_exec_ServoDrive_Turn(servo, angle, speed, c_bool(False), self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

    def get_angle(self, servo):
        self.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
        angle = c_int()
        errCode = self.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(servo, angle, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 
        return(angle.value) 

    def cleanup_servo(self, servo):
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_DestroyComponent(servo, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

    def add_led(self, led):
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkLedToController.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        errCode = self.lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), led, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 
    #    errCode = self.lib.RI_SDK_LinkLedToController(led, self.pwm, 15, 14, 13, self.errTextC)
        errCode = self.lib.RI_SDK_LinkLedToController(led, self.pwm, 14, 15, 13, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

    def cleanup_led(self, led):
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_DestroyComponent(led, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 

    def led_pulse(self, led, r, g, b, duration):
        self.lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_SinglePulse(led, r, g, b, duration, c_bool(False), self.errTextC)

    def led_pulse_pause(self, led, r, g, b, duration, pause, limit):
        self.lib.RI_SDK_exec_RGB_LED_FlashingWithPause.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_FlashingWithPause(led, r, g, b, duration, pause, limit, False, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

    def led_flicker(self, led, r, g, b, duration, limit):
        self.lib.RI_SDK_exec_RGB_LED_Flicker.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_Flicker(led, r, g, b, duration, limit, False, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)  

    def cleanup_final(self):
        self.lib.RI_SDK_sigmod_PWM_ResetAll.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]
        errCode = self.lib.RI_SDK_sigmod_PWM_ResetAll(self.pwm, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

        errCode = self.lib.RI_SDK_DestroyComponent(self.i2c, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2)

        errCode = self.lib.RI_SDK_DestroySDK(True, self.errTextC)
        if errCode != 0:
            print(errCode, self.errTextC.raw.decode())
            sys.exit(2) 