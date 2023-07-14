
import sys
import time
from ctypes import *
from riapi import RiApi


def main():

    servo_1 = c_int() 
    servo_4 = c_int() 
    servo_5 = c_int() 
    led = c_int()

    api = RiApi()
    api.init()


    api.add_led(led)

    api.led_flicker(led, 255, 0, 0, 500, 5)

    api.led_pulse(led, 255, 0, 0, 500)
    api.led_pulse(led, 0, 255, 0, 500)
    api.led_pulse(led, 0, 0, 255, 500)

    api.led_pulse_pause(led, 255, 0, 0, 1000, 200, 3)
    api.led_pulse_pause(led, 0, 255, 0, 1000, 200, 3)
    api.led_pulse_pause(led, 0, 0, 255, 1000, 200, 3)


    api.add_servo(servo_1, "mg90s", 0)
    api.add_servo(servo_4, "mg90s", 4)
    api.add_servo(servo_5, "mg90s", 5)


    api.turn_by_pulse(servo_1, 1600)
    time.sleep(1) 

    api.turn_by_angle(servo_1, 90, 200)
    time.sleep(1) 

    api.turn_by_angle(servo_1, -180, 300)
    time.sleep(1) 


    api.turn_by_pulse(servo_4, 1600)
    time.sleep(1) 

    api.turn_by_angle(servo_4, 90, 200)
    time.sleep(1) 

    api.turn_by_angle(servo_4, -180, 300)
    time.sleep(1) 


    api.turn_by_pulse(servo_5, 1600)
    time.sleep(1) 

    api.turn_by_angle(servo_5, 90, 200)
    time.sleep(1) 

    api.turn_by_angle(servo_5, -180, 300)
    time.sleep(1) 

    print("servo_1 angle: " + str(api.get_angle(servo_1)))
    print("servo_4 angle: " + str(api.get_angle(servo_4)))
    print("servo_5 angle: " + str(api.get_angle(servo_5)))

    api.cleanup_servo(servo_1)
    api.cleanup_servo(servo_4)
    api.cleanup_servo(servo_5)

    api.cleanup_led(led)
    api.cleanup_final()

    print("Success")

if __name__ == "__main__":
    main()