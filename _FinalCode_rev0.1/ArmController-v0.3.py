import serial
from robotArm import RobotArm
import math
 # units in mm
 # Max X = 300 mm
 # Max input = 8
 # increment = 0.027
roboArm = RobotArm(135,180,120,165)

bt_com = serial.Serial("COM6", 9600)

# data = [accel_x, accel_y, mode_select, claw_act, claw_rot]
data = [0,0,0,0,0]
pos = [0,0,0]

angle_old = [0,0,0]
angle_cur = [0,0,0]
wrist_angle = 150
    
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
        
        
        print(check_params(data[2], data[3], data[4]))
        print()
        #check_params(data[2], data[3], data[4])

def check_params(mode_select, claw_act, claw_rot):
    global angle_cur, angle_old, wrist_angle
    out = [0, # Base - 0
            0, # Shoulder - 1
            0, # Elbow - 2
            0, # Wrist angle - 3
            0, # Wrist Rotation, - 4
            0 # Claw actuation - 5
            ]

    if (mode_select != 0.0):
        pos[2] = clamp(pos[2] - data[0], 0, 590)
        wrist_angle = clamp(servo_angle2PWM((data[1] + 8) * 6.875), 150, 420)
    else:
        pos[0] = clamp(pos[0] + data[0], 90, 280)
        pos[1] = clamp(pos[1] - data[1], -180, 180)

    if (claw_rot != 0.0):
        out[4] = servo_angle2PWM(0)
    else:
        out[4] = servo_angle2PWM(90)
        
    
    if (claw_act != 0.0):
        out[5] = servo_angle2PWM(90)
    else:
        out[5] = servo_angle2PWM(0)

    distance = math.sqrt(math.pow(pos[0], 2) + math.pow((pos[2] - 135), 2))
    if distance < 300:
        temp = roboArm.get_joint_angles(pos)
        out[0] = temp[0]
        out[1] = temp[1]
        out[2] = temp[2]

        angle_cur = [out[0], out[1], out[2]]
        out[0] = (angle_cur[0] / 1.8) - (angle_old[0] / 1.8)  #

        angle_old = angle_cur
        out[1] = servo_angle2PWM(clamp(out[1], 0, 90))
        out[2] = servo_angle2PWM(clamp(out[2], 0, 140))
        out[3] = wrist_angle
    else:
        out[0] = (angle_cur[0] / 1.8) - (angle_old[0] / 1.8)  
        out[1] = servo_angle2PWM(clamp(angle_old[1], 0, 90))
        out[2] = servo_angle2PWM(clamp(angle_old[2], 0, 90))
        out[3] = wrist_angle
    print(pos)
    return out

def servo_angle2PWM(servo_angle):
    return (2.5 * math.fabs(servo_angle)) + 150

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

initializaion()
loop()

