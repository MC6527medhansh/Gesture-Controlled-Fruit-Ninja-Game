import cv2 as cv
import pygame
from PlayerHand import Player
from UI import UI
from Events import Events
from typing import List

# Initialize camera
cam = cv.VideoCapture(0)

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Ninja")
clock = pygame.time.Clock()

# Load assets
fruit_images = [
    pygame.transform.scale(pygame.image.load("assets/images/apple.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/images/banana.png"), (50, 50))
]
slice_sound = pygame.mixer.Sound("assets/sounds/steel-blade-slice-2-188214.mp3")

# Set up modules
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
ui = UI()
events = Events(SCREEN_WIDTH, SCREEN_HEIGHT, fruit_images)

# Game variables
score = 0
running = True
FRUIT_SPAWN_TIME = 1000
pygame.time.set_timer(pygame.USEREVENT, FRUIT_SPAWN_TIME)

# Main loop
while running:
    screen.fill((255, 255, 255))

    # Handle OpenCV feed
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process hand landmarks
    results = player.process_frame(frame_rgb)
    
    # Draw hand landmarks on the OpenCV feed
    player.draw_landmarks(frame, results)
    
    # Get index finger position
    index_finger_pos = player.get_index_finger_position()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            events.spawn_fruit()

    # Update fruits
    events.update_fruits(screen)

    # Check slices
    if index_finger_pos and events.check_slices(index_finger_pos, slice_sound):
        score += 1

    # Draw UI
    ui.draw_score(screen, score)
    
    # Draw the green dot for index finger position
    if index_finger_pos:
        pygame.draw.circle(screen, (0, 255, 0), index_finger_pos, 10)

    # Update Pygame display
    pygame.display.flip()
    clock.tick(30)

    # Display OpenCV webcam feed
    cv.imshow("Webcam Feed", frame)

    if cv.waitKey(1) == ord('q'):
        running = False

# Cleanup
cam.release()
cv.destroyAllWindows()
pygame.quit()































# import cv2 as cv
# import pygame
# import mediapipe as mp

# from Fruit import Fruit
# from typing import List

# # Camera configuration
# cam = cv.VideoCapture(0)
# frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv.VideoWriter_fourcc(*'mp4v')
# out = cv.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# # Initialise mediapipe
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(
#     static_image_mode=False,  
#     max_num_hands=2,  
#     min_detection_confidence=0.7,  
#     min_tracking_confidence=0.5  
# )

# # Initialise PyGame
# pygame.init()

# SCREEN_WIDTH = 640
# SCREEN_HEIGHT = 480
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Fruit Ninja")
# clock = pygame.time.Clock()

# fruit_images = [
#     pygame.transform.scale(pygame.image.load("assets/images/apple.png"), (50, 50)),
#     pygame.transform.scale(pygame.image.load("assets/images/banana.png"), (50, 50))
# ]
# slice_sound = pygame.mixer.Sound(
#     "assets/sounds/steel-blade-slice-2-188214.mp3")

# FRUIT_SPAWN_TIME = 1000
# pygame.time.set_timer(pygame.USEREVENT, FRUIT_SPAWN_TIME)

# fruits: List[Fruit] = []

# def spawn_fruit():
#     fruits.append(Fruit(SCREEN_WIDTH, SCREEN_HEIGHT, fruit_images))
    
# def check_slices(index_finger_pos):
#     sliced = False
#     for fruit in fruits[:]:
#         if fruit.rect.collidepoint(index_finger_pos):
#             fruits.remove(fruit)
#             slice_sound.play()
#             sliced = True
#     return sliced
              
# running = True
# score = 0

# while running:
#     screen.fill((255, 255, 255))
    
#     ret, frame = cam.read()
#     if not ret:
#         print("Failed to grab frame")
#         break
#     frame = cv.flip(frame, 1)
#     frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#     results = hands.process(frame_rgb)
    
#     index_finger_pos = None
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(frame, hand_landmarks, 
#                                       mp_hands.HAND_CONNECTIONS)
         
#             # for index, landmark in enumerate(hand_landmarks.landmark):
#             #     height, width, _ = frame.shape
#             #     px, py = int(landmark.x * width), int(landmark.y * height)
#             #     print(f"Landmark {index}: ({px}, {py})")
            
#             index_finger_pos = (
#                 int(hand_landmarks.landmark
#                     [mp_hands.HandLandmark.INDEX_FINGER_TIP].x * SCREEN_WIDTH),
#                 int(hand_landmarks.landmark
#                     [mp_hands.HandLandmark.INDEX_FINGER_TIP].y * SCREEN_HEIGHT)
#             )
            
#             pygame.draw.circle(screen, (0, 255, 0), index_finger_pos, 10)
            
#     cv.imshow("Webcam Feed", frame)
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.USEREVENT:
#             spawn_fruit()
            
#     for fruit in fruits[:]:
#         fruit.moveY()
#         fruit.draw(screen)
#         if (fruit.off_screen(SCREEN_HEIGHT)):
#             fruits.remove(fruit)
            
#     if (index_finger_pos):
#         if (check_slices(index_finger_pos)):
#             score += 1
        
#     font = pygame.font.Font(None, 36)
#     score_text = font.render(f"Score: {score}", True, (0, 0, 0))
#     screen.blit(score_text, (10, 10))

#     pygame.display.flip()
#     clock.tick(30)
    
#     if cv.waitKey(1) == ord('q'):
#         running = False


# cam.release()
# out.release()
# cv.destroyAllWindows()
