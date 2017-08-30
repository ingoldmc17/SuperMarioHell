import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)

character_width = 48
character_height = 63
cannon_width = 26
cannon_height = 50
bullet_width = 30
bullet_height = 18

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Super Mario Hell')
clock = pygame.time.Clock()

marioImg = pygame.image.load('mario.png')
blasterImg = pygame.image.load('billblaster.png')
bulletImg = pygame.image.load('bullet.png')

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(TextSurf, TextRect)
	
	pygame.display.update()
	
	time.sleep(2)
	
	game_loop()

def blit_cannons(num_cannons, image):
	increment = 0
	while increment <= display_height:
		gameDisplay.blit(image,(0,increment))
		gameDisplay.blit(image,(display_width-cannon_width, increment))
		increment += (display_height / num_cannons)
	
def blit_character(x, y, image):
	gameDisplay.blit(image,(x,y))
	
def blit_bullet(x, y, image):
	gameDisplay.blit(image,(x,y))
	
def random_cannon(num_cannons):
	# returns a tuple (x,y) coords of a random left-side cannon
	cannon_locations = []
	increment = 0
	while increment <= display_height:
		cannon_locations.append((0,increment))
		increment += (display_height / num_cannons)
	return cannon_locations[random.randrange(0,len(cannon_locations)-1)]
	
def collision_occurs(x1,y1,w1,h1,x2,y2,w2,h2):
	# returns true if the two items collide
	x_crossover = False
	y_crossover = False
	
	for pixel in range(x1,x1+w1+1):
		if pixel > x2 and pixel < x2 + w2:
			x_crossover = True
			break
	
	for pixel in range(y1, y1+h1+1):
		if pixel > y2 and pixel < y2 + h2:
			y_crossover = True
			break
			
	if x_crossover and y_crossover:
		return True
	else:
		return False
	
def character_death():
	pass

def game_loop():
	
	character_x = int(display_width * 0.45)
	character_y = int(display_height * 0.80)
	
	max_x = display_width - character_width - cannon_width
	min_x = cannon_width
	max_y = display_height - character_height
	min_y = 0
	
	cannon_count = 8
	
	bullets = [random_cannon(cannon_count)]
	bullets_with_children = []
	bullet_speed = 3
	threshold = 0.95 * display_width
	
	character_xChange = 0
	character_yChange = 0
	
	gameExit = False
	
	while not gameExit:
		print("Bullets: {}".format(len(bullets)))
		print("Bullets with children: {}".format(len(bullets_with_children)))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					character_xChange = -5
				elif event.key == pygame.K_RIGHT:
					character_xChange = 5
				elif event.key == pygame.K_UP:
					character_yChange = -5
				elif event.key == pygame.K_DOWN:
					character_yChange = 5
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					character_xChange = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					character_yChange = 0
					
		character_x += character_xChange
		character_y += character_yChange
		
		gameDisplay.fill(white)
		
		blit_cannons(cannon_count, blasterImg)
		blit_character(character_x, character_y, marioImg)
			
		for index, bullet in enumerate(bullets, start=0):
			bullet_x, bullet_y = bullet
			if bullet_x > display_width and bullet in bullets_with_children:
				bullets.remove(bullet)
				bullets_with_children.remove(bullet)
				break
			elif bullet_x > display_width:
				bullets.remove(bullet)
			elif bullet_x > threshold and bullet not in bullets_with_children:
				bullets.append(random_cannon(cannon_count))
				blit_bullet(bullet_x,bullet_y,bulletImg)
				bullet_x += bullet_speed
				bullets[index] = (bullet_x, bullet_y)
				bullets_with_children.append((bullet_x, bullet_y))
				threshold *= .95
			elif bullet_x > threshold and bullet in bullets_with_children:
				blit_bullet(bullet_x, bullet_y, bulletImg)
				bullet_x += bullet_speed
				bullets[index] = (bullet_x,bullet_y)
				spot = bullets_with_children.index(bullet)
				bullets_with_children[spot] = (bullet_x, bullet_y)
			else:
				blit_bullet(bullet_x, bullet_y, bulletImg)
				bullet_x += bullet_speed
				bullets[index] = (bullet_x,bullet_y)
				

				
		
			
		if character_x > max_x:
			character_x = max_x
		elif character_x < min_x:
			character_x = min_x
		if character_y > max_y:
			character_y = max_y
		elif character_y < min_y:
			character_y = min_y
			
		if collision_occurs(character_x,character_y,character_width,character_height,bullet_x,bullet_y,bullet_width,bullet_height):
			message_display('Game Over')
		
		pygame.display.update()
		clock.tick(60)
		
game_loop()
pygame.quit()
quit()
		
		