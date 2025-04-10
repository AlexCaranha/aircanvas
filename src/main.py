import cv2
import numpy as np
from config import *
from hand_tracker import HandTracker
from gesture import GestureRecogniser, GestureType

def initialise_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

    return cap

def main():
    cap = initialise_camera()
    tracker = HandTracker()
    gesture_recogniser = GestureRecogniser()

    # create a blank canvas for drawing
    canvas = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to get frame from camera")
            break
    
        # flip frame if enabled because i look ugly mirrored
        if FLIP_CAMERA:
            frame = cv2.flip(frame, 1)

        # find and draw hands
        frame = tracker.find_hands(frame)
        landmark_list = tracker.get_hand_position(frame)

        # recognise gesture
        gesture = gesture_recogniser.recognise_gesture(landmark_list)

        # display gesture info
        cv2.putText(frame, f"Gesture: {gesture.value}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        index_finger = tracker.get_finger_position(frame, 8)
        if index_finger:
            # Draw circle at finger position with color based on gesture
            color = {
                GestureType.DRAW: (0, 255, 0),    # Green
                GestureType.ERASE: (0, 0, 255),   # Red
                GestureType.SELECT: (255, 0, 0),  # Blue
                GestureType.CLEAR: (0, 255, 255), # Yellow
                GestureType.NONE: (128, 128, 128) # Gray
            }[gesture]
            
            cv2.circle(frame, index_finger, 10, color, cv2.FILLED)

        cv2.imshow('AirCanvas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()