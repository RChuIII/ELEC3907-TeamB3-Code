import math

class RobotArm:
    """Really cool docstring"""
    def __init__(self, baseHeight, bicepLength, forearmLength, wristLength):
        self.baseHeight = baseHeight
        self.bicepLength = bicepLength
        self.forearmLength = forearmLength
        self.wristLength = wristLength
        
    def __calculateDistance(self, initialPos: list, finalPos: list) -> float:
        """
        Calculates the distance between two points
        >>>calcDistance([1,5],[1,5])
        5.656854249492381
        >>>calcDistance([5,1],[5,1])
        5.656854249492381
        >>>calcDistance([6,9],[6,9])
        0.0

        Author(s): Romy I. Chu III
        """
        dist = math.sqrt( math.pow( finalPos[0] - initialPos[0], 2 ) + math.pow( finalPos[1] - initialPos[1], 2 ) )
        return dist
        
    def __roundTo(self, num: float, base: float) -> float:
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
    
    def __roundTo_list(self, nums: list, base: float) -> list:
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

    def __rad2deg(self, angle: float):
        deg = angle * 180 / math.pi
        return deg
    
    def get_joint_angles(self, finalPosition: list):
        length_bicep_sqrd = math.pow( self.bicepLength, 2)
        length_forearm_sqrd = math.pow( self.forearmLength, 2)
        r = math.sqrt(math.pow(finalPosition[0], 2) + math.pow((finalPosition[2] - self.baseHeight), 2))
        r_sqrd = math.pow(r, 2)

        phi1 = math.atan2((finalPosition[2] - self.baseHeight), finalPosition[0])
        phi2 = math.acos( (length_bicep_sqrd + r_sqrd - length_forearm_sqrd) / (2 * self.bicepLength * r) )    
        phi3 = math.acos( (length_bicep_sqrd + length_forearm_sqrd - r_sqrd) / (2 * self.bicepLength * self.wristLength))

        stepperBaseAngle = math.atan2( finalPosition[1], finalPosition[0] )
        servoShoulderAngle = phi2 + phi1
        servoElbowAngle = phi3 - math.pi

        roundedAngleList = [self.__roundTo(self.__rad2deg(servoShoulderAngle),1), self.__roundTo(self.__rad2deg(servoElbowAngle),1)]
        roundedBaseAngle = [self.__roundTo(self.__rad2deg(stepperBaseAngle), 1.8)]
        
        return roundedBaseAngle + roundedAngleList