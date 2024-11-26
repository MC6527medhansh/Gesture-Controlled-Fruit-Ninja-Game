import mediapipe as mp


class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.index_finger_pos = None

    def process_frame(self, frame):
        # Process the frame and detect hand landmarks
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                
                self.index_finger_pos = (
                    int(hand_landmarks.
                        landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x 
                        * self.screen_width),
                    int(hand_landmarks.
                        landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y 
                        * self.screen_height)
                )
        else:
            self.index_finger_pos = None
        
        return results
            
    def draw_landmarks(self, frame, results):
        # Draw hand landmarks and connections on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

    def get_index_finger_position(self):
        # Return the current index finger position.
        return self.index_finger_pos
