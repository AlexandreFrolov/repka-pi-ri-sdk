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


    # Инициализация шим-модулятора
    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), pwm, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    # Инициализация i2c адаптера 
    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), i2c, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    # Подключение i2c адаптера к шим-модулятору 
    errCode = lib.RI_SDK_LinkPWMToController(pwm, i2c, c_uint8(0x40), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 


def servo_init(lib, pwm, servo_1, servo_2, servo_3):
    errTextC = create_string_buffer(1000) 


# Инициализация 3-х сервоприводов
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), "mg90s".encode(), servo_1, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 
    
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), "mg90s".encode(), servo_2, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 
    
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), "mg90s".encode(), servo_3, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

# Подключение 3-х сервоприводов к шим модулятору

    errCode = lib.RI_SDK_LinkServodriveToController(servo_1, pwm, 0, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 
    
    errCode = lib.RI_SDK_LinkServodriveToController(servo_2, pwm, 1, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 
    
    errCode = lib.RI_SDK_LinkServodriveToController(servo_3, pwm, 2, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

def led_init(lib, pwm, led):
    # Инициализация светодиода
    errTextC = create_string_buffer(1000) 

    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), led, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 



    # Подключение светодиода к шим модулятору
    errCode = lib.RI_SDK_LinkLedToController(led, pwm, 15, 14, 13, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)


def cleanup(lib, pwm, i2c, servo_1, servo_2, servo_3, led):
    errTextC = create_string_buffer(1000)  # Текст ошибки. C type: char*

    errCode = lib.RI_SDK_sigmod_PWM_ResetAll(pwm, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroyComponent(i2c, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroyComponent(servo_1, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroyComponent(servo_2, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroyComponent(servo_3, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)        

    errCode = lib.RI_SDK_DestroyComponent(led, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_DestroySDK(True, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)	

def main():

    errTextC = create_string_buffer(1000)  # Текст ошибки. C type: char*
    i2c = c_int()
    pwm = c_int()
    led = c_int()
    servo_1 = c_int() 
    servo_2 = c_int() 
    servo_3 = c_int() 

    lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")

    init(lib, i2c, pwm)
    servo_init(lib, pwm, servo_1, servo_2, servo_3)
    led_init(lib, pwm, led)


    # Поворот сервопривода на заданный угол с заданной угловой скоростью 
    errCode = lib.RI_SDK_exec_ServoDrive_Turn(servo_2, 90, 100, c_bool(False), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)
    print(90)

    errCode = lib.RI_SDK_exec_ServoDrive_Turn(servo_2, 90, 100, c_bool(False), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)
    print(90)


#    errCode = lib.RI_SDK_exec_ServoDrive_Turn(servo_1, 90, 100, c_bool(False), errTextC)
#    if errCode != 0:
#        print(errCode, errTextC.raw.decode())
#        sys.exit(2)


   # Поучение текущего угла поворота сервопривода
    lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
    time.sleep(0.2)
    angle = c_int()
    errCode = lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(servo_2, angle, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    print("angle: ", angle.value) 


    lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]
    lib.RI_SDK_exec_RGB_LED_Flicker.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]


    errCode = lib.RI_SDK_exec_RGB_LED_Flicker(led, 0, 255, 0, 500, 10, c_bool(False), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    errCode = lib.RI_SDK_exec_RGB_LED_SinglePulse(led, 0, 0, 255, 10000, c_bool(False), errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    cleanup(lib, pwm, i2c, servo_1, servo_2, servo_3, led)
    print("Success")

if __name__ == "__main__":
    main()