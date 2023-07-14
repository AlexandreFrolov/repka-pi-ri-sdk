import sys
import time
from ctypes import *


def init(lib, i2c, pwm):
    lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
    lib.RI_SDK_CreateBasic.argtypes = [POINTER(c_int), c_char_p]
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

    errTextC = create_string_buffer(1000) 
    descriptor = c_int()

    errCode = lib.RI_SDK_InitSDK(1, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_CreateBasic(descriptor, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)
    print("descriptor: ", descriptor.value)

    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), pwm, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), i2c, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    errCode = lib.RI_SDK_LinkPWMToController(pwm, i2c, c_uint8(0x40), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 


def add_servo(lib, pwm, servo, servo_type, channel):
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]
    errTextC = create_string_buffer(1000) 

    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), servo, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    errCode = lib.RI_SDK_LinkServodriveToController(servo, pwm, channel, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

def cleanup_servo(lib, pwm, i2c, servo):
    lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)

    errCode = lib.RI_SDK_DestroyComponent(servo, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

def add_led(lib, pwm, led):
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkLedToController.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
    errTextC = create_string_buffer(1000) 

    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), led, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

#    errCode = lib.RI_SDK_LinkLedToController(led, pwm, 15, 14, 13, errTextC)
    errCode = lib.RI_SDK_LinkLedToController(led, pwm, 14, 15, 13, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

def cleanup_led(lib, pwm, i2c, led):
    lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)

    errCode = lib.RI_SDK_DestroyComponent(led, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)	

def cleanup_final(lib, pwm, i2c):
    lib.RI_SDK_sigmod_PWM_ResetAll.argtypes = [c_int, c_char_p]
    lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
    lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]

    errTextC = create_string_buffer(1000)

    errCode = lib.RI_SDK_sigmod_PWM_ResetAll(pwm, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroyComponent(i2c, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroySDK(True, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)	

def turn_by_pulse(lib, servo, dt):
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_TurnByPulse(servo, dt, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

def turn_by_angle(lib, servo, angle, speed):
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_Turn(servo, angle, speed, c_bool(False), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

def get_angle(lib, servo):
    errTextC = create_string_buffer(1000)
    lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
    angle = c_int()
    errCode = lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(servo, angle, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 
    return(angle.value) 


def led_pulse(lib, led, r, g, b, duration):
    lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RGB_LED_SinglePulse(led, r, g, b, duration, c_bool(False), errTextC)

def led_pulse_pause(lib, led, r, g, b, duration, pause, limit):
    lib.RI_SDK_exec_RGB_LED_FlashingWithPause.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RGB_LED_FlashingWithPause(led, r, g, b, duration, pause, limit, False, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

def led_flicker(lib, led, r, g, b, duration, limit):
    lib.RI_SDK_exec_RGB_LED_Flicker.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RGB_LED_Flicker(led, r, g, b, duration, limit, False, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)




def main():

    errTextC = create_string_buffer(1000)  # Текст ошибки. C type: char*
    i2c = c_int()
    pwm = c_int()
    led = c_int()
    servo_1 = c_int() 
    servo_4 = c_int() 
    servo_5 = c_int() 

    lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")

    init(lib, i2c, pwm)
    add_led(lib, pwm, led)
    # add_servo(lib, pwm, servo_1, "mg90s", 0)
    # add_servo(lib, pwm, servo_4, "mg90s", 4)
    # add_servo(lib, pwm, servo_5, "mg90s", 5)


    led_flicker(lib, led, 255, 0, 0, 500, 5)

    led_pulse(lib, led, 255, 0, 0, 500)
    led_pulse(lib, led, 0, 255, 0, 500)
    led_pulse(lib, led, 0, 0, 255, 500)

    led_pulse_pause(lib, led, 255, 0, 0, 1000, 200, 3)
    led_pulse_pause(lib, led, 0, 255, 0, 1000, 200, 3)
    led_pulse_pause(lib, led, 0, 0, 255, 1000, 200, 3)


    cleanup_led(lib, pwm, i2c, led)
    cleanup_final(lib, pwm, i2c)
    sys.exit(0)

    # time.sleep(1) 
    # turn_by_pulse(lib, servo_1, 2600)

    # time.sleep(1) 
    # turn_by_pulse(lib, servo_1, 1600)

    # time.sleep(1) 
    # turn_by_pulse(lib, servo_3, 600)
    # time.sleep(1) 

    # turn_by_pulse(lib, servo_3, 1600)
    # time.sleep(1) 
    # turn_by_pulse(lib, servo_3, 2600)
    # time.sleep(1) 


    turn_by_pulse(lib, servo_1, 1600)
    time.sleep(1) 

    turn_by_angle(lib, servo_1, 90, 200)
    time.sleep(1) 

    turn_by_angle(lib, servo_1, -180, 300)
    time.sleep(1) 


    turn_by_pulse(lib, servo_4, 1600)
    time.sleep(1) 

    turn_by_angle(lib, servo_4, 90, 200)
    time.sleep(1) 

    turn_by_angle(lib, servo_4, -180, 300)
    time.sleep(1) 


    turn_by_pulse(lib, servo_5, 1600)
    time.sleep(1) 

    turn_by_angle(lib, servo_5, 90, 200)
    time.sleep(1) 

    turn_by_angle(lib, servo_5, -180, 300)
    time.sleep(1) 



    # turn_by_pulse(lib, servo_2, 1600)
    # time.sleep(1) 

    # turn_by_angle(lib, servo_2, 90, 200)
    # time.sleep(1) 

    # turn_by_angle(lib, servo_2, -180, 300)
    # time.sleep(1) 

    print("servo_1 angle: " + str(get_angle(lib, servo_1)))
    print("servo_2 angle: " + str(get_angle(lib, servo_4)))
    print("servo_3 angle: " + str(get_angle(lib, servo_5)))



    cleanup_servo(lib, pwm, i2c, servo_1)
    cleanup_servo(lib, pwm, i2c, servo_4)
    cleanup_servo(lib, pwm, i2c, servo_5)
    cleanup_led(lib, pwm, i2c, led)
    cleanup_final(lib, pwm, i2c)
    print("Success")

if __name__ == "__main__":
    main()