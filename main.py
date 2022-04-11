#importing libraries
from msvcrt import setmode
from xmlrpc.client import boolean
import pygame
import pygame.locals
import time
import random
import pygame_menu

#libraries initialization
pygame.init()
pygame.mixer.init()

#Global Variables
windowSize = (1080,720)
objectSize = 20
speed = 0.1

#colors
white = (255,255,255)
#score font
scoreFont = (255, 217, 217)

#declaring font object
font = pygame.font.SysFont('arial', 30)

#initilizing game window
surface = pygame.display.set_mode(windowSize)

#initialiing game menu
menu = pygame_menu.Menu('Welcome', 1080, 720,theme=pygame_menu.themes.THEME_BLUE)

class Menu:
    def set_difficulty(self,value, difficulty):
        global speed
        speed = difficulty
    def start_the_game(self):
        game = Game()
        game.run()
    def menu(self):
        menu.add.text_input('Name :', default='PLAYER')
        menu.add.button('Play', self.start_the_game)
        menu.add.selector('Difficulty :', [('Easy', 0.1),('Medium', 0.06),('Hard', 0.03)], onchange=self.set_difficulty)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)

class Apple:
    def __init__(self):
        self.apple = pygame.image.load("media/apple.png").convert_alpha()
        self.x = objectSize * 3
        self.y = objectSize * 3    
    def draw(self):
        surface.blit(self.apple,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.x = random.randint(0,53)*objectSize
        self.y = random.randint(0,35)*objectSize

class Snake:
    def __init__(self, length):
        self.block = pygame.image.load("media/block.jpg").convert()
        self.x = [objectSize]*length
        self.y = [objectSize]*length
        self.direction = 'right'
        self.length = length
    def increaseLength(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    def draw(self):
        for i in range(self.length):
            surface.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    def moveLeft(self):
        if self.direction != 'right':
            self.direction = 'left'
    def moveRight(self):
        if self.direction != 'left':
            self.direction = 'right'
    def moveUp(self):
        if self.direction != 'down':
            self.direction = 'up'
    def moveDown(self):
        if self.direction != 'up':
            self.direction = 'down'
    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= objectSize
        if self.direction == 'down':
            self.y[0] += objectSize
        if self.direction == 'left':
            self.x[0] -= objectSize
        if self.direction == 'right':
            self.x[0] += objectSize
        self.draw()           

class Game:
    def __init__(self):
        self.bgMusic()
        self.snake = Snake(3)
        self.apple = Apple()
        self.apple.draw()       
        self.snake.draw()
    def checkCollision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + objectSize:
            if y1 >= y2 and y1 < y2 + objectSize:
                return True
        return False
    def checkWallCollision(self, x,y):
        if x<0 or x>1080 or y<0 or y>720:
            return True
    def bgMusic(self):
        pygame.mixer.music.load("media/gameSound.mp3")
        pygame.mixer.music.play()
    def renderBackground(self):
        bg = pygame.image.load("media/background1.jpg")
        surface.blit(bg, (0,0))
    def play(self):
        self.renderBackground()
        self.apple.draw()
        self.snake.move()
        self.displayScore()
        pygame.display.flip()
        #snake colliding with apple
        if self.checkCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("media/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increaseLength()
            self.apple.move()
        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.checkCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("media/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"
        #snake colliding with wall
        if self.checkWallCollision(self.snake.x[0], self.snake.y[0]):
            raise "Game Over"
    def displayScore(self):
        score = font.render(f"Score: {(self.snake.length-3)*10}", True, scoreFont)
        surface.blit(score, (800,10))
    def showGameOver(self):
        self.renderBackground()
        line1 = font.render(f"Game Over...!  Your Score is {(self.snake.length-3)*10}", True, white)
        surface.blit(line1, (290,280))
        line2 = font.render(f"Press Enter To Continue...", True, white)
        surface.blit(line2, (290,380))
        pygame.display.flip()
        pygame.mixer.music.pause()
    def reset(self):
        self.snake = Snake(3)
        self.apple = Apple()
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        running = False
                    if event.key == pygame.K_RETURN and pause:
                        running = False
                        menu.reset_value()
                    if not pause:
                        if event.key == pygame.K_UP:
                            self.snake.moveUp()
                        if event.key == pygame.K_DOWN:
                            self.snake.moveDown()
                        if event.key == pygame.K_LEFT:
                            self.snake.moveLeft()
                        if event.key == pygame.K_RIGHT:
                            self.snake.moveRight()
                elif event.type == pygame.QUIT:
                    exit(0)
            try:
                if not pause:
                    self.play()
            except:
                self.showGameOver()
                pause = True
                self.reset()
            time.sleep(speed)            
if __name__ == "__main__":
    obj = Menu()
    obj.menu()