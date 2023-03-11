import math

# [BaseHeight, armBicep, armForearm, armWristLength]
_armSpecifications = [0, 10, 10, 10]

def _calculateDistance(initialPos: list, finalPos: list) -> float:
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
    return 0

def _roundTo(num: float, base: float) -> float:
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

def _roundTo_list(nums: list, base: float) -> list:
    """
    >>> roundTo_list([1.4, 1, 5, 6.34, 12.543, 1209.120, 0.88], 1.8)
    [0.0, 0.0, 3.6, 5.4, 10.8, 1207.8, 0.0]
    >>> roundTo_list([1.4, 1, 5, 6.34, 12.543, 1209.120, 0.88], 2.5)
    [0.0, 0.0, 5.0, 5.0, 12.5, 1207.5, 0.0]
    >>> roundTo_list([1.4, 1, 5, 6.34, 12.543, 1209.120, 0.88], 10)
    [0, 0, 0, 0, 10, 1200, 0]
    >>> roundTo_list([1.4, 1, 5, 6.34, 12.543, 1209.120, 0.88], 1)
    [1, 1, 5, 6, 12, 1209, 0]
    """
    roundedList = [(base * round(num//base)) for num in nums]
    return roundedList

def _rad2deg(angle: float):
    deg = angle * 180 / math.pi
    return deg

def calculate_2Joint_6DoF(finalPosition: list ) -> list:
    length_bicep_sqrd = math.pow( _armSpecifications[1], 2)
    length_forearm_sqrd = math.pow( _armSpecifications[2], 2)
    r = math.sqrt(math.pow(finalPosition[0], 2) + math.pow((finalPosition[2] - _armSpecifications[0]), 2))
    r_sqrd = math.pow(r, 2)

    phi1 = math.atan2((finalPosition[2] - _armSpecifications[0]), finalPosition[0])
    phi2 = math.acos( (length_bicep_sqrd + r_sqrd - length_forearm_sqrd) / (2 * _armSpecifications[1] * r) )    
    phi3 = math.acos( (length_bicep_sqrd + length_forearm_sqrd - r_sqrd) / (2 * _armSpecifications[1] * _armSpecifications[2]))

    stepperBaseAngle = math.atan2( finalPosition[1], finalPosition[0] )
    servoShoulderAngle = phi2 + phi1
    servoElbowAngle = phi3 - math.pi

    roundedAngleList = _roundTo_list([_rad2deg(servoShoulderAngle), _rad2deg(servoElbowAngle)], 1)
    roundedBaseAngle = [_roundTo(_rad2deg(stepperBaseAngle), 1.8)]

    return roundedBaseAngle + roundedAngleList
    