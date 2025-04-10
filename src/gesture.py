from enum import Enum

class GestureType(Enum):
    NONE = "none"
    DRAW = "draw"       # index + thumb pinch
    ERASE = "erase"     # open palm 
    SELECT = "select"   # index pointing
    CLEAR = "clear"     # fist with thumb out 

class GestureRecogniser:
    def __init__(self):
        self.pinch_threshold = 30
        self.current_gesture = GestureType.NONE

    def recognise_gesture(self, landmark_list):
        if not landmark_list:
            return GestureType.NONE
        
        landmarks = dict([(id, (x, y)) for id, x, y in landmark_list])

        thumb_tip = landmarks.get(4)
        index_tip = landmarks.get(8)
        middle_tip = landmarks.get(12)
        ring_tip = landmarks.get(16)
        pinky_tip = landmarks.get(20)

        thumb_base = landmarks.get(2)
        index_base = landmarks.get(5)
        middle_base = landmarks.get(9)
        ring_base = landmarks.get(13)
        pinky_base = landmarks.get(17)

        if not all([thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip, thumb_base, index_base, middle_base, ring_base, pinky_base]):
            return GestureType.NONE
        
        # check for draw gesture
        pinch_distance = self._calculate_distance(thumb_tip, index_tip)
        if pinch_distance < self.pinch_threshold:
            return GestureType.DRAW
        
        # check for erase gesture
        fingers_extended = self._check_fingers_extended(landmarks)
        if all(fingers_extended):
            return GestureType.ERASE
        
        # check for select gesture 
        if (fingers_extended[1] and not any(fingers_extended[1:])):
            return GestureType.SELECT
        
        # check for clear gesture
        if (fingers_extended[0] and not any(fingers_extended[1:])):
            return GestureType.CLEAR
        
        return GestureType.NONE

    def _calculate_distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    
    def _check_fingers_extended(self, landmarks):
        thumb_extended = landmarks[4][0] > landmarks[3][0]

        fingers = []
        for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
            finger_extended = landmarks[tip][1] < landmarks[pip[1]]
            fingers.append(finger_extended)

        return [thumb_extended] + fingers
    


        
        