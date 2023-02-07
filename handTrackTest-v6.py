"""
    Python Hand Tracking Program v.
    Created for : ELEC 3907: Engineering Project (Robotic Arm Project)
    Created by : Romy I. Chu III (101190001)
    Lasted Edited on : January 26, 2023

    This program uses the OpenCV and MediaPipe libraries to track the movements of a hand
    and extract their XYZ coordinates 
"""

import cv2              # Python OpenCV library, does the raw capture from the webcam
import mediapipe as mp  # Python MediaPipe library, does most of the processing for tracking
import math
from datetime import datetime # Performance Testing... (REMOVE FROM FINAL CODE) beep boop
import socket # TESTING beep boop
import serial
import struct


mp_drawing = mp.solutions.drawing_utils             # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_drawing_styles = mp.solutions.drawing_styles     # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_hands = mp.solutions.hands                       # Used for all of the hand tracking data
serialCon = serial.Serial(port='COM3', baudrate=9600, timeout=None)

# Dictionary of all the landmark points from the MediaPipe library
hand_points = {
    0 : mp_hands.HandLandmark.WRIST,
    1 : mp_hands.HandLandmark.THUMB_CMC,
    2 : mp_hands.HandLandmark.THUMB_MCP,
    3 : mp_hands.HandLandmark.THUMB_IP,
    4 : mp_hands.HandLandmark.THUMB_TIP,
    5 : mp_hands.HandLandmark.INDEX_FINGER_MCP,
    6 : mp_hands.HandLandmark.INDEX_FINGER_PIP,
    7 : mp_hands.HandLandmark.INDEX_FINGER_DIP,
    8 : mp_hands.HandLandmark.INDEX_FINGER_TIP,
    9 : mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
    10 : mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
    11 : mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
    12 : mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
    13 : mp_hands.HandLandmark.RING_FINGER_MCP,
    14 : mp_hands.HandLandmark.RING_FINGER_PIP,
    15 : mp_hands.HandLandmark.RING_FINGER_DIP,
    16 : mp_hands.HandLandmark.RING_FINGER_TIP,
    17 : mp_hands.HandLandmark.PINKY_MCP,
    18 : mp_hands.HandLandmark.PINKY_PIP,
    19 : mp_hands.HandLandmark.PINKY_DIP,
    20 : mp_hands.HandLandmark.PINKY_TIP,
}

def getCoords(point: int, image_res: tuple) -> list:
    """
    Returns the XY coordinates of a specific tracking point.
    >>>getCoords(0, img.shape)
    [501.33323669433594, 336.0984420776367]
    >>>getCoords(20, img.shape)
    [135.6822395324707, 338.8007354736328]
    >>>getCoords(11, img.shape)
    [146.05748176574707, 443.34471702575684]

    Author(s): Romy I. Chu III
    """
    # Create an array of the XY coords of the given tracking point
    coords = [hand_landmarks.landmark[hand_points[point]].x, hand_landmarks.landmark[hand_points[point]].y]
    coords[0] *= image_res[1]   # Scale the coordinate to the capture resolution
    coords[1] *= image_res[0]   # Scale the coordinate to the capture resolution
    return coords               # Return the scaled coordinates

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
    if distance >= (armLength * 2):
        return (180,180)
    if distance <=0:
        return (0,0)
    
    # Calculate the angle of arm's shoulder
    servoShoulderAngle = math.acos( (armLength**2 + distance**2 - armLength**2) / (2*armLength*distance) ) *180/math.pi
    # Calculate the angle of the arm's elbow
    #servoElbowAngle = math.acos( (armLength**2 + distance**2 - armLength**2) / (2*armLength*distance) ) *180/math.pi
    servoElbowAngle = 180 - servoShoulderAngle * 2
    return (int(servoShoulderAngle), int(servoElbowAngle))

def getBaseAngle(cx: int, cy: int,  px: int, py: int):
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
    cyn = 480 - cy
    pyn = 480 - py 
    cxn = cx - 320 
    pxn = px - 320 
    angle = math.atan2((cxn + pxn), (cyn + pyn))*180/math.pi

    # Limiting the output angle to +- 90 degrees
    if angle < -90:
        return -90
    if angle > 90:
        return 90
    return  angle

# Capture the video from the default camera device
cam_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# Sets the video capture resolution
# Can capture at 1920x1080, but at the cost of performance
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Tell OpenCV to use compression (MJPG) and not raw video (YUYV)
cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

# Set the parameters for the tracking:
#   - We only want to track one hand!
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while cam_capture.isOpened():           # If the camera is still ON, keep the program running.
        then = datetime.now()
        success, img = cam_capture.read()   # Capture an image from the video feed "cam_capture"

        if success:     # If a frame was captured successfully, continue, otherwise pass
            img.flags.writeable = False                 # Pass the image by reference (to improve performance)
            img = cv2.flip(img, 1)
            # MediaPipe works with RGB, whereas OpenCV uses BGR, so we need to change colour modes
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change the colour mode to RGB from BGR
            results = hands.process(img)                # Get MediaPipe to process the image and try to find a hand
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Change back to BGR mode
            

            if results.multi_hand_landmarks:    # If there were hand landmarks found...
                for hand_landmarks in results.multi_hand_landmarks:                             # For each landmark...
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)   # Draw the landmarks and connection beep boop
                    
                # The MediaPipe library places landmarks on the hand,
                # to calculate the depth of the hand, we can take two of the points 
                # and find the distance between them. The smaller the distance between the
                # two points, the further away the hand is.
                dispHeight, dispWidth = img.shape[0], img.shape[1]
                wristCoords = getCoords(0, img.shape)   # Get the raw coordinates of the wrist point
                
                depth = calcDistance(getCoords(5, (dispHeight, dispWidth)), getCoords(17, (dispHeight, dispWidth))) # Calculate the how far away the hand is from the camera.
                normX = roundTo(wristCoords[0], 2)      # Rounded X-coordinate (down to the nearest 2)
                normY = roundTo(wristCoords[1], 2)      # Rounded Y-coordinate (down to the nearest 2)
                normZ = roundTo(depth, 2)               # Rounded Z-coordinate (down to the nearest 2)

                jointAngles = getJointAngles(10, calcDistance([dispWidth//2, dispHeight], [normX, normY])//20)
                baseAngle = getBaseAngle(dispWidth//2, dispHeight, normX, normY)
                claw = calcDistance(getCoords(4, (dispHeight, dispWidth)), getCoords(8, (dispHeight, dispWidth))) # ~ 50

                #data = [jointAngles[0], jointAngles[1], round(roundTo(baseAngle,1.8),1)]
                data = [jointAngles[0], jointAngles[1]]
                print(data)
                #sock.sendto(str.encode(str(data)), serverAddressPort)
                serialCon.write(struct.pack("f",baseAngle))
                img = cv2.line(img, (dispWidth//2, dispHeight), (normX, normY), (0, 0, 255), 4) # Draw the line... beep boop this is for testing beep boop
            cv2.imshow("Webcam", img)   # Show the image     beep boop
            #print(datetime.now() - then)

        if cv2.waitKey(3) & 0xFF == ord('q'): # Break from the loop when the 'q' key is pressed (after 3 seconds)
            break
    

# Close all OpenCV windows
cam_capture.release()
cv2.destroyAllWindows()
# -------------------- EOF Reached -------------------- #




"""
Collision Sensors... Prevent armfrom bumping into stuff.

Pressure feedback

Claw that senses if there is an object is in front of it and blasts you with LED or buzzers

LCD screen that shows stuff

Sacrifice strength for prescision
"""