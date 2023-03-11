import servoCalculations as scalc


#print(scalc.calculate_2Joint_6DoF([10,0,4]))
#print(scalc.calculate_2Joint_6DoF([10,10,2]))
#print(scalc.calculate_2Joint_6DoF([10,17.32051,3]))
#print(scalc.calculate_2Joint_6DoF([17.32051,10,0]))
#
#print(scalc.calculate_2Joint_6DoF([20,0,0]))
#print(scalc.calculate_2Joint_6DoF([17.32051,0,0]))
#print(scalc.calculate_2Joint_6DoF([10,0,4]))


someList = [10,9,8,7,6,4,2,1,3,11]


def bubble_sort(arr):
    for i in range(9):
        for j in range(9):
            if arr[j + 1] < arr[j]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

bubble_sort(someList)

print(someList)