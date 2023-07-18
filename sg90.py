
import sys
import time
from ctypes import *
from riapi import RiApi

def main():
    try:
        servo_1 = c_int() 

        api = RiApi(c_bool(False))
        api.init()

        servo_1 = api.add_custom_servo(2350, 365, 200, 180, 0)

        print("\nSG90 поворот в крайние положения")

        api.rotate(servo_1, 0, 200) # 2320 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229

        api.rotate(servo_1, 1, 200) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114


        print("\nSG90 управление через длительность импульсов")

        api.turn_by_pulse(servo_1, 2350) # 2550 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229 (custom 207)

        api.turn_by_pulse(servo_1, 365) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0
        
        api.turn_by_pulse(servo_1, 1360) # 1430 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114 (custom 103)
        
   
        print("\nSG90 Минимальный шаг")

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114


        api.rotate_min_step(servo_1, 1, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.rotate_min_step(servo_1, 0, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))


        print("\nSG90 управление через Duty")

        api.turn_by_duty(servo_1, 75)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_duty(servo_1, 278)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_duty(servo_1, 481)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

     
        print("\nSG90 поворот на заданный угол")

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114

        api.turn_by_angle(servo_1, 90, 200)
        time.sleep(1) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_angle(servo_1, -90, 200)
        time.sleep(1) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.cleanup_servo(servo_1)
        api.cleanup_final()

    except Exception as e:
        print("Class RiApi Error:", str(e))
        sys.exit(2)

if __name__ == "__main__":
    main()