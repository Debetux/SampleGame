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
    chimp = Chimp()

    entities = pygame.sprite.Group() # Group all our entities (platform, player)
    entities.add(player)

    up = down = left = right = running = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(Color("#BEEDFD"))

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

        entities.draw(screen)
        entities.update()
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
        self.image = pygame.Surface((60,60))
        self.image.fill(Color("#A5494F"))
        self.image.convert()

        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        # self.rect.midtop = pos
        self.rect.move_ip(pos)

        return None


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        

    def update(self):
        return None

main()