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

        # Display gesture and debug info
        if landmark_list:
            # Draw gesture type
            cv2.putText(frame, f"Gesture: {gesture.value}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Draw pinch distance
            if len(landmark_list) > 8:
                thumb_tip = next((x, y) for id, x, y in landmark_list if id == 4)
                index_tip = next((x, y) for id, x, y in landmark_list if id == 8)
                
                # Draw line between thumb and index
                cv2.line(frame, thumb_tip, index_tip, (0, 255, 0), 2)
                
                # Calculate and display distance
                distance = int(gesture_recogniser._calculate_distance(thumb_tip, index_tip))
                mid_point = ((thumb_tip[0] + index_tip[0])//2, (thumb_tip[1] + index_tip[1])//2)
                cv2.putText(frame, f"Dist: {distance}", mid_point,
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('AirCanvas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()