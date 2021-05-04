#!/usr/bin/env python3

'''
G3 Final Project
Hayden Walker 2021-05-03

A game in which the goal is to play as a UFO and collect
'wellness items' while avoiding 'bad habits'.
'''

import pygame # Import the Pygame graphics library
import random # Import the random number library

class Character:
	'''
	Character class
	Defines an object with health that can move
	'''
	def __init__(self, x, y, vx, vy):
		'''
		Initialize the Character class
		'''
		# Set position
		self.x = x
		self.y = y
		
		# Set velocity
		self.vx = vx
		self.vy = vy
		
		# Set health
		self.hp = 100

	def move(self):
		'''
		Move the character according to velocity and position
		'''
		# Check for edge in x direction
		if ((self.x > 0) and (self.x < 400)) or ((self.x == 0) and (self.vx > 0)) or ((self.x == 400) and (self.vx < 0)):
			self.x += self.vx # If no edge is present, move
		
		# Check for edge in y direction
		if ((self.y > 0) and (self.y < 425)) or ((self.y == 0) and (self.vy > 0)) or ((self.y == 425) and (self.vy < 0)):
			self.y += self.vy # If no edge is present, move

class G3UFO(Character):
	'''
	UFO class
	Defines a player-controlled object
	'''
	def __init__(self, x, y, vx, vy):
		'''
		Initialize the UFO class
		'''
		# Initialize parent class Character
		Character.__init__(self, x, y, vx, vy)
		
		# Load left, right, and stationary sprites
		self.left = pygame.image.load("sprites/UFOLeft.png")
		self.right = pygame.image.load("sprites/UFORight.png")
		self.stop = pygame.image.load("sprites/UFOStop.png")
		
		# Set score (items collected) to 0
		self.score = 0
	
	def draw(self):
		'''
		Draw the object on-screen at its current position
		'''
		if self.vx < 0:
			# If moving left, draw left sprite
			win.blit(self.left, (self.x, self.y))
		elif self.vx > 0:
			# If moving right, draw right sprite
			win.blit(self.right, (self.x, self.y))
		else:
			# If stopped, draw stationary sprite
			win.blit(self.stop, (self.x, self.y))
		
class PowerUp:
	'''
	Powerup class for wellness items
	Defines an item with a position that can tell when the player is touching it
	'''
	def __init__(self, x, y, sprite):
		'''
		Initialize the PowerUp class
		'''
		# Position
		self.x = x
		self.y = y
		
		# Availability (not yet touched by player)
		self.available = True
		
		# Load sprite
		self.sprite = pygame.image.load(sprite)
	
	def checkBounds(self, charX, charY):
		'''
		Given the player's coordinates, check if the powerup is touching the player
		'''
		# Return boolean
		return ((self.x in range(charX, charX + 100)) and (self.y in range(charY, charY + 100)) and (self.available))
	
	def draw(self):
		'''
		Draw the powerup's sprite to the screen at its current position
		'''
		# Only draw if the player has not touched it yet
		if self.available:
			win.blit(self.sprite, (self.x, self.y))

class BadHabit(PowerUp):
	'''
	Bad habit class that extends powerups
	Defines a powerup that can move
	'''
	def __init__(self, x, y, sprite):
		'''
		Initialize the BadHabit class
		'''
		# Initialize parent class PowerUp
		PowerUp.__init__(self, x, y, sprite)
		
		# Two possible velocities, one per direction
		speeds = [1, -1]
		
		# Randomly pick velocity in each direction
		self.vx = speeds[random.randint(0, 1)]
		self.vy = speeds[random.randint(0, 1)]

	def move(self):
		'''
		Move the bad habit according to its velocity and position
		'''
		# Check for edge in x direction
		if ((self.x > 0) and (self.x < 500)) or ((self.x <= 0) and (self.vx > 0)) or ((self.x >= 500) and (self.vx < 0)):
			self.x += self.vx # If not on edge, move
		else:
			self.vx *= -1 # If on edge, switch direction
		
		# Check for edge in y direction
		if ((self.y > 0) and (self.y < 500)) or ((self.y <= 0) and (self.vy > 0)) or ((self.y >= 500) and (self.vy < 0)):
			self.y += self.vy # If not on edge, move
		else:
			self.vy *= -1 # If on edge, switch direction

def drawsc():
	'''
	Update the screen; draw and update all entities and statts.
	'''
	# Clear the screen
	win.fill((255,255,0))
	
	# Move and draw the UFO
	ufo.move()
	ufo.draw()
	
	# Draw powerups
	for powerup in powerUpItems:
		# Check if the player is touching a power up
		if powerup.checkBounds(ufo.x, ufo.y):
			powerup.available = False # Make power up disappeas
			ufo.score += 1 # Award a point
		# Draw the powerup
		powerup.draw()
	
	# Draw bad habits
	for badHabit in badHabitItems:
		# Check if the player is touching a bad habit
		if badHabit.checkBounds(ufo.x, ufo.y):
			badHabit.available = False # Make it disappear
			ufo.hp -= 20 # Subtract health
		# Update and draw the bad habit
		badHabit.move()
		badHabit.draw()
	
	# Draw the stats
	displayStats()
	
	# Update the screen
	pygame.display.update()

def displayStats():
	'''
	Displays the player's health and score at the top of the screen
	'''
	win.blit(messagerender('HP: ' + str(ufo.hp) + ' Items: ' + str(ufo.score) + " / " + str(maxPowerUps)), (0, 0))

def checkWin():
	'''
	Check if the player has won
	'''
	didWin = True
	for powerUp in powerUpItems:
		# If any powerup is still available, player did not win
		if powerUp.available:
			didWin = False
	return didWin # Return boolean

def checkLose():
	'''
	Check if the player has lost
	'''
	return (ufo.hp == 0) # Return boolean

def messagerender(message):
	'''
	Render a message for use with win.blit()
	'''
	return myfont.render(message, False, (0, 0, 0))

def splashscreen():
	'''
	Opening splash screen
	'''
	win.fill((255,255,0)) # Clear screen
	
	# Red title text
	title = myfont.render("Hayden Walker's G3 Project", False, (255, 0, 0))
	win.blit(title, (5, 50))
	
	# Display each line of message
	win.blit(messagerender("Guide the UFO with the"), (5, 100))
	win.blit(messagerender("arrow keys."), (5, 150))
	win.blit(messagerender("Collect all wellness items."), (5, 200))
	win.blit(messagerender("Avoid bad habits and"), (5, 250))
	win.blit(messagerender("negativity."), (5, 300))
	win.blit(messagerender("Press SPACE to begin."), (5, 350))
	
	# Update the screen
	pygame.display.update()
	# Pause until a key is pressed
	gameHang()

def winGame():
	'''
	Screen for when the player has won
	'''
	win.fill((255,255,0)) # Clear the screen
	
	# Display each line of message
	win.blit(messagerender("You won!"), (5, 50))
	win.blit(messagerender("Press SPACE to play again."), (5, 100))
	win.blit(messagerender("Press ESC for title screen."), (5, 150))
	
	# Update the screen
	pygame.display.update()
	# Pause until a key is pressed
	gameHang()

def loseGame():
	'''
	Screen for when the player has lost
	'''
	win.fill((255,255,0)) # Clear the screen

	# Display each line of message
	win.blit(messagerender("You lost."), (5, 50))
	win.blit(messagerender("Press SPACE to play again."), (5, 100))
	win.blit(messagerender("Press ESC for title screen."), (5, 150))
	
	# Update the screen
	pygame.display.update()
	# Pause until a key is pressed
	gameHang()

def gameHang():
	'''
	Pause the game until either SPACE or ESCAPE are pressed, or window is closed
	'''
	while True:
		for event in pygame.event.get():
			# Check for quit
			if event.type == pygame.QUIT:
				quit()
			# Check for key press
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					startGame() # Space starts game
				if event.key == pygame.K_ESCAPE:
					splashscreen() # Escape shows main menu

def startGame():
	'''
	This function initializes all variables and starts the game loop
	'''
	# Create global variables
	global ufo
	global powerUpItems
	global maxPowerUps
	global badHabitItems

	# Initialize Mrs. Bennett
	ufo = G3UFO(100, 100, 0, 0)
	
	# Initialize powerups
	maxPowerUps = 5
	powerUpItems = list()
	powerUpSprites = ["sprites/water.png", "sprites/book.png", "sprites/salad.png"]
	for powerUp in range(maxPowerUps):
		powerUpItems.append(PowerUp(random.randint(0, 450), random.randint(0, 450), powerUpSprites[random.randint(0, len(powerUpSprites) - 1)]))
	
	# Initialize bad habits
	maxBadHabits = 5
	badHabitItems = list()
	badHabitSprites = ["sprites/pepsi.png", "sprites/netflix.png", "sprites/sad.png"]
	for badHabit in range(maxBadHabits):
		badHabitItems.append(BadHabit(random.randint(0, 450), random.randint(0, 450), badHabitSprites[random.randint(0, len(badHabitSprites) - 1)]))

	while True:
		'''
		The main game loop
		'''
		for event in pygame.event.get():
				# Check for quit
				if event.type == pygame.QUIT:
					quit()
				# Check for arrow keys
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						ufo.vx = -2
					if event.key == pygame.K_RIGHT:
						ufo.vx = 2
					if event.key == pygame.K_DOWN:
						ufo.vy = 2
					if event.key == pygame.K_UP:
						ufo.vy = -2
				# If no key is pressed, UFO is stationary
				else:
					ufo.vx, ufo.vy = 0, 0
		
		# Check if the player has won
		if checkWin():
			winGame()
		
		# Check if the player has lost
		if checkLose():
			loseGame()
		
		# Update and redraw the screen
		drawsc()
		
		# Delay 5ms
		pygame.time.delay(5)

if __name__ == '__main__':
	'''
	If the program is run, initialize window and call title screen
	'''
	# Initialize PyGame and setup the window
	pygame.init()
	win = pygame.display.set_mode((500, 500))
	pygame.display.set_caption("Hayden's G3 Final Project")
	
	# Initialize font
	myfont = pygame.font.SysFont('Monospace', 30)
	
	# Call the title screen
	splashscreen()
