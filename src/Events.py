import pygame
from Fruit import Fruit


class Events:
    def __init__(self, screen_width, screen_height, fruit_images):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fruit_images = fruit_images
        self.fruits = []

    def spawn_fruit(self):
        # Add a new fruit to the list
        self.fruits.append(Fruit(self.screen_width, 
                                 self.screen_height, 
                                 self.fruit_images))

    def update_fruits(self, screen):
        # Update and draw fruits on the screen
        for fruit in self.fruits[:]:
            fruit.moveY()
            fruit.draw(screen)
            if fruit.off_screen(self.screen_height):
                self.fruits.remove(fruit)

    def check_slices(self, index_finger_pos, slice_sound):
        # Check if any fruits are sliced and remove them
        sliced = False
        for fruit in self.fruits[:]:
            if fruit.rect.collidepoint(index_finger_pos):
                self.fruits.remove(fruit)
                slice_sound.play()
                sliced = True
        return sliced
