import cv2
import numpy as np
from config import *
from hand_tracker import HandTracker

def initialise_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
    
    return cap

def main():
    cap = initialise_camera()
    tracker = HandTracker()

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

        index_finger = tracker.get_finger_position(frame, 8)

        fingers_up = tracker.get_finger_up_status(frame)

        if index_finger:
            cv2.circle(frame, index_finger, 10, (0, 255, 0), cv2.FILLED)
        
            finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            y_pos = 30
            for finger, is_up in zip(finger_names, fingers_up):
                status = "Up" if is_up else "Down"
                cv2.putText(frame, f"{finger}: {status}", (10, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                y_pos += 30

        cv2.imshow('AirCanvas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()