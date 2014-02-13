import random, sys, time, math, pygame
from pygame.locals import *

FPS = 60 # frames per second to update the screen
WINWIDTH = 1000 # width of the program's window, in pixels
WINHEIGHT = 1000 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

def main():
    global FPS, FPSCLOCK, WINHEIGHT, WINWIDTH, HALF_WINHEIGHT, HALF_WINWIDTH, DISPLAYSURF
    global green, white

    green = (140, 148, 64)
    white = (197, 200, 198)

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('DoodleJump with BOXES !')

    
    FPSCLOCK = pygame.time.Clock()

    global platforms
    platforms = Platforms()
    
    global player
    player = Player()

    while True:

        runGame()
        


def runGame():

    DISPLAYSURF.fill(white)
    player.live()
    platforms.live()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            # stop moving the player's squirrel
            if event.key in (K_LEFT, K_a):
                player.moveLeft = True
            elif event.key in (K_RIGHT, K_d):
                player.moveRight = True
            elif event.key in (K_UP, K_w):
                player.moveUp = True
            elif event.key in (K_DOWN, K_s):
                player.moveDown = True

        elif event.type == KEYUP:
            # stop moving the player's squirrel
            if event.key in (K_LEFT, K_a):
                player.moveLeft = False
            elif event.key in (K_RIGHT, K_d):
                player.moveRight = False
            elif event.key in (K_UP, K_w):
                player.moveUp = False
            elif event.key in (K_DOWN, K_s):
                player.moveDown = False

            elif event.key == K_ESCAPE:
                terminate()

    pygame.display.update()
    FPSCLOCK.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()


""" The player class """
class Player:

    def __init__(self):
        self.size = 25
        self.x = WINWIDTH / 3 - 50 #center x
        self.y = WINHEIGHT / 2 #center y
        self.rectangle = Rect(0, 0, self.size, self.size)
        self.rectangle.center = (self.x, self.y)
        self.yvel = 0
        self.gravity = .4
        self.terminalvelocity = 13
        self.jumpvel = 10
        self.score = 0
        self.isalive = True
        self.time = 0
        self.moveDown = 0
        self.moveUp = 0
        self.moveRight = 0
        self.moveLeft = 0

        self.direction = ""
        

    def move(self):
        # We check the movements :
        if(self.moveRight):
            self.rectangle.x += 2
        if(self.moveLeft):
            self.rectangle.x -= 2
        if(self.moveUp):
            self.rectangle.y -= 2
        if(self.moveDown):
            self.rectangle.y += 2

        pygame.draw.rect(DISPLAYSURF, green, self.getrect())

        self.yvel -= self.gravity
        if abs(self.yvel) >= self.terminalvelocity:
            self.yvel = -self.terminalvelocity
        self.rectangle.y -= self.yvel
        
        if self.time != 0:
            self.time += 1
            if self.time >= 2:
                self.time = 0

        if self.rectangle.collidelist(platforms.platforms_list) > -1:
            self.startjump()


    def startjump(self):
        if self.time == 0:
            self.yvel = self.jumpvel
            self.time += 1
            

    def go_up(self):
        self.rectangle.y -= 2       

    def go_down(self):
        self.rectangle.y += 2

    def getrect(self):
        return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)

    def live(self):
        self.move()



""" Class platforms """
class Platforms:

    def __init__(self):
        self.platforms_list = list()
        self.populate_platforms()

    def populate_platforms(self):

        for i in range(random.randint(30,40)):
            p = Rect((random.randint(0, WINWIDTH), random.randint(0, WINHEIGHT)), (60, 10))
            
            while p.collidelist(self.platforms_list) != -1:
                p.x = random.randint(0, WINWIDTH) 
                p.y = random.randint(0, WINHEIGHT)

            pygame.draw.rect(DISPLAYSURF, green, p)
            self.platforms_list.append(p)

    def live(self):
        for p in self.platforms_list:
            pygame.draw.rect(DISPLAYSURF, green, p)


main()