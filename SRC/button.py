
import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, image, pos, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.pos = pos
        self.width = width
        self.height = height
