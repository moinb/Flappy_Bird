#/********************************************************************************************************
# * 		Copyright (C) MOIN BANGI moin.bangi@live.com                            		*
# *									          	  		*
# *		 This program is free software; you can redistribute it and/or modify it        	*
# *		 under the terms of the GNU Lesser General Public License as published by		*
# * 		 the Free Software Foundation; either version 2.1 of the License, or      		*
# * 		 (at your option) any later version.                                      		*
# *        								          	 		*
# *		 This program is distributed in the hope that it will be useful,         		*
# * 		 but WITHOUT ANY WARRANTY; without even the implied warranty of	          		*
# * 		 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                   	*
# *		 GNU Lesser General Public License for more details.                      		*
# * 									     		  		*
# * 		 You should have received a copy of the GNU Lesser General Public License 		*
# * 		 along with this program; if not, write to the Free Software Foundation,  		*
# * 		 Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.        		*
# ********************************************************************************************************/




import pygame
from pygame.locals import *
import sys
import random

	
class FlappyBird:
						#............Initial Parameters............#
    def __init__(self):	
	self.screen = pygame.display.set_mode((width, height))			#Resolution of Screen
        self.bird = pygame.Rect(65, 50, 50, 50)					#Resolution of Bird
        self.background = pygame.image.load("background.png").convert()	#Background Image
        self.birdSprites = [pygame.image.load("1.png").convert_alpha(),	#Images of bird (Stable, Flying, Dead)
                            pygame.image.load("2.png").convert_alpha(),
                            pygame.image.load("dead.png")]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()	#Image of upper wall
        self.wallDown = pygame.image.load("top.png").convert_alpha()	#Image of lower wall
        self.gap = 140								#Gap Between the Walls
        self.wallx = width							#Distance of wall from x-axis						
        self.birdY = 350							#Height of bird location
        self.jump = 0								#State of jump (0 = no jump, 1 = jump)
        self.jumpSpeed = 10							#Speed of Jump
        self.gravity = 5							#Gravity by which bird falls
        self.dead = False							#State of bird (True = Dead, False = Alive)
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
						#..........Wall Updates over time..........#
    def updateWalls(self):
        self.wallx -= 5								#Wall comes closer by 2 pixels per tick
        if self.wallx < -80:
            self.counter += 1							#Increase Score by 1
	    self.wallx = width							#Set initial distace of wall							
            self.offset = random.randint(-110, 110)
						#..........Bird Updates over time..........#
    def birdUpdate(self):							
        if self.jump:								#If bird Jumps
            self.jumpSpeed -= 1							#decrement jumpspeed by 1 for each jumps
            self.birdY -= self.jumpSpeed					#Height of bird increases according to jump speed
            self.jump -= 1							#Update Jump parameter
        else:									#If bird doesn't jump
            self.birdY += self.gravity						#Decrease height of bird according to gravity
            self.gravity += 0.2							#Keep increasing gravity by 0.2 for each tick
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):					#If bird collides to upper wall, it dies
            self.dead = True
        if downRect.colliderect(self.bird):					#If bird collides to lower wall, it dies
            self.dead = True
        if not 0 < self.bird[1] < 720:						#if bird is within window
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = width
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):								#runtime 
        clock = pygame.time.Clock()						#initalize clock
        pygame.font.init()							#initialize font
        font = pygame.font.SysFont("Arial", 50)					#font style Arial, size 50
        while True:								#infinite loop
            clock.tick(60)							#set fps = 60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:					#exiting game
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))					#screen filling outside the background with white color
            self.screen.blit(self.background, (0, 0))				
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
	    myfont = pygame.font.SysFont("Arial", 50)				#initialize myfont
	    label = myfont.render("SCORE: ", 1, (255,255,255))			#print score in white color at top of screen
            self.screen.blit(label, ((width * 0.5) - 200, height * 0.1))	#position adjustments
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (width * 0.5, height * 0.1))

            if self.dead:							#if bird dies
                self.sprite = 2							#change bird image to dead
            elif self.jump:							#if bird jumps
                self.sprite = 1							#change bird image to flying bird
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()							
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
	pygame.init()								#To initialize Video System
	width = pygame.display.Info().current_w					#capture screen width
	height = pygame.display.Info().current_h				#capture screen height
	width = width - 80
	height = height - 80
        FlappyBird().run()							#Run the game 
