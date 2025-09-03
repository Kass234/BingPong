
import pygame
import sys
import math
import os
import random
import time
from src import ball
from src import paddle
from src import button
from src import powerup

class Controller:

    def __init__(self):
        pygame.mixer.pre_init(22100, -16, 2, 512)
        pygame.init()
        self.display = pygame.display.set_mode((1280, 720))
        self.background = pygame.image.load("assets/background.png")
        self.mbackground = pygame.image.load("assets/mbackground.png")
        self.bing = pygame.image.load("assets/bing.png")
        self.pong = pygame.image.load("assets/pong.png")


        self.ball = ball.Ball('assets/ball.png', (640, 360), 7, 30, 30)
        self.ball2 = ball.Ball('assets/ball.png', (640, 360), self.ball.speed, 30, 30)
        self.balls = pygame.sprite.Group(self.ball)
        self.speed = self.ball.speed

        mBalls = 20
        self.mBalls = pygame.sprite.Group()
        for i in range(mBalls):
            x = random.randrange(158,1122)
            y = random.randrange(158, 692)
            self.mBalls.add(ball.Ball('assets/sunybing.png',(x, y), 3, 128, 128))


        self.font = pygame.font.SysFont('chalkduster.ttf', 72)
        bwidth = 330
        bheight = 130
        x = 475
        y = 125

        self.button1 = (button.Button("assets/start.png", (x, y), bwidth, bheight))
        self.button2 = (button.Button("assets/settings.png", (x, y+200), bwidth, bheight))
        self.button3 = (button.Button("assets/quit.png", (x, y+400), bwidth, bheight))
        self.buttons = pygame.sprite.Group((self.button1), (self.button2), (self.button3))



        self.sbuttons = pygame.sprite.Group()
        for i in ["assets/difficulty.png", "assets/players.png", "assets/back.png"]:
            self.sbuttons.add(button.Button(i, (x,y), bwidth, bheight))
            y = y + 200

        y = 125
        self.pbuttons = pygame.sprite.Group()
        for i in ["assets/1p.png", "assets/2p.png", "assets/back.png"]:
            self.pbuttons.add(button.Button(i, (x,y), bwidth, bheight))
            y = y + 200

        y = 125
        self.dbutton1 = button.Button("assets/easy.png", (x,y-90), bwidth, bheight)
        self.dbutton2 = button.Button("assets/medium.png", (x,y+90), bwidth, bheight)
        self.dbutton3 = button.Button("assets/hard.png", (x,y+270), bwidth, bheight)
        self.dbutton4 = button.Button("assets/back.png", (x,y+450), bwidth, bheight)
        self.dbuttons = pygame.sprite.Group((self.dbutton1), (self.dbutton2), (self.dbutton3), (self.dbutton4))


        x = random.randrange(200,1080)
        y = random.randrange(100,620)
        num = random.randrange(3)
        self.powerup = powerup.PowerUp(num, (x, y))
        self.powerups = pygame.sprite.Group()


        width = 20
        height = 150
        self.player = paddle.Paddle((60, 360), 5, width, height)
        self.opponent = paddle.Paddle((1200,360), 5, width, height)
        self.paddles = pygame.sprite.Group((self.player), (self.opponent))

        self.menuButton = button.Button('assets/mainmenu.png', (1180, 25), 80, 54)
        self.infoButton = button.Button('assets/info.png', (1160, 25), 100, 90)
        self.infoScreen1 = button.Button('assets/blank.png', (148, 75), 270, 115)
        self.infoScreen2 = button.Button('assets/blank.png', (838, 75), 270, 115)
        self.buttons.add(self.infoButton)
        self.dbuttons.add(self.infoButton)
        self.infoscreen = pygame.sprite.Group((self.infoScreen1), (self.infoScreen2))
        self.winMenu = pygame.sprite.Group(self.menuButton)
        self.all_sprites = pygame.sprite.Group((self.balls), (self.player), (self.opponent),  (self.menuButton))
        self.difficulty = 'M'
        self.players = 1
        self.state = 'MENU'


    def mainLoop(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.state == 'EXIT':
                self.exitloop()
            else:
                self.gameloop()


    def gameloop(self):
        pygame.mixer.music.load('assets/click.wav')
        clock = pygame.time.Clock()
        while self.state != 'EXIT':
            clock.tick(60)
            if self.state == 'GAME':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.menuButton.rect.collidepoint(event.pos)):
                            self.state = 'MENU'

                hit = pygame.sprite.spritecollide(self.ball, self.paddles, False)
                if hit:
                    for p in hit:
                        if p == self.opponent:
                            lastHit = 'r'
                        elif p == self.player:
                            lastHit = 'l'
                        relativeIntersect = ((p.rect.y + (p.height/2)) - (self.ball.rect.y + (self.ball.height/2)))
                        nRelativeIntersect = (relativeIntersect/(p.height/2))
                        angle = nRelativeIntersect * ((5*(math.pi))/12)
                        self.ball.hit(angle)
                if self.ball.twoBalls == True:
                    hit = pygame.sprite.spritecollide(self.ball2, self.paddles, False)
                    if hit:
                        for p in hit:
                            relativeIntersect = ((p.rect.y + (p.height/2)) - (self.ball2.rect.y + 5))
                            nRelativeIntersect = (relativeIntersect/(p.height/2))
                            angle = nRelativeIntersect * ((5*(math.pi))/12)
                            self.ball2.hit(angle)


                powerup = pygame.sprite.spritecollide(self.ball, self.powerups, True)
                if powerup:
                    if self.powerup.type == 0:
                        self.ball.hitPowerup(0)
                    if self.powerup.type == 1:
                        if lastHit == 'l':
                            self.player.hitPowerup()
                        if lastHit == 'r':
                            self.opponent.hitPowerup()
                    if self.powerup.type == 2:
                        self.ball.hitPowerup(1)
                        self.powerup.kill()
                        self.balls.add(self.ball2)
                        self.all_sprites.add(self.ball2)
                    self.powerup.hit()

                if self.ball.duration == 0:
                    self.ball2.kill()

                if self.ball.rect.x > 1220:
                    self.ball.reset()
                    self.player.point()
                if self.ball.rect.x < 60:
                    self.ball.reset()
                    self.opponent.point()
                if self.ball.twoBalls == True:
                    if self.ball2.rect.x > 1220:
                        self.ball2.reset()
                        self.player.point()
                    if self.ball2.rect.x < 60:
                        self.ball2.reset()
                        self.opponent.point()

                if self.players == 1:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.player.moveUp()
                    if keys[pygame.K_DOWN]:
                        self.player.moveDown()
                    if keys[pygame.K_w]:
                        self.player.moveUp()
                    if keys[pygame.K_s]:
                        self.player.moveDown()
                    if self.ball.twoBalls == False:
                        if (self.opponent.rect.y + ((self.opponent.height/2)-(self.opponent.height/5))) > self.ball.rect.y:
                            self.opponent.moveUp()
                        if (self.opponent.rect.y + ((self.opponent.height/2)+(self.opponent.height/5))) < self.ball.rect.y:
                            self.opponent.moveDown()
                    elif self.ball.twoBalls == True:
                        if self.ball.rect.x >= self.ball2.rect.x:
                            if (self.opponent.rect.y + ((self.opponent.height/2)-(self.opponent.height/5))) > self.ball.rect.y:
                                self.opponent.moveUp()
                            if (self.opponent.rect.y + ((self.opponent.height/2)+(self.opponent.height/5))) < self.ball.rect.y:
                                self.opponent.moveDown()
                        elif self.ball2.rect.x > self.ball.rect.x :
                            if (self.opponent.rect.y + ((self.opponent.height/2)-(self.opponent.height/5))) > self.ball2.rect.y:
                                self.opponent.moveUp()
                                print('moved up')
                            if (self.opponent.rect.y + ((self.opponent.height/2)+(self.opponent.height/5))) < self.ball2.rect.y:
                                self.opponent.moveDown()
                                print('moved down')

                elif self.players == 2:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.opponent.moveUp()
                    if keys[pygame.K_DOWN]:
                        self.opponent.moveDown()
                    if keys[pygame.K_w]:
                        self.player.moveUp()
                    if keys[pygame.K_s]:
                        self.player.moveDown()




                if self.player.score == 10:
                    self.state = 'P1WIN'
                    self.player.resetScore()
                    self.opponent.resetScore()
                if self.opponent.score == 10:
                    self.state = 'P2WIN'
                    self.player.resetScore()
                    self.opponent.resetScore()


                score1 = self.font.render(str(self.player.score), True, [255,255,255])
                score2 = self.font.render(str(self.opponent.score), True, [255,255,255])

                if self.powerup.spawnTimer == 1200:
                    self.powerups.add(self.powerup)
                    print("spawned")

                self.display.blit(self.background, (0, 0))
                self.balls.update()
                self.powerup.update()
                self.paddles.update()
                self.display.blit(score1, (200, 50))
                self.display.blit(score2, (1080, 50))
                if self.powerup.state == 'alive':
                    self.powerups.draw(self.display)
                    print('draw')
                self.all_sprites.draw(self.display)

            if self.state == 'MENU':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.button1.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'GAME'
                        if(self.button2.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'SMENU'
                        if(self.button3.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'EXIT'
                        if(self.infoButton.rect.collidepoint(event.pos)):
                            self.state = 'INFO'

                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                self.buttons.draw(self.display)
                self.display.blit(self.bing, (65, 160))
                self.display.blit(self.pong, (815,120))

            if self.state == 'SMENU':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.button1.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'DMENU'
                        if(self.button2.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'PMENU'
                        if(self.button3.rect.collidepoint(event.pos)):
                            pygame.mixer.music.play()
                            self.state = 'MENU'
                        if(self.infoButton.rect.collidepoint(event.pos)):
                            self.state = 'INFO'
                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                self.buttons.draw(self.display)
                self.sbuttons.draw(self.display)

            if self.state == 'DMENU':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.dbutton1.rect.collidepoint(event.pos)):
                            self.difficulty = 'E'
                            self.ball.changespeed(self.difficulty)
                            self.player.changedifficulty(self.difficulty)
                            self.opponent.changedifficulty(self.difficulty)
                            print('ball speed = ', str(self.ball.speed), ', left paddle speed = ', str(self.player.speed), ', right paddle speed = ', str(self.opponent.speed))
                            self.state = 'SMENU'
                        if(self.dbutton2.rect.collidepoint(event.pos)):
                            self.difficulty = 'M'
                            self.ball.changespeed(self.difficulty)
                            self.ball.changespeed(self.difficulty)
                            self.player.changedifficulty(self.difficulty)
                            self.opponent.changedifficulty(self.difficulty)
                            print('ball speed = ', str(self.ball.speed), ', left paddle speed = ', str(self.player.speed), ', right paddle speed = ', str(self.opponent.speed))
                            self.state = 'SMENU'
                        if(self.dbutton3.rect.collidepoint(event.pos)):
                            self.difficulty = 'H'
                            self.ball.changespeed(self.difficulty)
                            self.ball.changespeed(self.difficulty)
                            self.player.changedifficulty(self.difficulty)
                            self.opponent.changedifficulty(self.difficulty)
                            print('ball speed = ', str(self.ball.speed), ', left paddle speed = ', str(self.player.speed), ', right paddle speed = ', str(self.opponent.speed))
                            self.state = 'SMENU'
                        if(self.dbutton4.rect.collidepoint(event.pos)):
                            self.state = 'SMENU'
                        if(self.infoButton.rect.collidepoint(event.pos)):
                            self.state = 'INFO'
                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                self.dbuttons.draw(self.display)

            if self.state == 'PMENU':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.button1.rect.collidepoint(event.pos)):
                            self.players = 1
                            self.state = 'SMENU'
                        if(self.button2.rect.collidepoint(event.pos)):
                            self.players = 2
                            self.state = 'SMENU'
                        if(self.button3.rect.collidepoint(event.pos)):
                            self.state = 'SMENU'
                        if(self.infoButton.rect.collidepoint(event.pos)):
                            self.state = 'INFO'
                self.display.blit(self.mbackground, (0, 0))
                self.buttons.draw(self.display)
                self.mBalls.draw(self.display)
                self.mBalls.update()
                self.pbuttons.draw(self.display)

            if self.state == 'P1WIN':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.menuButton.rect.collidepoint(event.pos)):
                            self.state = 'MENU'
                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                img = pygame.image.load('assets/winner.png')
                img2 = pygame.image.load('assets/1p.png')
                self.display.blit(img, (385, 100))
                self.display.blit(img2, (475, 425))
                self.winMenu.draw(self.display)
            pygame.display.flip()

            if self.state == 'P2WIN':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.menuButton.rect.collidepoint(event.pos)):
                            self.state = 'MENU'
                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                img = pygame.image.load('assets/winner.png')
                img2 = pygame.image.load('assets/2p.png')
                self.display.blit(img, (385, 100))
                self.display.blit(img2, (475, 425))
                self.winMenu.draw(self.display)

            if self.state == 'INFO':
                img = pygame.image.load('assets/infoscreen.png')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(self.menuButton.rect.collidepoint(event.pos)):
                            self.state = 'MENU'
                        if(self.infoScreen1.rect.collidepoint(event.pos)):
                            self.players = 1
                            print('self.players = ', self.players)
                        if(self.infoScreen2.rect.collidepoint(event.pos)):
                            self.players = 2
                            print('self.players = ', self.players)

                keys = pygame.key.get_pressed()
                if self.players == 1:
                    if keys[pygame.K_UP]:
                        self.player.moveUp()
                    if keys[pygame.K_DOWN]:
                        self.player.moveDown()
                    if keys[pygame.K_w]:
                        self.player.moveUp()
                    if keys[pygame.K_s]:
                        self.player.moveDown()

                elif self.players == 2:
                    if keys[pygame.K_UP]:
                        self.opponent.moveUp()
                    if keys[pygame.K_DOWN]:
                        self.opponent.moveDown()
                    if keys[pygame.K_w]:
                        self.player.moveUp()
                    if keys[pygame.K_s]:
                        self.player.moveDown()




                self.display.blit(self.mbackground, (0, 0))
                self.mBalls.draw(self.display)
                self.mBalls.update()
                self.infoscreen.draw(self.display)
                self.display.blit(img, (0, 0))
                self.paddles.draw(self.display)
                self.paddles.update()
                self.winMenu.draw(self.display)

            pygame.display.flip()

    def exitloop(self):
        pygame.quit()
        exit()
