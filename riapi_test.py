
import sys
import time
from ctypes import *
from riapi import RiApi

def main():
    try:
        servo_1 = c_int() 
        servo_4 = c_int() 
        servo_5 = c_int() 
        rservo = c_int() 
        led = c_int()

    #    api = RiApi(c_bool(False))
        api = RiApi(c_bool(True))
        api.init()


        api.add_rotate_servo(rservo, "mg996r", 8)
        api.rotate_by_pulse(rservo, 2000)

        time.sleep(5) 

#        api.rotate_by_pulse(rservo, 1000)
        api.stop_rservo(rservo)

        sys.exit(2)



        api.add_led(led, 14, 15, 13)
#        api.async_off()

        # api.led_flicker(led, 255, 0, 0, 500, 5)
        # api.led_flicker(led, 0, 255, 0, 500, 5)
        # api.led_flicker(led, 0, 0, 255, 500, 5)
#        time.sleep(1) 
        # api.led_pulse(led, 255, 0, 0, 500)
        # api.led_pulse(led, 0, 255, 0, 500)
        # api.led_pulse(led, 0, 0, 255, 500)
        # api.led_pulse_pause(led, 255, 0, 0, 1000, 200, 3)
        # api.led_pulse_pause(led, 0, 255, 0, 1000, 200, 3)
        # api.led_pulse_pause(led, 0, 0, 255, 1000, 200, 3)
        # api.led_pulse_frequency(led, 255, 0, 0, 10, 10)
        # api.led_pulse_frequency(led, 0, 255, 0, 20, 10)
        # api.led_pulse_frequency(led, 0, 0, 255, 30, 10)
#        api.async_on()

        api.add_servo(servo_1, "mg90s", 0)
#        servo_1 = api.add_custom_servo(2430, 365, 200, 229, 0)
#       servo_1 = api.add_custom_servo(2160, 365, 200, 180, 0)

        api.add_servo(servo_4, "mg90s", 4)
        api.add_servo(servo_5, "mg90s", 5)

        print("MG90S rotate")

        api.rotate(servo_1, 0, 200) # 2320 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229

        api.rotate(servo_1, 1, 200) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0


        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114


        print("MG90S by_pulse")

        api.turn_by_pulse(servo_1, 2430) # 2330 mc на осциллографе
#        api.turn_by_pulse(servo_1, 2650) # 2550 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229 (custom 207)


        api.turn_by_pulse(servo_1, 365) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0
        
        api.turn_by_pulse(servo_1, 1395) # 1330 mc на осциллографе
#        api.turn_by_pulse(servo_1, 1500) # 1430 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114 (custom 103)
        


        # api.set_middle(servo_1)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))



        # MG90S
        # api.turn_by_pulse(servo_1, 365) # 348 mc на осциллографе
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # api.turn_by_pulse(servo_1, 1260) # 1210 mc на осциллографе
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # api.turn_by_pulse(servo_1, 2160) # 2080 mc на осциллографе
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))


        # api.rotate_min_step(servo_1, 1, 100)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # api.rotate_min_step(servo_1, 0, 100)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))


        # api.turn_by_duty(servo_1, 75)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))

        # api.turn_by_duty(servo_1, 300)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))

        # api.turn_by_duty(servo_1, 540)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))


        # SG90
        # api.turn_by_pulse(servo_1, 380)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # api.turn_by_pulse(servo_1, 1260)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # api.turn_by_pulse(servo_1, 2165)
        # time.sleep(2) 
        # print("servo_1 angle: " + str(api.get_angle(servo_1)))



        # api.turn_by_angle(servo_1, 90, 200)
        # time.sleep(1) 

        # api.turn_by_angle(servo_1, -180, 300)
        # time.sleep(1) 


        # api.turn_by_pulse(servo_4, 1600)
        # time.sleep(1) 
        # api.turn_by_angle(servo_4, 90, 200)
        # time.sleep(1) 
        # api.turn_by_angle(servo_4, -180, 300)
        # time.sleep(1) 


        # api.turn_by_pulse(servo_5, 1600)
        # time.sleep(1) 
        # api.turn_by_angle(servo_5, 90, 200)
        # time.sleep(1) 
        # api.turn_by_angle(servo_5, -180, 300)
        # time.sleep(1) 

#        print("servo_1 angle: " + str(api.get_angle(servo_1)))
        # print("servo_4 angle: " + str(api.get_angle(servo_4)))
        # print("servo_5 angle: " + str(api.get_angle(servo_5)))

        api.cleanup_servo(servo_1)
        api.cleanup_servo(servo_4)
        api.cleanup_servo(servo_5)
        api.cleanup_led(led)
        api.cleanup_final()

        print("Success")

    except Exception as e:
        print("Class RiApi Error:", str(e))
        sys.exit(2)

if __name__ == "__main__":
    main()