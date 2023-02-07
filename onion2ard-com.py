import serial

ser = serial.Serial('/dev/ttyS1', 9600, timeout = None)

while True:
        input = ser.read()
        print(int(input))