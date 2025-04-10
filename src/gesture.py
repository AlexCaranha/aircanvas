from enum import Enum
import math

class GestureType(Enum):
    NONE = "none"
    DRAW = "draw"       # index + thumb pinch
    ERASE = "erase"     # open palm 
    SELECT = "select"   # index pointing
    CLEAR = "clear"     # fist with thumb out 

class GestureRecogniser:
    def __init__(self):
        self.pinch_threshold = 100
        self.current_gesture = GestureType.NONE

    def recognise_gesture(self, landmark_list):
        if not landmark_list:
            return GestureType.NONE
        
        landmarks = dict([(id, (x, y)) for id, x, y in landmark_list])

        fingers_extended = self._check_fingers_extended(landmarks)

        # calculate pinch distance
        pinch_distance = self._calculate_distance(
            landmarks[4],
            landmarks[8]
        )

        # debug info
        print(f"Pinch distance: {pinch_distance}")
        print(f"Fingers extended: {fingers_extended}")
        
        # check for draw gesture
        if pinch_distance < self.pinch_threshold:
            return GestureType.DRAW
        
        # check for erase gesture
        fingers_extended = self._check_fingers_extended(landmarks)
        if all(fingers_extended):
            return GestureType.ERASE
        
        # check for select gesture 
        if fingers_extended[1] and not any([fingers_extended[0], *fingers_extended[2:]]):
            return GestureType.SELECT
        
        # check for clear gesture
        if fingers_extended[0] and not any(fingers_extended[1:]):
            return GestureType.CLEAR
        
        return GestureType.NONE

    def _calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    def _check_fingers_extended(self, landmarks):
        # get palm center 
        palm_x = sum(landmarks[i][0] for i in [0, 5, 9, 13, 17]) / 5

        thumb_extended = landmarks[4][0] < palm_x

        # Other fingers - compare y positions
        fingers = []
        for tip, mid, base in [(8,6,5), (12,10,9), (16,14,13), (20,18,17)]:  # Index to Pinky
            finger_tip_y = landmarks[tip][1]
            finger_base_y = landmarks[base][1]
            finger_mid_y = landmarks[mid][1]

            # A finger is extended if its tip is higher (smaller y) than both its mid and base points
            finger_extended = finger_tip_y < finger_mid_y < finger_base_y
            fingers.append(finger_extended)

        return [thumb_extended] + fingers
    


        
        