""" Name: TD_Tower_Grid v0.07
    Authors: Joel Murphy & Chris Bentley
    Date: August 1, 2013
    Purpose: To try and place the towers into a grid.
"""
    
import pygame, random, math
pygame.init()

screen = pygame.display.set_mode((640, 480))

class PosTower(pygame.sprite.Sprite):
    towerx = 20
    towery = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.rect = self.image.get_rect()
    
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        difx = mousex % 40
        dify = mousey % 40
        if difx > 20:
            difx = difx - 20
            self.towerx = mousex - difx
        elif difx <= 20:
            difx = 20 - difx
            self.towerx = mousex + difx
            
        if dify > 20:
            dify = dify - 20
            self.towery = mousey - dify
        elif dify <= 20:
            dify = 20 - dify
            self.towery = mousey + dify
            
        self.rect.center = (self.towerx, self.towery)
        return self.towerx, self.towery
    
class Tower(pygame.sprite.Sprite):
    
    def __init__(self, shell, towerx, towery):
        self.shell = shell
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = towerx
        self.rect.centery = towery
        self.charge = 5
        
    
    def followMouse(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = self.rect.centerx - mouseX
        dy = self.rect.centery - mouseY
        dy *= -1
        
        radians = math.atan2(dy, dx)
        self.dir = radians * 180 / math.pi
        self.dir += 180
        
        #calculate distance
        self.distance = math.sqrt((dx * dx) + (dy * dy))
    
    def update(self):
        self.shell.pause += self.shell.frames
        if self.shell.pause >= self.shell.delay:
            self.shell.pause = 0
            self.shell.frames = 0
            self.shell.pressed = False
        
        self.followMouse()
        self.shoot()
        #self.checkKeys()
    
    def shoot(self):
        if self.shell.rect.centerx == -100:
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.dir
            self.shell.notFired = False

        
    def checkKeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print "Pressed"
            self.shell.pressed = True
            self.shell.frames = 1
            print pygame.mouse.get_pos()
            if self.shell.rect.centerx == -100:
                self.shell.rect.centerx = self.rect.centerx
                self.shell.rect.centery = self.rect.centery
                print "Shell x,y position: ", self.shell.x, " ", self.shell.y
                print "Shell centerx, centery position: ", self.shell.rect.center
                self.shell.speed = self.charge
                print "Shell speed: ", self.shell.speed
                self.shell.dir = self.dir
                print "Shell direction: ", self.shell.dir
                print "Shell dx: ", self.shell.dx
                print "Shell dy: ", self.shell.dy

class Shell(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        
        self.image = pygame.Surface((10, 10))
        self.image.fill((0xff, 0xff, 0xff))
        self.image.set_colorkey((0xff, 0xff, 0xff))
        pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.image = pygame.transform.scale(self.image, (5, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        
        self.speed = 0
        self.dir =0
        
        self.pressed = False
        self.pause = 0
        self.delay = 5
        self.frames = 0
        
        self.reset()
        print "Initialized"
        
    def update(self):
        #print self.rect.center
        
        self.calcVector()
        self.calcPos()
        self.checkBounds()
        if self.pressed:
            print "Shell at ", self.rect.center
            print "Shell dx and dy: ", self.dx, " ", self.dy
        self.rect.center = (self.x, self.y)
   
    def calcVector(self):
        radians = self.dir * math.pi / 180
        
        self.dx = self.speed * math.cos(radians)
        self.dy = self.speed * math.sin(radians)
        self.dy *= -1
    
    def calcPos(self):
        self.x += self.dx
        self.y += self.dy
    
    def checkBounds(self):
        screen = self.screen
        if self.x > screen.get_width():
            #print "Right Shell Reset"
            self.reset()
        if self.x < 0:
            #print "Left Shell Reset"
            self.reset()
        if self.y > screen.get_height():
            #print "Bottom Shell Reset"
            self.reset()
        if self.y < 0:
            #print "Top Shell Reset"
            self.reset()
    
    def reset(self):
        """ move off stage and stop"""
        if self.pressed:
            print "Shell Reset at ", self.x, " ", self.y
        self.x = -100
        self.y = -100
        self.speed = 0

class Road(pygame.sprite.Sprite):
    
    def __init__(self, roadx, roady):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/road.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = roadx
        self.rect.centery = roady
        
    
def Map1():
    roadGroup = [Road(20, 100), Road(60, 100), Road(100, 100),
                 Road(140, 100), Road(140, 140), Road(140, 180),
                 Road(180, 180), Road(220, 180), Road(220, 220),
                 Road(220, 260), Road(220, 300), Road(220, 340),
                 Road(220, 380), Road(260, 380), Road(300, 380),
                 Road(300, 340), Road(300, 300), Road(300, 260),
                 Road(300, 220), Road(300, 180), Road(300, 140),
                 Road(340, 140), Road(380, 140), Road(420, 140),
                 Road(460, 140), Road(500, 140), Road(540, 140),
                 Road(580, 140), Road(620, 140)]
    return roadGroup

  
def main():

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tower Defense: TD_Tower_Grid - Making the grid.")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    roadGroup = Map1()
    posTower = PosTower()
    shellNumber = 0
    towerGroup = []
    shellGroup = []
    
    #for index in range(5):
    #    shellGroup.append(Shell(screen))
        
    mouseSprites = pygame.sprite.Group(posTower)
    mapSprite = pygame.sprite.Group(roadGroup)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(True)
        #towerSprites = pygame.sprite.Group(towerGroup)
        
        hitRoad = pygame.sprite.spritecollide(posTower, roadGroup, False)
        hitTower = pygame.sprite.spritecollide(posTower, towerGroup, False)
        if hitRoad or hitTower:
            posTower.image = pygame.image.load("images/no_tower.gif")
        else:
            posTower.image = pygame.image.load("images/yes_tower.gif")
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not hitRoad and not hitTower:
                    towerx, towery = posTower.update()
                    print(towerx, towery)
                    #towerGroup.append(Tower((Shell(screen)), towerx, towery))
                    shellGroup.append(Shell(screen))
                    towerGroup.append(Tower(shellGroup[shellNumber], towerx, towery))
                    shellNumber += 1
        towerSprites = pygame.sprite.Group(shellGroup, towerGroup)
        
        towerSprites.clear(screen, background)
        mapSprite.clear(screen, background)        
        mouseSprites.clear(screen, background)
        
        mapSprite.draw(screen)
        towerSprites.update()
        mouseSprites.update()
        towerSprites.draw(screen)
        mouseSprites.draw(screen)
        
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
