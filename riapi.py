import sys
import time
import platform
from ctypes import *

class RiApi:
    def __init__(self, is_async: c_bool):
        self.platform = platform.system()
        try:
            if self.platform == "Windows":
                self.lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")
            if self.platform == "Linux":
                self.lib = cdll.LoadLibrary("/usr/local/robohand_remote_control/librisdk.so")
        except OSError as e:
            raise Exception("Failed to load: " + str(e))
        self.errTextC = create_string_buffer(1000)
        self.i2c = c_int()
        self.pwm = c_int()
        self.is_async = is_async

    def async_on(self):
        self.is_async = c_bool(True)         

    def async_off(self):
        self.is_async = c_bool(False)         

    def init(self):
        self.lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_CreateBasic.argtypes = [POINTER(c_int), c_char_p]
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]
        descriptor = c_int()

        errCode = self.lib.RI_SDK_InitSDK(1, self.errTextC)
        if errCode != 0:
            raise Exception(f"init: RI_SDK_InitSDK failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_CreateBasic(descriptor, self.errTextC)
        if errCode != 0:
            raise Exception(f"init: RI_SDK_CreateBasic failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), self.pwm, self.errTextC)
        if errCode != 0:
            raise Exception(f"init: RI_SDK_CreateModelComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), self.i2c, self.errTextC)
        if errCode != 0:
            raise Exception(f"init: RI_SDK_CreateModelComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_LinkPWMToController(self.pwm, self.i2c, c_uint8(0x40), self.errTextC)
        if errCode != 0:
            raise Exception(f"init: RI_SDK_LinkPWMToController failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def add_servo(self, servo, servo_type, channel):
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        errCode = self.lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_servo: RI_SDK_CreateModelComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_LinkServodriveToController(servo, self.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_servo: RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.errTextC.raw.decode()}")        

    def add_custom_servo(self, MaxDt, MinDt, MaxSpeed, RangeAngle, channel):
        self.lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
        self.lib.RI_SDK_exec_ServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        servo = c_int()
        errCode = self.lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive".encode(),  servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_custom_servo: RI_SDK_CreateDeviceComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_exec_ServoDrive_CustomDeviceInit(servo, MaxDt, MinDt, MaxSpeed, RangeAngle, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_custom_servo: RI_SDK_exec_ServoDrive_CustomDeviceInit failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_LinkServodriveToController(servo, self.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_servo: RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.errTextC.raw.decode()}")     

        return(servo)

    def rotate(self, servo, direction, speed):
        self.lib.RI_SDK_exec_ServoDrive_Rotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

        errCode = self.lib.RI_SDK_exec_ServoDrive_Rotate(servo, direction, speed, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"rotate: RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def rotate_min_step(self, servo, direction, speed):
        self.lib.RI_SDK_exec_ServoDrive_MinStepRotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

        errCode = self.lib.RI_SDK_exec_ServoDrive_MinStepRotate(servo, direction, speed, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"rotate_min_step: RI_SDK_exec_ServoDrive_MinStepRotate failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def set_middle(self, servo):
        self.lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange.argtypes = [c_int, c_char_p]

        errCode = self.lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange(servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"turn: RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def turn_by_pulse(self, servo, dt):
        errCode = self.lib.RI_SDK_exec_ServoDrive_TurnByPulse(servo, dt, self.errTextC)
        if errCode != 0:
            raise Exception(f"turn_by_pulse: RI_SDK_exec_ServoDrive_TurnByPulse failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def turn_by_angle(self, servo, angle, speed):
        errCode = self.lib.RI_SDK_exec_ServoDrive_Turn(servo, angle, speed, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"turn_by_angle: RI_SDK_exec_ServoDrive_Turn failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def turn_by_duty(self, servo, steps):
        self.lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle.argtypes = [c_int, c_int, c_char_p]
        errCode = self.lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle(servo, steps, self.errTextC)
        if errCode != 0:
            raise Exception(f"turn_by_duty: RI_SDK_exec_ServoDrive_TurnByDutyCycle failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def get_angle(self, servo):
        self.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
        angle = c_int()
        errCode = self.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(servo, angle, self.errTextC)
        if errCode != 0:
            raise Exception(f"get_angle: RI_SDK_exec_ServoDrive_GetCurrentAngle failed with error code {errCode}: {self.errTextC.raw.decode()}")
        return(angle.value) 

    def cleanup_servo(self, servo):
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_DestroyComponent(servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"cleanup_servo: RI_SDK_DestroyComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")



    def add_rotate_servo(self, rservo, servo_type, channel):
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        errCode = self.lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive_rotate".encode(), servo_type.encode(), rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_rotate_servo: RI_SDK_CreateModelComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_LinkServodriveToController(rservo, self.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"addadd_rotate_servo_servo: RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.errTextC.raw.decode()}")        

    def add_custom_rotate_servo(self, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, channel):
        self.lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
        self.lib.RI_SDK_exec_RServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        self.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        rservo = c_int()

        errCode = self.lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive_rotate".encode(), rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_custom_rotate_servo: RI_SDK_CreateDeviceComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_exec_RServoDrive_CustomDeviceInit(rservo, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_custom_rotate_servo: RI_SDK_exec_RServoDrive_CustomDeviceInit failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_LinkServodriveToController(rservo, self.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_custom_rotate_servo: RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.errTextC.raw.decode()}")        

        return rservo

    def rotate_by_pulse(self, rservo, dt):
        self.lib.RI_SDK_exec_RServoDrive_RotateByPulse.argtypes = [c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RServoDrive_RotateByPulse(rservo, dt, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"rotate_by_pulse: RI_SDK_exec_RServoDrive_RotateByPulse failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def stop_rservo(self, rservo):
        self.lib.RI_SDK_exec_RServoDrive_Stop.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_exec_RServoDrive_Stop(rservo, self.errTextC)
        if errCode != 0:
            raise Exception(f"stop_rservo: RI_SDK_exec_RServoDrive_Stop failed with error code {errCode}: {self.errTextC.raw.decode()}")





    def add_led(self, led, r, g, b):
        self.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.lib.RI_SDK_LinkLedToController.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        errCode = self.lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), led, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_led: RI_SDK_CreateModelComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")
    #    errCode = self.lib.RI_SDK_LinkLedToController(led, self.pwm, 15, 14, 13, self.errTextC)
        errCode = self.lib.RI_SDK_LinkLedToController(led, self.pwm, r, g, b, self.errTextC)
        if errCode != 0:
            raise Exception(f"add_led: RI_SDK_LinkLedToController failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def stop_led(self, led):
        self.lib.RI_SDK_exec_RGB_LED_Stop.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_Stop(led, self.errTextC)
        if errCode != 0:
            raise Exception(f"stop_led: RI_SDK_exec_RGB_LED_Stop failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def cleanup_led(self, led):
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.lib.RI_SDK_DestroyComponent(led, self.errTextC)
        if errCode != 0:
            raise Exception(f"cleanup_led: RI_SDK_DestroyComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def led_pulse(self, led, r, g, b, duration):
        self.lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_SinglePulse(led, r, g, b, duration, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"led_pulse: RI_SDK_exec_RGB_LED_SinglePulse failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def led_pulse_pause(self, led, r, g, b, duration, pause, limit):
        self.lib.RI_SDK_exec_RGB_LED_FlashingWithPause.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_FlashingWithPause(led, r, g, b, duration, pause, limit, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"led_pulse_pause: RI_SDK_exec_RGB_LED_FlashingWithPause failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def led_pulse_frequency(self, led, r, g, b, frequency, limit):
        self.lib.RI_SDK_exec_RGB_LED_FlashingWithFrequency.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_FlashingWithFrequency(led, r, g, b, frequency, limit, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"led_pulse_pause: RI_SDK_exec_RGB_LED_FlashingWithFrequency failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def led_flicker(self, led, r, g, b, duration, limit):
        self.lib.RI_SDK_exec_RGB_LED_Flicker.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
        errCode = self.lib.RI_SDK_exec_RGB_LED_Flicker(led, r, g, b, duration, limit, self.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"led_flicker: RI_SDK_exec_RGB_LED_Flicker failed with error code {errCode}: {self.errTextC.raw.decode()}")

    def cleanup_final(self):
        self.lib.RI_SDK_sigmod_PWM_ResetAll.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        self.lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]
        errCode = self.lib.RI_SDK_sigmod_PWM_ResetAll(self.pwm, self.errTextC)
        if errCode != 0:
            raise Exception(f"cleanup_final: RI_SDK_sigmod_PWM_ResetAll failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_DestroyComponent(self.i2c, self.errTextC)
        if errCode != 0:
            raise Exception(f"cleanup_final: RI_SDK_DestroyComponent failed with error code {errCode}: {self.errTextC.raw.decode()}")

        errCode = self.lib.RI_SDK_DestroySDK(True, self.errTextC)
        if errCode != 0:
            raise Exception(f"cleanup_final: RI_SDK_DestroySDK failed with error code {errCode}: {self.errTextC.raw.decode()}")
