import serial
import time
import os.path
"""
Arduino communication 
I : init 
C : check
R-steps- :
D <- : Done  
"""
class PlateManage:

    tty = "/dev/ttyACM0"
    baud_rate = 9600
    numer_steps = 200
    arduino = None
    init = False

    @classmethod
    def init_plate(cls):
        if not os.path.isfile(cls.tty):
            PlateManage.init = False
            return
        cls.arduino = serial.Serial(port=cls.tty, baudrate=cls.baud_rate, timeout=1)
        PlateManage.init = True

    @classmethod
    def move_plate_steps(cls, steps):
        if not cls.get_status():
            return False
        msg = "ROT" + str(steps)
        cls.arduino.write(bytes(msg, 'utf-8'))
        time.sleep(0.155 * steps + 1)
        data = cls.arduino.readline().decode("utf-8")[:-2]
        if (data == "ROT" + str(steps)):
            return True
        return False

    @classmethod
    def get_status(cls):
        if PlateManage.init is False:
            return False
        """" check if arduino respond
        return boolean """
        cls.arduino.write(bytes('CHECK', 'utf-8'))
        time.sleep(0.5)
        data = cls.arduino.readline().decode("utf-8")[:-2]
        if (data == "CKECK:DONE"):
            return True
        return False




