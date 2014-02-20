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
    global cameraX, cameraY, camera

    green = (140, 148, 64)
    white = (197, 200, 198)
    """ End of global part """


    """ Init pygame, windows, etc... """
    pygame.init()

    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
    pygame.display.set_caption('DoodleJump with BOXES !')

    clock = pygame.time.Clock()
    camera = Camera(simple_camera, WINWIDTH, WINHEIGHT)
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

        camera.update(player)

        # Draw entities
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        # ... and platforms
        platform.update()

        # Make player live
        player.update(platform.platforms_list)

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

        self.yvel = 0
        self.gravity = .4
        self.terminalvelocity = 13
        self.jumpvel = 10
        self.time = 0

        self.left = self.right = self.up = self.down = False

        self.image = pygame.Surface((30,30))
        self.image.fill(Color("#FF8A00"))
        self.image.convert()

        self.rect = self.image.get_rect()
        self.startjump()

    def update(self, platforms_list):

        if(self.right):
            self.rect.x += 3
        if(self.left):
            self.rect.x -= 3
        if(self.up):
            self.rect.y -= 3
        if(self.down):
            self.rect.y += 3

        if(self.rect.bottom >= WINHEIGHT):
            self.rect.bottom = WINHEIGHT
            self.yvel = 0
            self.startjump()

        self.yvel -= self.gravity
        if abs(self.yvel) >= self.terminalvelocity:
            self.yvel = -self.terminalvelocity

        self.rect.y -= self.yvel
        
        
        if self.time != 0:
            self.time += 1
            if self.time >= 2:
                self.time = 0

        # Detect if we need to jump or not :
        collision = self.rect.collidelist(platforms_list)
        if collision > -1 and self.yvel < 0 and self.rect.y <= platforms_list[collision].y:
            self.startjump()





    def startjump(self):
        if self.time == 0:
            self.yvel = self.jumpvel
            self.time += 1


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

            # pygame.draw.rect(DISPLAYSURF, green, p)
            self.platforms_list.append(p)

    def update(self):
        p = None
        screen = pygame.display.get_surface()
        for p in self.platforms_list:
            pygame.draw.rect(screen, green, p)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WINWIDTH, -t+HALF_WINHEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WINWIDTH, -t+HALF_WINHEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-HALF_WINWIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-HALF_WINHEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

main()