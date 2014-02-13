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

    timer = pygame.time.Clock()
    """ End of init part """
    

    """ Now, we can start the game : """
    runGame(screen, timer)
        


def runGame(screen, timer):

    entities = pygame.sprite.Group() # Group all our entities (platform, player)
    player = Player()
    entities.add(player)
    camera = Camera(complex_camera, WINWIDTH, WINHEIGHT)

    while True:


        screen.fill(white)

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

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        timer.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


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
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

""" The player class """
class Player(Entity):

    def __init__(self):
        Entity.__init__(self)
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

        self.image = pygame.Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(0, 0, 32, 32)
        

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

        #pygame.draw.rect(DISPLAYSURF, green, self.getrect())

        self.yvel -= self.gravity
        if abs(self.yvel) >= self.terminalvelocity:
            self.yvel = -self.terminalvelocity
        self.rectangle.y -= self.yvel
        
        if self.time != 0:
            self.time += 1
            if self.time >= 2:
                self.time = 0

        # if self.rectangle.collidelist(platforms.platforms_list) > -1:
        #     self.startjump()


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