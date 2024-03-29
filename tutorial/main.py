# Python Test Game
# Written by Yuriy Strela for educational purposes

import pygame
pygame.init()

GAMEWIDTH = 500
GAMEHEIGHT = 480

win = pygame.display.set_mode((GAMEWIDTH,GAMEHEIGHT))

pygame.display.set_caption("First Game")

#Image loading
walkRight = [pygame.image.load("images/R1.png"),pygame.image.load("images/R2.png"),pygame.image.load("images/R3.png"),pygame.image.load("images/R4.png"),pygame.image.load("images/R5.png"),pygame.image.load("images/R6.png"),pygame.image.load("images/R7.png"),pygame.image.load("images/R8.png"),pygame.image.load("images/R9.png")]
walkLeft = [pygame.image.load("images/L1.png"),pygame.image.load("images/L2.png"),pygame.image.load("images/L3.png"),pygame.image.load("images/L4.png"),pygame.image.load("images/L5.png"),pygame.image.load("images/L6.png"),pygame.image.load("images/L7.png"),pygame.image.load("images/L8.png"),pygame.image.load("images/L9.png")]
bg = pygame.image.load("images/bg.jpg")
char = pygame.image.load("images/standing.png")

bulletSound = pygame.mixer.Sound("audio/bullet.wav")
hitSound = pygame.mixer.Sound("audio/hurt.wav")

music = pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.play(-1) ## Play sound forever

clock = pygame.time.Clock()

class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 10
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)

	def draw(self,win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0

		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (self.x, self.y))
			else:
				win.blit(walkLeft[0], (self.x,self.y))

		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def hit(self):
		self.jumpCount = 10
		self.isJump = False
		self.x = 60
		self.y = 410
		self.walkCount = 0
		font1 = pygame.font.SysFont("comicsans", 100)
		text = font1.render("-5", 1, (255,0,0))
		win.blit(text, ((GAMEWIDTH/2) - (text.get_width()/2), 200))
		pygame.display.update()
		i = 0
		while i < 300:
			pygame.time.delay(10)
			i += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 301
					pygame.quit()

class projectile(object):
	def __init__(self,x,y,radius,color,facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.velocity = 8 * facing

	def draw(self,win):
		pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
	walkRight = [pygame.image.load("images/R1E.png"),pygame.image.load("images/R2E.png"),pygame.image.load("images/R3E.png"),pygame.image.load("images/R4E.png"),pygame.image.load("images/R5E.png"),pygame.image.load("images/R6E.png"),pygame.image.load("images/R7E.png"),pygame.image.load("images/R8E.png"),pygame.image.load("images/R9E.png"),pygame.image.load("images/R10E.png"),pygame.image.load("images/R11E.png")]
	walkLeft = [pygame.image.load("images/L1E.png"),pygame.image.load("images/L2E.png"),pygame.image.load("images/L3E.png"),pygame.image.load("images/L4E.png"),pygame.image.load("images/L5E.png"),pygame.image.load("images/L6E.png"),pygame.image.load("images/L7E.png"),pygame.image.load("images/L8E.png"),pygame.image.load("images/L9E.png"),pygame.image.load("images/L10E.png"),pygame.image.load("images/L11E.png")]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]
		self.walkCount = 0
		self.velocity = 3
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.health = 9
		self.visible = True
		
	def hit(self):
		hitSound.play()
		if self.health > 0:
			self.health -= 1
		else:
			self.visible = False
		global score
		print("Hit")
		score += 100
		print(score)
		pass

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0

			if self.velocity > 0:
				win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20 , 50, 10))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20 , 50 - ((50/9) * (9 - self.health)), 10))
			#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def move(self):
		if self.velocity > 0:
			if self.x + self.velocity < self.path[1]:
				self.x += self.velocity
			else:
				self.velocity = self.velocity * -1
				self.walkCount = 0
		else:
			if self.x - self.velocity > self.path[0]:
				self.x += self.velocity
			else:
				self.velocity = self.velocity * -1
				self.walkCount = 0


def redrawGameWindow():
	global walkCount
	win.blit(bg, (0,0))  #draw background 
	text = font.render("Score: " + str(score), 1, (0,0,0))
	win.blit(text, ((GAMEWIDTH/2)-(text.get_width()/2), 100))
	man.draw(win)
	goblin.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()
										#size #bold #italic
font = pygame.font.SysFont("comicsans", 30,   True, True)
run = True
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootcooldown = 0
score = 0
bullets = []

while run:
	clock.tick(27)
	if goblin.visible == True:
		if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]: # above bottom and below top of rectangle
				if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
					man.hit()
					score -= 5
			

	if shootcooldown > 0:
		shootcooldown += 1
	if shootcooldown > 3:
		shootcooldown = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # above bottom and below top of rectangle
			if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
				goblin.hit()
				bullets.pop(bullets.index(bullet))

		if bullet.x < GAMEWIDTH and bullet.x > 0:
			bullet.x += bullet.velocity
		else: 
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed()

	if keys[pygame.K_SPACE] and shootcooldown == 0:
		bulletSound.play()
		if man.left:
			facing = -1
		else:
			facing = 1
		if len(bullets) < 5:
			bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))
		shootcooldown = 1


	if keys[pygame.K_LEFT] and man.x >= man.velocity:
		man.x -= man.velocity
		man.left = True
		man.right = False
		man.standing = False
	elif keys[pygame.K_RIGHT] and man.x < GAMEWIDTH-man.width:
		man.x += man.velocity
		man.left = False
		man.right = True
		man.standing = False
	else:
		man.walkCount = 0
		man.standing = True
	if not(man.isJump):
		if keys[pygame.K_UP]:
			man.isJump = True
			man.walkCount = 0
	else:
		if man.jumpCount >= -10:
			neg = 1
			if man.jumpCount < 0:
				neg = -1
			man.y -= (man.jumpCount ** 2) * 0.5 * neg
			man.jumpCount -= 1
		else:
			man.isJump = False
			man.jumpCount = 10

	redrawGameWindow()
pygame.quit()

