import math

def calcDistance(pi: list, pf: list) -> float:
    """
    Calculates the distance between two points
    >>>calcDistance(1,5,1,5)
    5.656854249492381
    >>>calcDistance(5,1,5,1)
    5.656854249492381
    >>>calcDistance(6,9,6,9)
    0.0

    Author(s): Romy I. Chu III
    """
    return ((pf[0]-pi[0])**2 + (pf[1]-pi[1])**2)**0.5   # Return the distance between the two given points

def roundTo(num: float, base: float) -> float:
    """
    Returns a number rounded to the nearest 'base'
    >>>roundTo(1232, 10)
    1230
    >>>roundTo(5428, 3)
    5427
    >>>roundTo(10946.94637, 1.8)
    10945.800000000001

    Author(s): Romy I. Chu III
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

    Author(s): Romy I. Chu III
    """
    # If the total distance traveled is greater than twice the length of the arm segments
    # return angles of 180 (both segments straight)
    if distance > (armLength * 2):
        return (0,180)
    if distance <= 0:
        return (90,0)
    
    # Calculate the angle of arm's shoulder
    servoShoulderAngle = math.acos( (distance**2) / (2*armLength*distance) ) *180/math.pi
    # Calculate the angle of the arm's elbow
    #servoElbowAngle = math.acos( (armLength**2 + distance**2 - armLength**2) / (2*armLength*distance) ) *180/math.pi
    servoElbowAngle = 180 - servoShoulderAngle * 2
    return (int(servoShoulderAngle), int(servoElbowAngle))

def getBaseAngle(scrRes, pointCoords):
    """
    Calculates the angle of the base plate of the robot arm.
    This is assuming that straight forward is 0 degrees.
    >>>getBaseAngle(320, 480, 0, 0)
    -33.690067525979785
    >>>getBaseAngle(320, 480, 640, 0)
    33.690067525979785
    >>>getBaseAngle(320, 480, 320, 0)
    0.0
    >>>getBaseAngle(320, 480, 320, 480)
    0

    Author(s): Romy I. Chu III
    """
    # Normalize the values values so that the calclations are centered on 
    # center x (cx) and center y (cy) (center -> 0,0)
    normPX = pointCoords[0] - scrRes[0]/2
    normPY = scrRes[1] - pointCoords[1]
    angle = roundTo(math.atan2(normPX, normPY))

    # Limiting the output angle to +- 90 degrees
    if angle < -90:
        return -90
    if angle > 90:
        return 90
    return  angle