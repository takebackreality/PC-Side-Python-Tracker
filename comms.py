import serial
import time
from config import COM_PORT, BAUD_RATE

class SerialComms:
    def __init__(self):
        self.ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  
        print("Connected to Arduino on", COM_PORT)

    def send(self, command: str):
        cmd = (command.strip() + "\n").encode("utf-8")
        self.ser.write(cmd)
