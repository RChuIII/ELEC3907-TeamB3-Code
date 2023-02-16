import cv2              # Python OpenCV library, does the raw capture from the webcam
import clr
import mediapipe as mp  # Python MediaPipe library, does most of the processing for tracking
from datetime import datetime # Performance Testing... (REMOVE FROM FINAL CODE) beep boop

clr.AddReference("RoboArmCalculations")
from RoboArmCalculations import RACalc
calc = RACalc()

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

    Author(s): Romy I. Chu III
    """
    # Create an array of the XY coords of the given tracking point
    coords = [hand_landmarks.landmark[hand_points[point]].x, hand_landmarks.landmark[hand_points[point]].y]
    coords[0] *= image_res[1]   # Scale the coordinate to the capture resolution
    coords[1] *= image_res[0]   # Scale the coordinate to the capture resolution
    return coords               # Return the scaled coordinates


cam_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)                         # Capture the video from the default camera device
cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))   # Tell OpenCV to use compression (MJPG) and not raw video (YUYV)

# Sets the video capture resolution
# Can capture at 1920x1080, but at the cost of performance
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Set the parameters for the tracking:
#   - We only want to track one hand!
# Increase detection and tracking confidence to prevent the tracking of something other than a hand.
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while cam_capture.isOpened():           # If the camera is still ON, keep the program running.
        then = datetime.now()
        success, img = cam_capture.read()   # Capture an image from the video feed "cam_capture"

        if success:     # If a frame was captured successfully, continue, otherwise pass
            img.flags.writeable = False                 # Pass the image by reference (to improve performance)
            img = cv2.flip(img, 1)                      # Flips image on the vertical axis (mirror sideways)
            # MediaPipe works with RGB, whereas OpenCV uses BGR, so we need to change colour modes
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change the colour mode to RGB from BGR
            results = hands.process(img)                # Get MediaPipe to process the image and try to find a hand
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Change back to BGR mode

            if results.multi_hand_landmarks:    # If there were hand landmarks found...
                hand_landmarks = results.multi_hand_landmarks[0]
                dispHeight, dispWidth = img.shape[0], img.shape[1]
                wristCoords = getCoords(0, img.shape)   # Get the raw coordinates of the wrist point
                
                #depth = calc.calcDistance(getCoords(5, (dispHeight, dispWidth)), getCoords(17, (dispHeight, dispWidth))) # Calculate the how far away the hand is from the camera.
                normX = calc.roundTo(wristCoords[0], 2)      # Rounded X-coordinate (down to the nearest 2)
                normY = calc.roundTo(wristCoords[1], 2)      # Rounded Y-coordinate (down to the nearest 2)
                #normZ = calc.roundTo(depth, 2)               # Rounded Z-coordinate (down to the nearest 2)

                jointAngles = calc.calculateJointAngles(10, calc.calcDistance(dispWidth//2, dispHeight, normX, normY)//20)
                #baseAngle = calc.calculateBaseAngle(dispWidth/2, float(dispHeight), float(normX), float(normY))
                #claw = calc.calcDistance(getCoords(4, (dispHeight, dispWidth)), getCoords(8, (dispHeight, dispWidth))) # ~ 50
                data = [jointAngles.Item1, jointAngles.Item2]
                print(data)
            #print(datetime.now() - then)
            cv2.imshow("Webcam", img)   # Show the image     beep boop
        if cv2.waitKey(3) & 0xFF == ord('q'): # Break from the loop when the 'q' key is pressed (after 3 seconds)
            break
# Close all OpenCV windows
cam_capture.release()
cv2.destroyAllWindows()
# -------------------- EOF Reached -------------------- #