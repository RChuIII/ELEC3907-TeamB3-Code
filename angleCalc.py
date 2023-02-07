"""
    Angle Calculation Program
    Created for : ELEC 3907: Engineering Project (Robotic Arm Project)
    Created by : Romy I. Chu III (101190001)
    Lasted Edited on : January 23, 2023

    This program will be used to calculate the required angles for 
    servo motors
"""
import math

def getAngles(distance: int) -> tuple:
    if distance > 20:
        return (0,0)
    
    servoShoulderAngle = math.acos( (10**2 + distance**2 - 10**2) / (2*10*distance) ) *180/math.pi
    servoElbowAngle = math.acos( (10**2 + distance**2 - 10**2) / (2*10*distance) ) *180/math.pi
    return (int(servoShoulderAngle), int(servoElbowAngle))


def getBaseAngles(cx: int, cy: int,  px: int, py: int):
    """
    Calculates the angle of the base plate of the robot arm.
    This is assuming that straight forward is 0 degrees.
    >>>getBaseAngles(320, 480, 0, 0)
    -33.690067525979785
    >>>getBaseAngles(320, 480, 640, 0)
    33.690067525979785
    >>>getBaseAngles(320, 480, 320, 0)
    0.0
    >>>getBaseAngles(320, 480, 320, 480)
    0
    """
    # Normalize the values values so that the calclations are centered on 
    # center x (cx) and center y (cy) (center -> 0,0)
    cyn = 480 - cy
    pyn = 480 - py 
    cxn = cx - 320 
    pxn = px - 320 
    # Nested if statements to prevent 0 division
    if cyn == pyn: # Check if the y-coordinates are the same...
        if pxn > cxn:       # If the pointx is greater than the center...
            return 90       #   The angle will always be 90 degrees
        elif pxn == cxn:    # If the point is the center...
            return 0        #   The angle is 0 degrees
        return -90          # If the pointx is smaller than the center...
                            #   The angle must be -90 degrees
    oa = (cxn + pxn) / (cyn + pyn)
    return math.atan(oa)*180/math.pi

def roundTo(num: float, base: float) -> int:
    """
    Really cool comments
    """
    return base * round(num//base)

def roundTo(num: float, base: float) -> float:
    """
    Returns a number rounded to the nearest 'base'
    >>>
    >>>
    """
    return base * round(num//base)

def getJointAngles(armLength:int, distance: int) -> tuple:
    """
    Calculates the required shoulder and elbow angles for a two segment arm,
    with segment lengths of 'armLength', to reach a distance of sideC.
    ALl SIDE LENGTHS MUST BE IN THE SAME UNITS
    >>>getJointAngles(10, 1)
    (87,87)
    >>>getJointAngles(10, 20)
    (0,0)
    >>>getJointAngles(10, 10*2**0.5)
    (45,45)
    >>>getJointAngles(10, 25)
    (0,0)
    """
    if distance > 20:
        return (0,0)
    servoShoulderAngle = math.acos( (armLength**2 + distance**2 - armLength**2) / (2*armLength*distance) ) *180/math.pi
    servoElbowAngle = math.acos( (armLength**2 + distance**2 - armLength**2) / (2*armLength*distance) ) *180/math.pi
    return (int(servoShoulderAngle), int(servoElbowAngle))







print(getAngles(1))
print(getAngles(5))
print(getAngles(10))
print(getAngles(15))
print(getAngles(20))
print(getAngles(10*2**0.5))
print(getAngles(25))
print()

x1 = getBaseAngles(320, 480, 0, 0)
print(x1)

x2 = getBaseAngles(320, 480, 640, 0)
print(x2)

x3 = getBaseAngles(320, 480, 320, 0)
print(x3)

x4 = getBaseAngles(320, 480, 320, 480)
print(x4)
print()


y1 = roundTo(1232, 10)
y2 = roundTo(5428, 3)
y3 = roundTo(10946.94637, 1.8)
print(y1)
print(y2)
print(y3)
print()

print(getJointAngles(10,1))
print(getJointAngles(10,5))
print(getJointAngles(10,10))
print(getJointAngles(10,15))
print(getJointAngles(10,20))
print(getJointAngles(10,10*2**0.5))
print(getJointAngles(10,25))
print()