
import sys
import time
from ctypes import *
from riapi import RiApi

def main():
    try:
        servo_1 = c_int() 

        api = RiApi(c_bool(False))
    #    api = RiApi(c_bool(True))
        api.init()
#        api.async_off()

        api.add_servo(servo_1, "mg90s", 0)


        print("\nMG90S поворот в крайние положения")

        api.rotate(servo_1, 0, 200) # 2320 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229

        api.rotate(servo_1, 1, 200) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114

        print("\nMG90S управление через длительность импульсов")

        api.turn_by_pulse(servo_1, 2650) # 2550 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 229 (custom 207)

        api.turn_by_pulse(servo_1, 365) # 330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 0
        
        api.turn_by_pulse(servo_1, 1500) # 1430 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114 (custom 103)
        

        print("\nMG90S Минимальный шаг")

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114


        api.rotate_min_step(servo_1, 1, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.rotate_min_step(servo_1, 0, 100)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        print("\nMG90S управление через Duty")

        api.turn_by_duty(servo_1, 75)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_duty(servo_1, 300)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_duty(servo_1, 540)
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

     
        print("\nMG90S поворот на заданный угол")

        api.set_middle(servo_1) # 1330 mc на осциллографе
        time.sleep(2) 
        print("servo_1 angle: " + str(api.get_angle(servo_1))) # угол 114

        api.turn_by_angle(servo_1, 90, 200)
        time.sleep(1) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.turn_by_angle(servo_1, -90, 300)
        time.sleep(1) 
        print("servo_1 angle: " + str(api.get_angle(servo_1)))

        api.cleanup_servo(servo_1)
        api.cleanup_final()

    except Exception as e:
        print("Class RiApi Error:", str(e))
        sys.exit(2)

if __name__ == "__main__":
    main()