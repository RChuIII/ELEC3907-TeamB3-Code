"""
Required Modules:
    //-> Write calibration code for accelerometer
    //-> Read Accelerometer data from bluetooth device
    //-> Clean up the maths code
    //-> write a better python main program.
    ->Thursday-> Integrate accelerometer and bluetooth moduels
    -> Accelerometer to maths(
"""

"""
Arm-Glove System
    -> Glove(arduino nano) sends signal via bluetooth
        -> Sent signals:
            -> [glove_XTilt, glove_YTilt, axis_mode, claw_acutation, claw_rotation]
            -> [analog, analog, digital, analog, digital]

    -> Raspberry PI recieves data
    -> Raspberry PI parses data
        -> Takes glove_XTilt, golve_YTilt, and axis_mode to calculate position
        -> Takes claw_rotation to determine if 0_deg or 90_deg rotation

    -> Raspberry PI sends data to arduino Mega
        -> [stepper_pos, servo_sh_pos, servo_el_pos, servo_wr_pos, servo_cr_pos, servo_cl_pos]
        -> Stepper position, shoulder position, elbow position, wrist position, claw rotation, claw grip

    -> Arduino Mega sends data to servo/stepper drivers
    
    -> Arduino mega sends feedback information
        -> proximity sensor stop signal
        -> claw proximity sensor (obj within claw grip)
"""

import serial
from robotArm import RobotArm
 # units in mm
 # Max X = 300 mm
 # Max input = 8
 # increment = 0.027
roboArm = RobotArm(135,180,120,165)

SCALING_FACTOR = 300/8

try:
    bt_com = serial.Serial(port='COM6', baudrate=9600)
    print(bt_com)
    print("Connected")
    #arduino_mega_com = serial.Serial(port='COMX', baudrate=9600, bytesize=8, timeout=None)
except Exception as e:
    raise e

# data = [accel_x, accel_y, mode_select, claw_act, claw_rot]
data = [0,0,0,0,0]
pos = [0,0,0]

angle_old = [0,0,0]
angle_cur = [0,0,0]
    
def initializaion():
    print("initializing...")
    global angle_old, data, pos
    pos = [233, 0, 135]
    angle_old = roboArm.get_joint_angles(pos)

def loop():
    print("starting loop...")
    global data
    while True:
        temp = bt_com.readline().decode()[:-1]
        temp_list = temp.split()
        data = [float(x) for x in temp_list]

        data[0] = clamp(data[0], -8, 8)
        data[1] = clamp(data[1], -8, 8)
        
        
        check_params(data[2], data[3], data[4])

def check_params(mode_select, claw_act, claw_rot):
    global angle_cur, angle_old
    out = [0, # Base - 0
            0, # Shoulder - 1
            0, # Elbow - 2
            0, # Wrist angle - 3
            0, # Wrist Rotation, - 4
            0 # Claw actuation - 5
            ]

    if (mode_select != 0.0):
        pos[2] = clamp(pos[2] + data[0], 1, 590)
        out[3] = clamp(servo_angle2PWM((data[1] + 8) * 6.875), 150, 420)
    else:
        pos[0] = clamp(pos[0] + data[0], 1, 465)
        pos[1] = clamp(pos[1] - data[1], 1, 465)

    if (claw_rot != 0.0):
        out[4] = servo_angle2PWM(0)
    else:
        out[4] = servo_angle2PWM(90)
        
    
    if (claw_act != 0.0):
        out[5] = servo_angle2PWM(0)
    else:
        out[5] = servo_angle2PWM(90)

    out[0:2] = roboArm.get_joint_angles(pos)

    angle_cur = out[0:2]
    # Divide base ANLGE by 1.8 to get the number of steps
    out[0] = (angle_cur[0] / 1.8) - (angle_old[0] / 1.8)  #

    angle_old = angle_cur

    out[1] = servo_angle2PWM(clamp(out[1], 0, 90))
    out[2] = servo_angle2PWM(clamp(out[2], 0, 140))
    return out

def servo_angle2PWM(servo_angle):
    return 2.5 * servo_angle + 150

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

initializaion()
loop()

