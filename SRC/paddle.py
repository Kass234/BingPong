
import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, speed, width, height):
         pygame.sprite.Sprite.__init__(self)
         self.image = pygame.Surface((width, height))
         self.image.fill([255,255,255])
         self.rect = pygame.Rect(pos[0], pos[1], width, height)

         self.pos = pos
         self.rect.x = pos[0]
         self.rect.y = pos[1]

         self.powerup = False
         self.duration = 0

         self.height = height
         self.speed = speed
         self.score = 0

    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > (720-(self.height+1)):
            self.rect.y = (720-(self.height+1))

    def changedifficulty(self, difficulty):
        if difficulty == 'E':
            self.speed = 3
            self.height = 150
            self.image.fill([255,255,255])
        if difficulty == 'M':
            self.speed = 5
            self.height = 125
        if difficulty == 'H':
            self.speed = 7
            self.height = 100
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 20, self.height)
        self.image = pygame.Surface((20, self.height))
        self.image.fill([255,255,255])

    def hitPowerup(self):
        if self.powerup == False:
            self.powerup = True
            self.height += 50
            self.image = pygame.Surface((20, self.height))
            self.image.fill([255,255,255])
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 20, self.height)

    def point(self):
        self.score += 1
        
    def resetScore(self):
        self.score = 0

    def update(self):
        if self.powerup == True:
            self.duration += 1
            if self.duration == 600:
                self.height -= 50
                self.image = pygame.Surface((20, self.height))
                self.image.fill([255,255,255])
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 20, self.height)
                self.duration = 0
                self.powerup = False
