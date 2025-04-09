import mediapipe as mp 
import cv2
from config import *

class HandTracker:
    def __init__(self):
        # initialise mediapipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands = MAX_HANDS,
            min_detection_confidence = MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence = MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        # convert bgr to rgb
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the frame
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

        return frame 
    
    def get_hand_position(self, frame, hand_number=0):
        landmark_list = []

        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > hand_number:
                hand = self.results.multi_hand_landmarks[hand_number]
                for id, landmark in enumerate(hand.landmark):
                    height, width, _ = frame.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    landmark_list.append((id, cx, cy))

        return landmark_list