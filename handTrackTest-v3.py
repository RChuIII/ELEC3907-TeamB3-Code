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

# Capture the video from the default camera device
cam_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# Sets the video capture resolution
# Can capture at 1920x1080, but at the cost of performance
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Tell OpenCV to use compression (MJPG) and not raw video (YUYV)
cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# Set the parameters for the tracking:
#   - We only want to track one hand!
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while cam_capture.isOpened():           # If the camera is still ON, keep the program running.
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
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)   # Draw the landmarks and connection
                    
                # The MediaPipe library places landmarks on the hand,
                # to calculate the depth of the hand, we can take two of the points 
                # and find the distance between them. The smaller the distance between the
                # two points, the further away the hand is.
                dispHeight, dispWidth = img.shape[0], img.shape[1]
                depth = calcDistance(getCoords(5, (dispHeight, dispWidth)), getCoords(17, (dispHeight, dispWidth))) # Calculate the how far away the hand is from the camera.
                wristCoords = getCoords(0, img.shape)   # Get the raw coordinates of the wrist point
                normX = roundTo(wristCoords[0], 2)      # Rounded X-coordinate (down to the nearest 2)
                normY = roundTo(wristCoords[1], 2)      # Rounded Y-coordinate (down to the nearest 2)
                normZ = roundTo(depth, 2)               # Rounded Z-coordinate (down to the nearest 2)
                out = ( "x = " + str(normX) + "\n" +
                        "y = " + str(normY) + "\n" +
                        "z = " + str(normZ) + "\n"
                )
                img = cv2.line(img, (dispWidth//2, dispHeight), (normX, normY), (0, 0, 255), 4) # Draw the line... beep boop this is for testing beep boop
                print(out)  # you should see this line of code. beep boop
            cv2.imshow("Webcam", img)   # Show the image
        if cv2.waitKey(3) & 0xFF == ord('q'): # Break from the loop when the 'q' key is pressed (after 3 seconds)
            break
    

# Close all OpenCV windows
cam_capture.release()
cv2.destroyAllWindows()

# -------------------- EOF Reached -------------------- #