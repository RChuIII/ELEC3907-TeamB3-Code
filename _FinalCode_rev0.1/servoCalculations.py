import math


_baseHeight = -1
_armSegment1 = -1 # Bicep
_armSegment2 = -1 # Forearm
_armSegment3 = -1 # wrist length

_armSpecifications = [_baseHeight, _armSegment1, _armSegment2, _armSegment3]

def calculateDistance(initialPos: list, finalPos: list) -> float:
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

def roundTo_list(nums: list, base: float) -> list:
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

def _calculate_2Joint_6DoF(finalPosition: list ) -> list:
    length_bicep_sqrd = math.pow( _armSpecifications[1], 2)
    length_forearm_sqrd = math.pow( _armSpecifications[2], 2)
    r = math.sqrt(math.pow(finalPosition[0], 2) + math.pow((finalPosition[2] - _armSpecifications[0]), 2))
    r_sqrd = math.pow(r, 2)

    phi1 = math.atan2((finalPosition[2] - _armSpecifications[0]), finalPosition[0])
    phi2 = math.acos( (length_bicep_sqrd + r_sqrd - length_forearm_sqrd) / (2 * _armSpecifications[1] * r) )    
    phi3 = math.acos( (length_bicep_sqrd + length_forearm_sqrd - r_sqrd) / (2 * _armSpecifications[1] * _armSpecifications[2]))

    stepperBaseAngle = math.atan2( finalPosition[1], finalPosition[0] )
    servoShoulderAngle = phi1 - phi2
    servoElbowAngle = math.pi - phi3

    roundedAngleList = roundTo_list([servoShoulderAngle, servoElbowAngle], 0.5)
    roundedBaseAngle = [roundTo(stepperBaseAngle, 1.8)]

    return roundedBaseAngle + roundedAngleList