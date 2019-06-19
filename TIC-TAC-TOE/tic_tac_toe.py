import pygame
import sys

pygame.init()

class Piece(pygame.sprite.Sprite) :

	def __init__(self,x,y,pos) :
		self.imagepy_x = pygame.image.load("images/x.png")
		self.imagepy_o = pygame.image.load("images/o.png")
		self.imagepy_transparent = pygame.image.load("images/background_transparent.png")
		self.type_piece = ""
		self.played = False
		self.pos = pos
		self.image = self.imagepy_transparent
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = x,y

	def update(self, display) :

		display.blit(self.image, self.rect)

class Cursor(pygame.Rect) :

	def __init__(self) :

		pygame.Rect.__init__(self,0,0,0,1)

	def update(self, display) :

		self.left, self.top = pygame.mouse.get_pos()

class actor() :

	def __init__(self, f_name) :

		self.turn = False
		self.f_name = f_name

def draw_lines(display) :

	x = 200
	yinitiate = 100
	yfinal = 400 

	for i in range(0,2) :

		pygame.draw.line(display, (0,0,0),(x,yinitiate),(x,yfinal),1)
		x += 100

	xyfinal = 200
	for i in range(0,2) :

		pygame.draw.line(display, (0,0,0),(100,xyfinal),(400,xyfinal),1)
		xyfinal += 100

def play(cursor, segment, actor1, actor2, game_result, innings) :

	sound_push = pygame.mixer.Sound("music/push.wav")
	cond_sound_push = False

	if cursor.colliderect(segment.rect) :

		if actor1.turn == True  and segment.played == False:


			segment.image = segment.imagepy_x
			segment.type_piece = "x"
			actor1.turn = False
			actor2.turn = True
			segment.played = True
			game_result[segment.pos[0]][segment.pos[1]] = segment.type_piece
			cond_sound_push = check_sound(sound_push, cond_sound_push)
			innings += 1

		if actor2.turn == True  and segment.played == False:

			segment.image = segment.imagepy_o
			segment.type_piece = "o"
			actor1.turn = True
			actor2.turn = False
			segment.played = True
			game_result[segment.pos[0]][segment.pos[1]] = segment.type_piece
			cond_sound_push = check_sound(sound_push, cond_sound_push)
			innings += 1
	
	return innings

def check_structure(game_result) :

	# horinzontally

	for x in range(0,3) :

		if (game_result[x][0] == game_result[x][1] == game_result[x][2]) and game_result[x][0] != "." :

			return game_result[x][0]

	# vertically

	for x in range(0,3) :

		if (game_result[0][x] == game_result[1][x] == game_result[2][x]) and game_result[0][x] != "." :

			return game_result[0][x]

	# diagonally

	# principal diagonal

	if(game_result[0][0] == game_result[1][1] == game_result[2][2]) and game_result[0][0] != "." :

		return game_result[0][0]

	#check secundary diagonal
	if(game_result[0][2] == game_result[1][1] == game_result[2][0]) and game_result[0][2] != "." :
		
		return game_result[0][2]

	# else return draw
	return "."

class button(pygame.sprite.Sprite) :

	def __init__(self, imagepy1, imagepy2, x = 200, y = 200) :

		self.imagepy_normal = imagepy1
		self.imagepy_seleccion = imagepy2
		self.rect = self.imagepy_normal.get_rect()
		self.rect.left, self.rect.top = x,y 
		self.imagepy_actual = self.imagepy_normal

	def update(self, display, cursor) :

		if cursor.colliderect(self.rect) :

			self.imagepy_actual = self.imagepy_normal

		else :

			self.imagepy_actual = self.imagepy_seleccion

		display.blit(self.imagepy_actual, self.rect)


def check_winner(game_result, innings) :

	winner = check_structure(game_result)

	if winner != "." :

		return winner

	if innings == 9 :

		if winner == "." :

			return winner

	return "none"

def show_menu(display,cursor,buttones) :

	for button in buttones :

		button.update(display, cursor)

	source = pygame.font.Font("fonts/Pacifico.ttf",30)

	text_title = source.render("TIC TAC TOE GAME",0,(0,0,255))

	#display.blit(text_title, (50,35))

	image_title = pygame.image.load("images/Tic_tac_toe.png")

	display.blit(image_title, (75,100))

	cursor.update(display)

def check_sound(sound1, cond) :

	if cond == False :

		sound1.play()

	cond = True

	return cond

def main() :

	pygame.init()

	display = pygame.display.set_mode([500,600])
	pygame.display.set_caption("TIC TAC TOE")
	image_game_icon = pygame.image.load("images/icon.png")
	pygame.display.set_icon(image_game_icon)


	cursor1 = Cursor()

	# Pieces
	xpiece = 110
	piece1 = Piece(110,110,[0,0])
	piece2 = Piece(215,110,[0,1])
	piece3 = Piece(310,110,[0,2])
	piece4 = Piece(110,210,[1,0])
	piece5 = Piece(215,210,[1,1])
	piece6 = Piece(310,210,[1,2])
	piece7 = Piece(110,310,[2,0])
	piece8 = Piece(215,310,[2,1])
	piece9 = Piece(310,310,[2,2])

	# Players

	player1 = actor("X")
	player2 = actor("Y")

	player1.turn = True

	reloj = pygame.time.Clock()
	quit = False

	# data structure of the game

	game_result = [[".",".","."],[".",".","."],[".",".","."]]

	# aux

	winner = ""
	innings = 0

	# Fonts

	font_type = pygame.font.Font("fonts/atarian.ttf", 35)
	font_type2 = pygame.font.Font("fonts/atarian.ttf", 60)
	text_actor1 = font_type.render(" Player 1 :" + player1.f_name, 0,(0,0,255))
	text_actor2 = font_type.render("Payer 2: " + player2.f_name, 0,(0,0,255))
	text_play_again = font_type.render("Press Space To Pay Again...",0,(0,0,255))
	#images 

	imagepy_button_startgame = pygame.image.load("images/playbutton.png")
	imagepy_button_startgame_hover = pygame.image.load("images/playbutton_hover.png")
	imagepy_button_quit = pygame.image.load("images/playbutton1.png")
	imagepy_button_quit_hover = pygame.image.load("images/playbutton1_hover.png")
	button1 = button(imagepy_button_startgame, imagepy_button_startgame_hover, 75,400)
	button2 = button(imagepy_button_quit, imagepy_button_quit_hover,275,400)
	
	# sounds

	main_channel = pygame.mixer.Channel(5)
	sound_winner = pygame.mixer.Sound("music/winner.wav")
	sound_draw = pygame.mixer.Sound("music/draw.wav")

	#conds scenes
	cond_menu = True
	cond_game = False
	cond_gameover = False

	# cons sound
	cond_sound_principal = False
	cond_sound_winner = False
	cond_sound_draw = False

	while quit != True :

		for event in pygame.event.get() :

			if event.type == pygame.QUIT :

				quit = True
			
			if event.type == pygame.MOUSEBUTTONDOWN :

				# if click and collide with the background
				if winner == "none" :
					innings = play(cursor1, piece1, player1, player2, game_result, innings)
					innings = play(cursor1, piece2, player1, player2, game_result, innings)
					innings = play(cursor1, piece3, player1, player2, game_result, innings)
					innings = play(cursor1, piece4, player1, player2, game_result, innings)
					innings = play(cursor1, piece5, player1, player2, game_result, innings)
					innings = play(cursor1, piece6, player1, player2, game_result, innings)
					innings = play(cursor1, piece7, player1, player2, game_result, innings)
					innings = play(cursor1, piece8, player1, player2, game_result, innings)
					innings = play(cursor1, piece9, player1, player2, game_result, innings)

				if cond_menu == True :

					if cursor1.colliderect(button1.rect) :

						cond_game = True
						cond_menu = False
					if cursor1.colliderect(button2) :

						pygame.quit()
						# quit del programa
						sys.exit(0)

			# play again option
			if event.type == pygame.KEYDOWN :
				
				if event.key == pygame.K_SPACE :
					
					if cond_gameover == True :

						cond_gameover = False
						piece1.image = piece1.imagepy_transparent
						piece1.played = False
						piece2.image = piece2.imagepy_transparent
						piece2.played = False
						piece3.image = piece3.imagepy_transparent
						piece3.played = False
						piece4.image = piece4.imagepy_transparent
						piece4.played = False
						piece5.image = piece5.imagepy_transparent
						piece5.played = False
						piece6.image = piece6.imagepy_transparent
						piece6.played = False
						piece7.image = piece7.imagepy_transparent
						piece7.played = False
						piece8.image = piece8.imagepy_transparent
						piece8.played = False
						piece9.image = piece9.imagepy_transparent
						piece9.played = False

						game_result = [[".",".","."],[".",".","."],[".",".","."]]
						innings = 0
						winner = "none"
						player1.turn = True
						player2.turn = False
						cond_sound_winner = False
						cond_sound_draw = False

					# if user press space and the music has no finish
					if main_channel.get_busy() == True :

						main_channel.stop()

					#pygame.mixer.music.rewind()
					#pygame.mixer.music.play()

		reloj.tick(20)
		display.fill((255,255,255))

		if cond_menu == True :

			show_menu(display, cursor1, [button1, button2])

		if cond_game == True :

			if cond_sound_principal == False :
				pygame.mixer.music.load("music/principal.mp3")
				pygame.mixer.music.play()
				cond_sound_principal = True
			cursor1.update(display)
			draw_lines(display)
			display.blit(text_actor1,(50,445))
			display.blit(text_actor2,(270,445))

			piece1.update(display)
			piece2.update(display)
			piece3.update(display)
			piece4.update(display)
			piece5.update(display)
			piece6.update(display)
			piece7.update(display)
			piece8.update(display)
			piece9.update(display)

			# check the game result to see if there is a winner
			winner = check_winner(game_result, innings)

			if winner != "none" :

				if winner == "x" :

					text_winner = font_type2.render("winner :"+ player1.f_name,0,(255,0,0))
					display.blit(text_winner,(50,500))

				if winner == "o" :

					text_winner = font_type2.render("winner :" + player2.f_name, 0,(255,0,0))
					display.blit(text_winner,(45,500))

				if winner != "." :

					if cond_sound_winner == False :

						pygame.mixer.music.stop()
						main_channel.play(sound_winner)
						cond_sound_winner = True
				

				if winner == "." :

					text_winner = font_type2.render("Draw!!!!!", 0,(255,0,0))
					display.blit(text_winner,(175,500))
					pygame.mixer.music.stop()

					if cond_sound_draw == False :
						main_channel.play(sound_draw)
						cond_sound_draw = True


				display.blit(text_play_again,(100,20))
				cond_gameover = True

		
		pygame.display.update()

		

	pygame.quit()

main()
