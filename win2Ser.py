import serial

serialCon = serial.Serial(port='COM', baudrate=9600, bytesize=8, timeout=None)

while True:
    serialCon.write("190")