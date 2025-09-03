
import pygame
import random
import math



class Ball(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        self.width = width
        self.height = height
        num1 = random.randrange(101)
        num2 = (num1 / 100) *((5*math.pi)/12)
        self.vel_y = self.speed * math.sin(num2)
        self.vel_x = random.choice([-1,1])
        self.duration = 600
        self.powerup = False
        self.twoBalls = False

    def hit(self, angle):
        self.vel_x *= -1
        self.vel_y = self.speed * -math.sin(angle)

    def speedUp(self):
        self.speed *= 2

    def update(self):
        if (self.rect.x + self.width) > 1280 or self.rect.x < 0:
            self.vel_x *= -1
        if (self.rect.y + self.height) > 720 or self.rect.y <= 0:
            self.vel_y *= -1
        self.rect.x = self.rect.x + (self.speed * self.vel_x)
        self.rect.y = self.rect.y + self.vel_y
        if self.powerup == True:
            self.duration -= 1
            if self.duration == 0:
                self.powerup = False
                self.speed = (self.speed/2)
                self.duration = 600
        if self.twoBalls == True:
            self.duration -= 1
            if self.duration == 0:
                self.twoBalls = False
            print(self.duration)

    def hitPowerup(self, type):
        self.duration = 600
        if type == 0:
            if self.powerup == False:
                self.powerup = True
                self.speed *= 2
        if type == 1:
            self.twoBalls = True


    def changespeed(self, difficulty):
        if difficulty == 'E':
            self.speed = 5
        if difficulty == 'M':
            self.speed = 7
        if difficulty == 'H':
            self.speed = 9

    def reset(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.vel_x = random.choice([-1,1])
        self.vel_y = 0
