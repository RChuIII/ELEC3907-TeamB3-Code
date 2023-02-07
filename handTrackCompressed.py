import cv2,math
import mediapipe as mp  # Python MediaPipe library, does most of the processing for tracking
from datetime import datetime # Performance Testing... (REMOVE FROM FINAL CODE) beep boop
mp_drawing = mp.solutions.drawing_utils             # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_drawing_styles = mp.solutions.drawing_styles     # Used to draw the landmarks (REMOVE FROM FINAL CODE)
mp_hands = mp.solutions.hands                       # Used for all of the hand tracking data
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
    20 : mp_hands.HandLandmark.PINKY_TIP, }
RAD2DEG = 180/math.pi
def getCoords(point: int, image_res: tuple) -> list:
    coords = [hand_landmarks.landmark[hand_points[point]].x, hand_landmarks.landmark[hand_points[point]].y]
    coords[0] *= image_res[1]   # Scale the coordinate to the capture resolution
    coords[1] *= image_res[0]   # Scale the coordinate to the capture resolution
    return coords               # Return the scaled coordinates
def calcDistance(pi: list, pf: list) -> float:
    return ((pf[0]-pi[0])**2 + (pf[1]-pi[1])**2)**0.5   # Return the distance between the two given points
def roundTo(num: float, base: float) -> float:
    return base * round(num//base)
def getJointAngles(armLength:int, distance: int) -> tuple:
    if distance >= (armLength * 2):
        return (0,180)
    if distance <=0:
        return (90,90)
    servoShoulderAngle = math.acos((distance**2) / (2*armLength*distance) ) * RAD2DEG
    return (int(servoShoulderAngle), int(180 - servoShoulderAngle * 2))
def getBaseAngle(cx: int, cy: int,  px: int, py: int):
    cxn, cyn = cx - 320, 480 - cy
    pxn, pyn = px - 320, 480 - py 
    angle = math.atan2((cxn + pxn), (cyn + pyn)) * RAD2DEG
    if angle < -90:
        return -90
    if angle > 90:
        return 90
    return  angle
cam_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while cam_capture.isOpened():           # If the camera is still ON, keep the program running.
        then = datetime.now()
        success, img = cam_capture.read()   # Capture an image from the video feed "cam_capture"
        if success:     # If a frame was captured successfully, continue, otherwise pass
            img.flags.writeable = False                 # Pass the image by reference (to improve performance)
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change the colour mode to RGB from BGR
            results = hands.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Change back to BGR mode
            if results.multi_hand_landmarks:    # If there were hand landmarks found...
                hand_landmarks = results.multi_hand_landmarks[0]
                dispHeight, dispWidth = img.shape[0], img.shape[1]
                wristCoords = getCoords(0, img.shape)   # Get the raw coordinates of the wrist point
                depth = calcDistance(getCoords(5, (dispHeight, dispWidth)), getCoords(17, (dispHeight, dispWidth))) # Calculate the how far away the hand is from the camera.
                normX, normY, normZ = roundTo(wristCoords[0], 2), roundTo(wristCoords[1], 2),roundTo(depth, 2)
                jointAngles = getJointAngles(10, calcDistance([dispWidth//2, dispHeight], [normX, normY])//20)
                baseAngle = getBaseAngle(dispWidth//2, dispHeight, normX, normY)
                claw = calcDistance(getCoords(4, (dispHeight, dispWidth)), getCoords(8, (dispHeight, dispWidth))) # ~ 50
                data = [baseAngle, jointAngles[0], jointAngles[1]]
                print(baseAngle)
        print(datetime.now() - then)
cam_capture.release()
cv2.destroyAllWindows()