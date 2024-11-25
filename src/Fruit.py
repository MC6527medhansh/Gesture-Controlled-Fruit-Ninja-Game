import pygame
import random

class Fruit:
    def __init__(self, screen_width, screen_height, fruit_images):
        self.image = random.choice(fruit_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = 0
        self.speed = random.randint(5, 10)
             
    def moveY(self):
        self.rect.y += self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def off_screen(self, screen_height):
        return self.rect.y > screen_height
    