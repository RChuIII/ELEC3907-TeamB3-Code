import serial
import time

bt = serial.Serial(port='COM6', baudrate=9600, timeout=None)

while True:
    out = bt.read_until(size=25)
    if out == None:
        print("fuck you, you messed up big time")
    print(out)
