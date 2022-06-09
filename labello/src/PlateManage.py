import serial
import time
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

    @classmethod
    def init_plate(cls):
        cls.arduino = serial.Serial(port=cls.tty, baudrate=cls.baud_rate, timeout=1)

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
        """" check if arduino respond
        return boolean """
        cls.arduino.write(bytes('CHECK', 'utf-8'))
        time.sleep(0.5)
        data = cls.arduino.readline().decode("utf-8")[:-2]
        if (data == "CKECK:DONE"):
            return True
        return False




