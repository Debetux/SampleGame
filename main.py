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
    camera = Camera(complex_camera, WINWIDTH, WINHEIGHT)

    entities = pygame.sprite.Group() # Group all our entities (platform, player)
    entities.add(player)
    platforms_list = list()

    up = down = left = right = running = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(Color("#BEEDFD"))


    """ Populate platforms """
    for iy in range(-WINHEIGHT, WINHEIGHT, random.randint(40, 50)):

        for ix in range(0, WINWIDTH, random.randint(70, 80)):
            if(random.randint(0,5) == 1):
                p = Platform()
                p.rect.x = ix + random.randint(-10,10)
                p.rect.y = iy + random.randint(-10, 10)

                entities.add(p)
                platforms_list.append(p)
        

        # while p.collidelist(self.platforms_list) != -1:
        #     p.x = random.randint(0, WINWIDTH) 
        #     p.y = random.randint(0, WINHEIGHT)

        # pygame.draw.rect(DISPLAYSURF, green, p)
        # self.platforms_list.append(p)

    
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
        # entities.draw(screen)
        for e in entities:
             screen.blit(e.image, camera.apply(e))
        # ... and platforms
        

        # Make player live
        player.update(platforms_list)

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

        self.image = pygame.Surface((10,10))
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


        """ Manage the case when the rect is out of the screen """
        out_left = self.rect.topleft[0]
        out_right = self.rect.topright[0] - WINWIDTH

        
        screen = pygame.display.get_surface()

        if out_right > 0:
            newrect = self.rect.copy()
            newrect.x = out_right - self.rect.width
            pygame.draw.rect(screen, Color("#FF8A00"), newrect)
            
            if(out_right - self.rect.width) > 0:
                self.rect.x = out_right - self.rect.width

        elif out_left < 0:
            newrect = self.rect.copy()
            newrect.x = WINWIDTH + out_left
            pygame.draw.rect(screen, Color("#FF8A00"), newrect)

            if abs(out_left) > self.rect.width:
                self.rect.x = WINWIDTH + out_left
        """ End """  
        
        collide_platform = pygame.sprite.spritecollideany(self, platforms_list)

        for platform in platforms_list:
            if pygame.sprite.collide_rect(self, platform) and self.yvel < 0:

                # pygame.draw.line(screen, (255,255,0), (0, self.rect.y), (WINWIDTH, self.rect.y))
                # pygame.draw.line(screen, (255,255,0), (0, platform.rect.y), (WINWIDTH, platform.rect.y))

                # pygame.draw.rect(screen, (0,0,0), (0, 0, WINWIDTH, WINHEIGHT))
                # print("Collision detected, waiting 1 sec...")
                # print('self.rect', self.rect, 'platform.rect', platform.rect)
                # time.sleep(0.5)
                self.startjump()






    def startjump(self):
        if self.time == 0:
            self.yvel = self.jumpvel
            self.time += 1


""" Platform """
class Platform(Entity):

    def __init__(self):
        Entity.__init__(self)

        self.image = pygame.Surface((60,10))
        self.image.fill(green)
        self.image.convert()

        self.rect = self.image.get_rect()

    def update(self):
        return None


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