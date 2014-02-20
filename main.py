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
    platform = Platforms()

    entities = pygame.sprite.Group() # Group all our entities (platform, player)
    entities.add(player)

    up = down = left = right = running = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(Color("#BEEDFD"))

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                # start moving the player
                if event.key in (K_LEFT, K_a):
                    player.left = True
                elif event.key in (K_RIGHT, K_d):
                    player.right = True
                elif event.key in (K_UP, K_w):
                    player.up = True
                elif event.key in (K_DOWN, K_s):
                    player.down = True

            elif event.type == KEYUP:
                # stop moving the player
                if event.key in (K_LEFT, K_a):
                    player.left = False
                elif event.key in (K_RIGHT, K_d):
                    player.right = False
                elif event.key in (K_UP, K_w):
                    player.up = False
                elif event.key in (K_DOWN, K_s):
                    player.down = False

                elif event.key == K_ESCAPE:
                    terminate()

        # Reset image with the background
        screen.blit(background, (0, 0))

        # Draw entities
        entities.draw(screen)
        # ... and platforms
        platform.update()

        # Make them live
        entities.update()

        # Flip the images
        pygame.display.flip()
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

        self.left = self.right = self.up = self.down = False

        self.image = pygame.Surface((60,60))
        self.image.fill(Color("#FF8A00"))
        self.image.convert()

        self.rect = self.image.get_rect()

    def update(self):
        if(self.right):
            self.rect.x += 2
        if(self.left):
            self.rect.x -= 2
        if(self.up):
            self.rect.y -= 2
        if(self.down):
            self.rect.y += 2


""" Platforms """
class Platforms(Entity):

    def __init__(self):
        Entity.__init__(self)

        self.platforms_list = list()
        self.populate_platforms()

    def populate_platforms(self):

        for i in range(random.randint(60,70)):
            p = Rect((random.randint(0, WINWIDTH), random.randint(0, WINHEIGHT)), (60, 10))
            
            while p.collidelist(self.platforms_list) != -1:
                p.x = random.randint(0, WINWIDTH) 
                p.y = random.randint(0, WINHEIGHT)

            #pygame.draw.rect(DISPLAYSURF, green, p)
            self.platforms_list.append(p)

    def update(self):
        p = None
        screen = pygame.display.get_surface()
        for p in self.platforms_list:
            pygame.draw.rect(screen, green, p)

main()