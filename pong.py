import pygame, sys, abc, time

from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 500), 0, 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class Shape(object):

	__metaclass__ = abc.ABCMeta

	"""Abstract class which contains methods and attributes used by all shapes"""
	def __init__(self, x, y, colour):
		self._x = x
		self._y = y
		self._colour = colour

	def getColour(self):
		return self._colour

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def setX(self, newX):
		self._x = newX
		return self._x

	def setY(self, newY):
		self._y = newY
		return self._y
		
	@abc.abstractmethod
	def draw(self):
		return

class Block(Shape):

	def __init__(self, x, y, colour, width, height, score = 0):
		Shape.__init__(self, x, y, colour)
		self._width = width
		self._height = height
		self._score = 0

		#USED ONLY FOR SECOND PLAYER IN MULTIPLAYER
		self._up = False
		self._down = False

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def getScore(self):
		return self._score

	def isUp(self):
		return self._up

	def isDown(self):
		return self._down

	def incrementScore(self):
		self._score += 1
		return self._score

	def toggleUp(self):
		'''
		USED FOR KEYBOARD CONTROLS IN 2 PLAYER MODE
		'''
		self._up = not(self._up)

	def toggleDown(self):
		'''
		USED FOR KEYBOARD CONTROLS IN 2 PLAYER MODE
		'''
		self._down = not(self._down)

	def move(self):
		'''
		USED FOR KEYBOARD CONTROLS IN 2 PLAYER MODE
		'''

		if self.isUp():
			self.setY(self.getY() - 0.75)

		elif self.isDown():
			self.setY(self.getY() + 0.75)


	def catchUp(self, target):
		'''
		USED FOR BOT IN 1 PLAYER MODE
		This function moves the block slightly towards the target's position but not completley
		This can be iterated to make a smooth transition move towards the target as well as control the speed of the bot
		'''

		if self.getY() > target:
			self.setY(self.getY() - 0.7)

		elif self.getY() < target:
			self.setY(self.getY() + 0.7)

	def draw(self):

		#Ensure that the blocks do not leave the window
		if self.getY() < 0:
			self.setY(0)

		if (self.getY() + 100) > 500:
			self.setY(400)
		pygame.draw.rect(screen, self.getColour(), (self.getX(), self.getY(), self.getWidth(), self.getHeight()), 0)

	def drawScore(self, (x, y)):
		font = pygame.font.Font(None, 50)
		text = font.render(str(self.getScore()), 1, WHITE)
		screen.blit(text, (x, y))

	def flash(self):
		'''
		Used when a point is scored

		The player that has lost a point flashes
		'''
		for i in xrange(3):
			screen.fill(BLACK)
			pygame.display.update()
			time.sleep(0.25)
			self.draw()
			pygame.display.update()
			time.sleep(0.25)

	def AI(self, i):
		'''
		The AI for 1 player mode simply works by tracking the ball's y coordinate. To make it easer, the tracking is delayed with i.
		Also, every 4 iterations, it will make a 'dumb' move where it moves to a position that is slightly off towards the ball
		'''

		if i == 1250:
			if self.getY() == int(ball.getY()):
				i = 0
			else:
				self.catchUp(ball.getY())

		elif i % 4 == 0:
			if ball.getVerticalVelocity() == 0.3:
				self.catchUp(self.getY() + 6)

			elif ball.getVerticalVelocity() == -0.3:
				self.catchUp(self.getY() - 6)

			i += 1
		else:

			i += 1

		return i


class Ball(Shape):

	def __init__(self, x, y, colour, radius, horizontalVelocity, verticalVelocity):
		Shape.__init__(self, x, y, colour)
		self._radius = radius
		self._horizontalVelocity = horizontalVelocity
		self._verticalVelocity = verticalVelocity

	def getRadius(self):
		return self._radius

	def getHorizontalVelocity(self):
		return self._horizontalVelocity

	def getVerticalVelocity(self):
		return self._verticalVelocity

	def setHorizontalVelocity(self, newVelocity):
		self._horizontalVelocity = newVelocity
		return self._horizontalVelocity

	def setVerticalVelocity(self, newVelocity):
		self._verticalVelocity = newVelocity
		return self._verticalVelocity

	def checkCollisions(self):

		if (int(self.getX()) == 0):
			#If it hits the left, Give player 2 a point
			p2Block.incrementScore()
			p1Block.flash()
			game.restart()


		if (int(self.getX()) == 800):
			#If it hits the right wall, Give player 1 a point
			p1Block.incrementScore()
			p2Block.flash()
			game.restart()

		if ((int(self.getY()) == 0) or (int(self.getY()) == 500)):
			self.setVerticalVelocity(-(self.getVerticalVelocity()))


		#Detect collisions on the top and bottom of the blocks

		###LEFT BLOCK###
		if ((int(self.getX()) - 10) <= (p1Block.getX()) + (p1Block.getWidth())):
			if ((int(self.getY()) + 10) == (p1Block.getY())) or ((int(self.getY())) == ((p1Block.getY()) + p1Block.getHeight())):
				self.setVerticalVelocity(-(self.getVerticalVelocity()))

		###RIGHT BLOCK###
		if ((int(self.getX()) + 10) >= (p2Block.getX()) + (p2Block.getWidth())):
			if ((int(self.getY()) + 10) == (p2Block.getY())) or ((int(self.getY())) == ((p2Block.getY()) + p2Block.getHeight())):
				self.setVerticalVelocity(-(self.getVerticalVelocity()))	


		#Detect collisions for the sides of the blocks

		###LEFT BLOCK###
		if ((p1Block.getY() <= ((int(self.getY() + 10)))) and ((int(self.getY() + 10)) <= (p1Block.getY() + p1Block.getHeight()))) or ((p1Block.getY() <= ((int(self.getY() - 10)))) and ((int(self.getY() - 10)) <= (p1Block.getY() + p1Block.getHeight()))):
			if (int(self.getX()) - 5) == (p1Block.getX() + p1Block.getWidth()):
				self.setHorizontalVelocity(-(self.getHorizontalVelocity()))

		###RIGHT BLOCK###
		if ((p2Block.getY() <= ((int(self.getY() + 10)))) and ((int(self.getY() + 10)) <= (p2Block.getY() + p2Block.getHeight()))) or ((p2Block.getY() <= ((int(self.getY() - 10)))) and ((int(self.getY() - 10)) <= (p2Block.getY() + p2Block.getHeight()))):
			if (int(self.getX()) + 5) == (p2Block.getX()):
				self.setHorizontalVelocity(-(self.getHorizontalVelocity()))



	def update(self):
		#Update ball's position with reference to the velocities
		self.setX(self.getX() + self.getHorizontalVelocity())
		self.setY(self.getY() + self.getVerticalVelocity())


	def draw(self):
		pygame.draw.circle(screen, self._colour, (int(self.getX()), int(self.getY())), self.getRadius(), 0)

class Game():

	def __init__(self):
		self._multiplayer = False
		self._ready = False

	def drawTick(self):
		pygame.draw.lines(screen, WHITE, False, [(370, 237), (410, 273), (430, 200)], 5)

	def isMultiplayer(self):
		return self._multiplayer

	def menu(self):

		#Renders title
		font = pygame.font.Font(None, 300)
		menu = font.render('PONG', 1, WHITE)
		menuPos = menu.get_rect()
		menuPos.centerx = screen.get_rect().centerx
		screen.blit(menu, menuPos)

		#Renders Start text
		font = pygame.font.Font(None, 100)
		start = font.render('START', 1, WHITE)
		startPos = start.get_rect()
		startPos.midleft = screen.get_rect().midleft
		screen.blit(start, startPos)

		#Renders multiplayer text
		font = pygame.font.Font(None, 75)
		multiplayerText = font.render('MULTIPLAYER', 1, WHITE)
		multiplayerTextPos = multiplayerText.get_rect()
		multiplayerTextPos.midright = screen.get_rect().midright
		screen.blit(multiplayerText, multiplayerTextPos)

		#Renders square next to multiplayer text
		text_position = multiplayerTextPos.midleft
		position = ((text_position[0] - 70), text_position[1] - 25)
		size = (50, 50)
		pygame.draw.rect(screen, WHITE, position + size, 1)


		if self._multiplayer:
			self.drawTick()

	def isReady(self):
		return self._ready


	def toggleMultiplayer(self):
		self._multiplayer = not(self._multiplayer)

	def restart(self):

		'''
		Used when a point has been scored, moves everything to middle positions and starts a new match

		'''

		#place blocks in the middle
		p1Block.setY(250)
		p2Block.setY(250)

		#place ball in middle of 'court'
		ball.setX(400)
		ball.setY(250)

		screen.fill(BLACK)

		p1Block.draw()
		p2Block.draw()
		ball.draw()
		pygame.draw.lines(screen, WHITE, False, [(400, 0), (400, 500)],1)

		p1Block.drawScore((50, 5))
		p2Block.drawScore((730, 5))

		pygame.display.update()

		time.sleep(0.5)

		#change direction of ball to be towards the player that just scored a point
		ball.setHorizontalVelocity(-(ball.getHorizontalVelocity()))
		ball.setVerticalVelocity(-(ball.getVerticalVelocity()))

	def start(self):
		pygame.mouse.set_visible(False)
		self._ready = True



p1Block = Block(0, 0, WHITE, 20, 100)
p2Block = Block(780, 250, WHITE, 20, 100)
ball = Ball(400, 250, GREEN, 5, 0.3, 0.3)
game = Game()


#AI iterator
i = 1

while True:

	screen.fill(BLACK)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if (event.type == MOUSEBUTTONDOWN) and not(game.isReady()) and (event.button == 1):
			#check if the multiplayer button has been pressed
			if (pygame.mouse.get_pos()[0] >= 360) and (pygame.mouse.get_pos()[0] <= 800):
				if (pygame.mouse.get_pos()[1] >= 225) and (pygame.mouse.get_pos()[1] <= 275):
					game.toggleMultiplayer()



			#check if the start button has been pressed
			elif (pygame.mouse.get_pos()[0] >= 0) and (pygame.mouse.get_pos()[0] <= 230):
				if (pygame.mouse.get_pos()[1] >= 212) and (pygame.mouse.get_pos()[1] <= 288):
					game.start()


		#detect if player 2 has pressed any keys
		if (event.type == KEYDOWN) and game.isMultiplayer():
			if event.key == pygame.K_UP:
				p2Block.toggleUp()

			elif event.key == pygame.K_DOWN:
				p2Block.toggleDown()


		if (event.type == KEYUP) and game.isMultiplayer():
			if event.key == pygame.K_UP:
				p2Block.toggleUp()

			elif event.key == pygame.K_DOWN:
				p2Block.toggleDown()			


	if game.isReady():
		screen.fill(BLACK)

		x,y = pygame.mouse.get_pos()

		p1Block.setY(y)

		
		ball.update()

		ball.checkCollisions()

		p1Block.draw()
		p2Block.draw()
		ball.draw()
		pygame.draw.lines(screen, WHITE, False, [(400, 0), (400, 500)],1)

		if game.isMultiplayer() == False:
			i = p2Block.AI(i)

		else:
			p2Block.move()


		p1Block.drawScore((50, 5))
		p2Block.drawScore((730, 5))

		pygame.display.update()

	else:
		game.menu()
		pygame.display.update()

