import servoCalculations as scalc
from robotArm import RobotArm
import math


roboArm = RobotArm(135,180,120,165)
finalPosition = [100,100, 135]
#print(roboArm.get_joint_angles([0.0,-0.0, 135]))
#roboArm.get_joint_angles([75.0,-0.0, 135])
#roboArm.get_joint_angles([0.0,255, 135])
#roboArm.get_joint_angles([-75,-255, 135])
#roboArm.get_joint_angles([-300,-37.5, 135])
print(roboArm.get_joint_angles(finalPosition))


length_bicep_sqrd = math.pow( 180, 2)
length_forearm_sqrd = math.pow( 120, 2)
r = math.sqrt(math.pow(finalPosition[0], 2) + math.pow((finalPosition[2] - 135), 2))
r_sqrd = math.pow(r, 2)
#print(math.acos(length_bicep_sqrd + r_sqrd - length_forearm_sqrd) / (2 * 135 * r)


"""print(roboArm.get_joint_angles([10,0,4]))
print(scalc.calculate_2Joint_6DoF([10,0,4]))
print()
print(roboArm.get_joint_angles([10,10,2]))
print(scalc.calculate_2Joint_6DoF([10,10,2]))
print()
print(roboArm.get_joint_angles([10,17.32051,3]))
print(scalc.calculate_2Joint_6DoF([10,17.32051,3]))
print()
print(roboArm.get_joint_angles([17.32051,10,0]))
print(scalc.calculate_2Joint_6DoF([17.32051,10,0]))
print()
print(roboArm.get_joint_angles([20,0,0]))
print(scalc.calculate_2Joint_6DoF([20,0,0]))
print()
print(roboArm.get_joint_angles([17.32051,0,0]))
print(scalc.calculate_2Joint_6DoF([17.32051,0,0]))
print()
print(roboArm.get_joint_angles([10,0,4]))
print(scalc.calculate_2Joint_6DoF([10,0,4]))
print()
"""





"""someList = [10,9,8,7,6,4,2,1,3,11]


def bubble_sort(arr):
    for i in range(9):
        for j in range(9)
            if arr[j + 1] < arr[j]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

bubble_sort(someList)

print(someList)"""