
import pygame
from pygame.locals import *
import random
import os


pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Snake')

pygame.mixer.init()
pygame.mixer.music.load('Assets/background.music.mp3')
pygame.mixer.music.play(loops=-1)

#for space
clock=pygame.time.Clock()	

#define fontstyle and font size
font = pygame.font.SysFont("Times New Roman", 20, bold = True)
font2 = pygame.font.SysFont("Times New Roman", 30, bold = True)


#setup a rectangle for "Play Again" Option
#Playagain_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#define snake variables
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([300,310])
snake_pos.append([300,320])
snake_pos.append([300,330])
direction = 1 #1 is up, 2 is right, 3 is down, 4 is left


#define game variables
cell_size = 15
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0



background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tanah.jpg")), (screen_width, screen_height))
#define color of snake and food 
body_inner = (255, 255, 0)
body_outer = (0, 0, 0)
food_col = (255, 255, 0)

#define colors
blue = (0, 0, 255)
red = (255, 0, 0)
firebrick1 = (255,48,48)
dodgerblue1 = (30,144,255)
ghostwhite1 = (248,248,255)	
chocolate = (210,105,30)
black = (0, 0, 0)

def draw_screen():
	screen.blit(background, (0,0))

def draw_score():
	score_txt = 'Score: ' + str(score)
	score_img = font2.render(score_txt, True, ghostwhite1)
	screen.blit(score_img, (250, 10))

def check_game_over(game_over):
	#first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
	head_count = 0
	for x in snake_pos:
		if snake_pos[0] == x and head_count > 0:
			game_over = True
		head_count += 1

	#second check is to see if the snake has gone out of bounds
	if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
		game_over = True   

	return game_over


def draw_game_over():
	over_text = "Game Over!"
	over_img = font.render(over_text, True, red)
	screen.blit(over_img, (250,250))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, ghostwhite1)
	screen.blit(again_img, (250,300))
	pygame.mixer.music.pause()
	pygame.mixer.music.play()
	

def pause():
	loop = 1
	Pause = font.render("PAUSED", True, ghostwhite1)
	pygame.draw.rect(screen, black, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
	screen.blit(Pause,(screen_width // 2 - 40, screen_height // 2 - 50))
	Continue = font.render("Press to continue", True, ghostwhite1)
	pygame.draw.rect(screen, chocolate, (screen_width // 2 - 80, screen_height // 2, 160, 50))
	screen.blit(Continue, (screen_width // 2 - 70, screen_height // 2 + 10))

	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = 0
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					loop=0
				if event.key == pygame.K_SPACE:
					screen.fill((0,0,0))
					loop = 0
		pygame.display.update()
		clock.tick(60)


#Game Running 
run = True
while run:

	draw_screen()
	draw_score()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and direction != 3:
				direction = 1
			if event.key == pygame.K_RIGHT and direction != 4:
				direction = 2
			if event.key == pygame.K_DOWN and direction != 1:
				direction = 3
			if event.key == pygame.K_LEFT and direction != 2:
				direction  = 4
			if event.key == pygame.K_SPACE:
				pause()
		
	#create food
	if new_food == True:
		new_food = False
		food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)
		food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)
	
	#draw food
	pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))


	#check if food has been eaten
	if snake_pos[0] == food:
		new_food = True
		#create a new piece at the last point of the snake's tail
		new_piece = list(snake_pos[-1])
		#add an extra piece to the snake
		if direction == 1:
			new_piece[1] += cell_size
		#heading down
		if direction == 3:
			new_piece[1] -= cell_size
		#heading right
		if direction == 2:
			new_piece[0] -= cell_size
		#heading left
		if direction == 4:
			new_piece[0] += cell_size
		
		#attach new piece to the end of the snake
		snake_pos.append(new_piece)

		#increase score
		score += 1



	if game_over == False:
		#update snake
		if update_snake > 99:
			update_snake = 0
			#first shift the positions of each snake piece back.
			snake_pos = snake_pos[-1:] + snake_pos[:-1]
			#now update the position of the head based on direction
			#heading up
			if direction == 1:
				snake_pos[0][0] = snake_pos[1][0]
				snake_pos[0][1] = snake_pos[1][1] - cell_size
			#heading down
			if direction == 3:
				snake_pos[0][0] = snake_pos[1][0]
				snake_pos[0][1] = snake_pos[1][1] + cell_size
			#heading right
			if direction == 2:
				snake_pos[0][1] = snake_pos[1][1]
				snake_pos[0][0] = snake_pos[1][0] + cell_size
			#heading left
			if direction == 4:
				snake_pos[0][1] = snake_pos[1][1]
				snake_pos[0][0] = snake_pos[1][0] - cell_size
			game_over = check_game_over(game_over)
		

	if game_over == True:
		draw_game_over()
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			clicked = False
			#reset variables
			game_over = False
			update_snake = 0
			food = [0, 0]
			new_food = True
			new_piece = [0, 0]
			#define snake variables
			snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
			snake_pos.append([300,310])
			snake_pos.append([300,320])
			snake_pos.append([300,330])
			direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
			score = 0



	head = 1
	for x in snake_pos:

		if head == 0:
			pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
			pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
		if head == 1:
			pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
			pygame.draw.rect(screen, (255,0,0), (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
			head = 0

	pygame.display.update()

	update_snake += 1

pygame.quit()
