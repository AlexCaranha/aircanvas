import cv2
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

        # get hand landmarks (for future gesture recognition)
        landmarks = tracker.get_hand_position(frame)
        
        # draw circle on indez fingetip if detected
        if landmarks and len(landmarks) > 0:
            index_finger_tip = landmarks[8]
            cv2.circle(frame, (index_finger_tip[1], index_finger_tip[2]), 10, (0, 255, 0), cv2.FILLED)

        cv2.imshow('AirCanvas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()