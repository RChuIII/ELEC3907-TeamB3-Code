"""
    Python Hand Tracking Program
    Created for : ELEC 3907: Engineering Project (Robotic Arm Project)
    Created by : Romy I. Chu III (101190001)
    Lasted Edited on : January 22, 2023

    This program uses the OpenCV and MediaPipe libraries to track the movements of a hand
    and extract their XY coordinates 
"""

import cv2              # Python OpenCV library, does the raw capture from the webcam
import mediapipe as mp  # Python MediaPipe library, does most of the processing for tracking
#from datetime import datetime # Performance Testing... (REMOVE FROM FINAL CODE)

mp_drawing = mp.solutions.drawing_utils             # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_drawing_styles = mp.solutions.drawing_styles     # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_hands = mp.solutions.hands                       # Used for all of the hand tracking data

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

def roundTo(num: float, base: int) -> int:
    """
    Really cool comments
    """
    return base * round(num//base)

cam_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

with mp_hands.Hands(max_num_hands=1) as hands:
    while cam_capture.isOpened():
        success, img = cam_capture.read()
        if success:
            img.flags.writeable = False                 # Pass the image by reference (to improve performance)
            # MediaPipe works with RGB, whereas OpenCV uses BGR, so we need to change colour modes
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change the colour mode to RGB from BGR
            results = hands.process(img)                # Get MediaPipe to process the image and try to find a hand
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Change back to BGR mode
            if results.multi_hand_landmarks:    # If there were hand landmarks found...
                for hand_landmarks in results.multi_hand_landmarks:                             # For each landmark...
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)   # Draw the landmarks and connection
        
        
        
        
            cv2.imshow("Webcam", img)   # Show the image
        if cv2.waitKey(3) & 0xFF == ord('q'): # Break from the loop when the 'q' key is pressed (after 3 seconds)
            break
    