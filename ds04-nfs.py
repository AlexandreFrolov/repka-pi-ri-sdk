import sys
import time
from ctypes import *
from riapi import RiApi

def main():
    try:
        rservo = c_int() 

    #    api = RiApi(c_bool(False))
        api = RiApi(c_bool(True))
        api.init()

#        api.add_rotate_servo(rservo, "mg996r", 0)
        rservo = api.add_custom_rotate_servo(1050, 2100, 1050, 2100, 0)

        api.rotate_by_pulse(rservo, 1050) # 1000
        time.sleep(3) 

        api.rotate_by_pulse(rservo, 2100) # 2000
        time.sleep(3) 

        api.rotate_by_pulse(rservo, 1570) # 1500
        time.sleep(3) 

        api.stop_rservo(rservo)

        api.cleanup_servo(rservo)
        api.cleanup_final()

    except Exception as e:
        print("Class RiApi Error:", str(e))
        sys.exit(2)

if __name__ == "__main__":
    main()