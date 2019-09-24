# Python Chess
# Written by Yuriy Strela for educational purposes

import pygame
pygame.init()

GAMEWIDTH = 500
GAMEHEIGHT = 500


win = pygame.display.set_mode((GAMEWIDTH,GAMEHEIGHT))

pygame.display.set_caption("First Game")


x = 50
y = 50
width = 40
height = 40
velocity = 10

isJump = False
jumpCount = 10

run = True

while run:
	pygame.time.delay(30)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] and x >= velocity:
		x -= velocity
	if keys[pygame.K_RIGHT] and x < GAMEWIDTH-width:
		x += velocity
	if not(isJump):
		if keys[pygame.K_UP] and y >= velocity:
			y -= velocity
		if keys[pygame.K_DOWN] and y < GAMEHEIGHT-height:	
			y += velocity
		if keys[pygame.K_SPACE]:
			isJump = True
	else:
		if jumpCount >= -10:
			neg = 1
			if jumpCount < 0:
				neg = -1
			y -= (jumpCount ** 2) * 0.5 * neg
			jumpCount -= 1
		else:
			isJump = False
			jumpCount = 10

	win.fill((0,0,0))  #remove previous rectangle from the screen 
	pygame.draw.rect(win, (255, 0, 0), (x,y,width,height))
	pygame.display.update()

pygame.quit()

