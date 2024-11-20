import cv2 as cv
import pygame
import mediapipe as mp

mp_hands = mp.solutions.hands.Hands()
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,  
    max_num_hands=1,  
    min_detection_confidence=0.7,  
    min_tracking_confidence=0.5  
)


cam = cv.VideoCapture(0)
frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    out.write(frame)
    
    cv.flip(cam)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_lamdmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.drawing.draw_landmark(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            for index, landmark in enumerate(hand_landmarks.landmark): 
                height, width, _ = frame.shape
                px, py = int(landmark.x * width), int(landmark.y * height)
                print(f"Landmark {index}: ({px}, {py}")

    cv.imshow('Camera', frame)

    if cv.waitKey(1) == ord('q'):
        break

cam.release()
out.release()
cv2.destroyAllWindows()