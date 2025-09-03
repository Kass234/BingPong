
import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        x = random.randrange(200,1080)
        y = random.randrange(100,620)
        self.type = random.randrange(3)
        if self.type == 0:
            self.image = pygame.image.load('assets/speedup.png')
            self.rect = pygame.Rect(x, y, 70, 70)
        if self.type == 1:
            self.image = pygame.image.load('assets/paddleup.png')
            self.rect = pygame.Rect(x, y, 70, 70)
        if self.type == 2:
            self.image = pygame.image.load('assets/extraball.png')
            self.rect = pygame.Rect(x, y, 70, 70)
        self.spawnTimer = 0
        self.state = 'dead'

    def hit(self):
        self.spawnTimer = 0
        self.state = 'dead'

    def update(self):
        if self.spawnTimer  == 1200:
            x = random.randrange(200,1080)
            y = random.randrange(100,620)
            self.type = random.randrange(3)
            if self.type == 0:
                self.image = pygame.image.load('assets/speedup.png')
                self.rect = pygame.Rect(x, y, 70, 70)
            if self.type == 1:
                self.image = pygame.image.load('assets/paddleup.png')
                self.rect = pygame.Rect(x, y, 70, 70)
            if self.type == 2:
                self.image = pygame.image.load('assets/extraball.png')
                self.rect = pygame.Rect(x, y, 70, 70)
            self.state = 'alive'
        self.spawnTimer += 1
        print(self.spawnTimer)
