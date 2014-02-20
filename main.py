import random, sys, time, math, pygame
from pygame.locals import *

FPS = 60 # frames per second to update the screen
WINWIDTH = 1000 # width of the program's window, in pixels
WINHEIGHT = 1000 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

def main():
    """ Global vars, and colors """
    global FPS, FPSCLOCK, WINHEIGHT, WINWIDTH, HALF_WINHEIGHT, HALF_WINWIDTH, DISPLAYSURF
    global green, white
    global cameraX, cameraY

    green = (140, 148, 64)
    white = (197, 200, 198)
    """ End of global part """


    """ Init pygame, windows, etc... """
    pygame.init()

    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
    pygame.display.set_caption('DoodleJump with BOXES !')

    clock = pygame.time.Clock()
    """ End of init part """
    

    """ Now, we can start the game : """
    runGame(screen, clock)
        


def runGame(screen, clock):

    player = Player()

    entities = pygame.sprite.Group() # Group all our entities (platform, player)
    entities.add(player)
    
    up = down = left = right = running = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(white)

    screen.blit(background, (0, 0))

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    left = True
                elif event.key in (K_RIGHT, K_d):
                    right = True
                elif event.key in (K_UP, K_w):
                    up = True
                elif event.key in (K_DOWN, K_s):
                    down = True

            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    left = False
                elif event.key in (K_RIGHT, K_d):
                    right = False
                elif event.key in (K_UP, K_w):
                    up = False
                elif event.key in (K_DOWN, K_s):
                    down = False

                elif event.key == K_ESCAPE:
                    terminate()



        pygame.display.update()
        clock.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



""" The player class """
class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(0, 0, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)



""" Platforms, which inherit entity """
class Platforms(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.platforms_list = list()
        self.populate_platforms()

    def populate_platforms(self):

        for i in range(random.randint(30,40)):
            p = Rect((random.randint(0, WINWIDTH), random.randint(0, WINHEIGHT)), (60, 10))
            
            while p.collidelist(self.platforms_list) != -1:
                p.x = random.randint(0, WINWIDTH) 
                p.y = random.randint(0, WINHEIGHT)

            #pygame.draw.rect(DISPLAYSURF, green, p)
            self.platforms_list.append(p)

    def live(self):
        p = None
        #for p in self.platforms_list:
            #pygame.draw.rect(DISPLAYSURF, green, p)


main()