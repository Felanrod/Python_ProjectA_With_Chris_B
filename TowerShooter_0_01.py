import pygame, random, math, operator
pygame.init()

screen = pygame.display.set_mode((640, 480))

class PosTower(pygame.sprite.Sprite):
    towerx = 20
    towery = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.rect = self.image.get_rect()
        self.distance = []
    
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
    
    def __init__(self, shell, towerx, towery, enemies):
        self.shell = shell
        self.enemies = enemies
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = towerx
        self.rect.centery = towery
        self.charge = 5
        self.distance = []
        
    
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
        self.checkKeys()
    
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
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.dir
            self.shell.notFired = False

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
        #print "Initialized"
        
    def update(self):
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
            self.reset()
        if self.x < 0:
            self.reset()
        if self.y > screen.get_height():
            self.reset()
        if self.y < 0:
            self.reset()
    
    def reset(self):
        """ move off stage and stop"""
        if self.pressed:
            print "Shell Reset at ", self.x, " ", self.y
        self.x = -100
        self.y = -100
        self.speed = 0
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        self.path = []
        self.path = path
        self.image = pygame.image.load("images/enemy.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.alive = True
        self.reset()

    def update(self):
        if self.health > 0 and self.alive:
            self.rect.centerx += self.moveSpeed
        if self.rect.centerx > screen.get_width():
            self.reset()
            
    def reset(self):
        self.rect.centerx = 50
        self.rect.centery = random.randrange(20, 460, 30)
        self.moveSpeed = 2
        self.health = 1

class Road(pygame.sprite.Sprite):
    
    def __init__(self, road):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/road.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = road

class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        #Sets up necessary variables for scrolling road
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/overworld.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (640, 480)) #Stretched image, numbers tell me how long should I do the scrolling
        self.rect = self.image.get_rect()
    
def Map1():
    path = [(-20, 100),
            (20, 20), (60, 20), (100, 20),
            (20, 60), (60, 60), (100, 60),
            (20, 100), (60, 100), (100, 100),
            (20, 140), (60, 140), (100, 140),
            (20, 180), (60, 180), (100, 180),
            (20, 220), (60, 220), (100, 220),
            (20, 260), (60, 260), (100, 260),
            (20, 300), (60, 300), (100, 300),
            (20, 300), (60, 300), (100, 300),
            (20, 300), (60, 300), (100, 300),
            (20, 340), (60, 340), (100, 340),
            (20, 380), (60, 380), (100, 380),
            (20, 420), (60, 420), (100, 420),
            (20, 460), (60, 460), (100, 460),
            (20, 500), (60, 500), (100, 500)]
    return path

  
def main():

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tower Shooter: What remains of Failed Tower Defense")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    pathGroup = Map1()
    roadGroup = []
    terrain = Terrain()
    enemyDelay = 30
    enemyFrames = 0
    for path in range(len(pathGroup)):
        roadGroup.append(Road(pathGroup[path]))
    posTower = PosTower()
    shellNumber = 0
    towerGroup = []
    shellGroup = []
    enemyGroup = []
    
    mouseSprites = pygame.sprite.Group(posTower)
    mapSprite = pygame.sprite.Group(terrain, roadGroup)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    while keepGoing:
        clock.tick(30)

        pygame.mouse.set_visible(True)
        if len(enemyGroup) < 10:
##            print "Enemy Group Length", len(enemyGroup)
            enemyFrames += 1
            if enemyFrames >= enemyDelay:
                enemyFrames = 0
                pathGroup = Map1()
##                print "Enemy Added"
##                print "Length Path List: ", len(pathGroup)
                enemyGroup.append(Enemy(pathGroup))
                
        
        hitRoad = pygame.sprite.spritecollide(posTower, roadGroup, False)
        hitTower = pygame.sprite.spritecollide(posTower, towerGroup, False)
 
        if hitRoad or hitTower:
            posTower.image = pygame.image.load("images/no_tower.gif")
        else:
            posTower.image = pygame.image.load("images/yes_tower.gif")

        enemySprites = pygame.sprite.Group(enemyGroup)
           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not hitRoad and not hitTower:
                    towerx, towery = posTower.update()
##                    print(towerx, towery)
                    
                    shellGroup.append(Shell(screen))
                    towerGroup.append(Tower(shellGroup[shellNumber], towerx, towery, enemyGroup))
                    shellNumber += 1
        
        towerSprites = pygame.sprite.Group(shellGroup, towerGroup)
        

        hitEnemy = []
        for i in range(len(shellGroup)):
            hitEnemy.append(pygame.sprite.spritecollide(shellGroup[i], enemySprites, False))
        
            for enemy in hitEnemy[i]:
                print "HIT!"
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.reset()
                shellGroup[i].reset()
        
        towerSprites.clear(screen, background)

        enemySprites.clear(screen, background)
        mapSprite.clear(screen, background)        
        mouseSprites.clear(screen, background)
        
        
        towerSprites.update()
        enemySprites.update()
        mouseSprites.update()
        mapSprite.draw(screen)
        towerSprites.draw(screen)
        enemySprites.draw(screen)
        mouseSprites.draw(screen)
        
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
