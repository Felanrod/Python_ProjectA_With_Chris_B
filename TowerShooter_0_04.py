import pygame, random, math, operator, mixer
pygame.init()

screen = pygame.display.set_mode((640, 480))

class PosTower(pygame.sprite.Sprite):
    towerx = 20
    towery = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.distance = []
    
    def update(self):
        self.image.set_alpha(200)
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

class PosCrossHairs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Cross_Hairs.gif")
        self.rect = self.image.get_rect()
        self.distance = []
    
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)
    
class Tower(pygame.sprite.Sprite):
    
    def __init__(self, screen, shell, towerx, towery, enemies):
        self.shell = shell
        self.screen = screen
        self.enemies = enemies
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("images/base.png")
        self.imageMaster = self.imageMaster.convert()
        self.transColor = self.imageMaster.get_at((1, 1))
        self.imageMaster.set_colorkey(self.transColor)
        self.rect = self.imageMaster.get_rect()
        
        self.rect.centerx = towerx
        self.rect.centery = towery
        
        self.charge = 5
        self.speed = 2
        self.nspeed = 2
        self.vdir = 0
        self.distance = []

        self.health = 100
        self.healthbar = HealthBar(self.health)

        self.centerx = 0
        self.centery = 0
        self.delay = 15
        self.pause = 0
        self.turnRate = 2
        self.destroyed = False
        self.normalSpeed = True
        
    
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
        #self.shell.pause += self.shell.frames
        #if self.shell.pause >= self.shell.delay:
        #    self.shell.pause = 0
        #    self.shell.frames = 0
        #    self.shell.pressed = False
        self.pause += 1
        self.followMouse()
        self.checkKeys()
        self.checkBorders()
        self.rotate()

        self.healthbar.level = self.health
        self.healthbar.rect.center = self.centerx,self.centery-45
    
    def shoot(self):
        if self.shell.rect.centerx == -100:
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.dir
            self.shell.notFired = False

    def checkBorders(self):
        screen = self.screen
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
        if self.rect.top < 0:
            self.rect.top = 0

        
    def checkKeys(self):
        moveX, moveY = 0,0
        keys = pygame.key.get_pressed()
        if not self.destroyed:
            if keys[pygame.K_SPACE]:
                for index in range(10):
                    if self.shell[index].x == -100:
                        if self.pause >= self.delay:
                            self.pause = 0
                            self.shell[index].x = self.rect.centerx
                            self.shell[index].y = self.rect.centery
                            self.shell[index].speed = self.charge
                            self.shell[index].dir = self.dir
                            break
            if keys[pygame.K_w]:
                moveY -= math.cos(math.radians(self.vdir)) * (2 * self.speed)
                moveX -= math.sin(math.radians(self.vdir)) * (2 * self.speed)

                self.rect.centery += moveY
                self.rect.centerx += moveX
            if keys[pygame.K_s]:
                moveY -= math.cos(math.radians(self.vdir)) * (2 * self.speed)
                moveX -= math.sin(math.radians(self.vdir)) * (2 * self.speed)
                self.rect.centery -= moveY
                self.rect.centerx -= moveX
            if keys[pygame.K_a]:
                self.vdir += self.turnRate
                if self.vdir > 360:
                    self.vdir = self.turnRate
            if keys[pygame.K_d]:
                self.vdir -= self.turnRate
                if self.vdir < 0:
                    self.vdir = 360 - self.turnRate

            #self.shell.x = self.rect.centerx
            #self.shell.y = self.rect.centery
            #self.shell.speed = self.charge
            #self.shell.dir = self.dir
            #self.shell.notFired = False

    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.vdir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def getPosition(self):
        return self.rect.center
    
    def destroyed(self, group):
        self.group = group
        self.group.pop()
        #self.kill()

class Turret (pygame.sprite.Sprite):
    def __init__ (self, tower):
        self.tower = tower
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("images/turret.png")
        self.imageMaster = self.imageMaster.convert()
        self.transColor = self.imageMaster.get_at((1, 1))
        self.imageMaster.set_colorkey(self.transColor)
        self.rect = self.imageMaster.get_rect()
        self.rect.center = -100,-100

    def update(self):
        if self.tower != []:
            self.rect.center = self.tower[0].rect.center
        self.followMouse()
        self.rotate()
    
    def followMouse(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = self.rect.centerx - mouseX
        dy = self.rect.centery - mouseY
        dy *= -1
        
        radians = math.atan2(dy, dx)
        self.dir = radians * 180 / math.pi
        self.dir += 90
        
        #calculate distance
        self.distance = math.sqrt((dx * dx) + (dy * dy))
    
    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
        

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
        
class FasterPUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/faster_pUp.gif")
        self.rect = self.image.get_rect()
        self.reset()
    
    def onField(self):
        self.rect.center = (random.randrange(60, 280), random.randrange(20, 460))
    
    def reset(self):
        self.rect.center = (-500, -500)

class FasterFirePUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/faster_fire_pUp.gif")
        self.rect = self.image.get_rect()
        self.reset()
    
    def onField(self):
        self.rect.center = (random.randrange(60, 280), random.randrange(20, 460))
    
    def reset(self):
        self.rect.center = (-500, -500)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        self.loadanimation()
        self.path = []
        self.path = path
        self.image = pygame.image.load("images/enemov0.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.alive = True
        self.frame = 0
        self.delay = 0
        self.reset()

    def update(self):
        self.delay += 1
        if self.delay > 2:
            self.frame += 1
            self.delay = 0
            
        
        if self.health > 0 and self.alive:
            self.rect.centerx += self.moveSpeed
            if self.frame >= len(self.walkImages):
                self.frame = 0
                self.afterHit = False
            else:
                self.image = self.walkImages[self.frame]
        if self.rect.centerx > screen.get_width():
            self.reset()
        

    def loadanimation(self):
        self.walkImages = []
        for i in range(5):
            imgName = "images/enemov{0}.png".format(i)
            tmpImage = pygame.image.load(imgName)
            tmpImage = pygame.transform.flip(tmpImage, 10, 0)
            tmpImage = tmpImage.convert()
            transColor = tmpImage.get_at((1, 1))
            tmpImage.set_colorkey(transColor)
            self.walkImages.append(tmpImage)
            
    def reset(self):
        self.rect.centerx = 0
        self.rect.centery = random.randrange(20, 460, 30)
        self.moveSpeed = 2
        self.health = 1

class Road(pygame.sprite.Sprite):
    
    def __init__(self, road):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/tree.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = road

class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        #Sets up necessary variables for scrolling road
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/terrain.jpg")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (640, 480)) 
        self.rect = self.image.get_rect()

class HealthBar(pygame.sprite.Sprite):
    def __init__(self,health):
        pygame.sprite.Sprite.__init__(self)
        self.level = health
        self.image = pygame.Surface((50, 10))
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image,(0,255,0),[0,0,self.level,10],0)
        self.rect = self.image.get_rect()
        
    
    def update(self):
        self.image.fill((0,0,0))
        if self.level > 25:
            color = (0,255,0)
        elif self.level > 12:
            color = (255,255,0)
        else:
            color = (255,0,0)
        pygame.draw.rect(self.image,color,[0,0,self.level,10],0)   

class Base(pygame.sprite.Sprite):
    def __init__(self, y):
        #Sets up necessary variables for scrolling road
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/hq.gif")
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.rect.center = 600, y
        self.oldrect = self.rect.center
        self.alive = True

    def explodedBase(self):
        self.image = pygame.image.load("images/destroyedhq.png")
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldrect

#In charge of explosion animation when a player loses or car hits something
class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        #Initializes the settings for the explosions
        pygame.sprite.Sprite.__init__(self)
        self.loadexplosion()
        self.image = pygame.image.load("images/animation/explosion (0).png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (-100,-100)
        self.frame = 0

    def update(self, position):
        self.rect.center = position
        self.rect.centery -= 40
        self.rect.centerx -= 60
        #Creates an explosion animation by shifting upwars through the frames
        self.frame += 1
        #If the frameset is over, reset the sequence for further use
        if self.frame >= len(self.walkImages):
            self.frame = 0
        else:
            self.image = self.walkImages[self.frame]

    def loadexplosion(self):
        #Loads the images of the explosion from folder
        self.walkImages = []
        for i in range(24):
            imgName = "images/animation/explosion ({0}).png".format(i)
            tmpImage = pygame.image.load(imgName)
            tmpImage = pygame.transform.scale(tmpImage, (150, 150))
            tmpImage = tmpImage.convert()
            transColor = tmpImage.get_at((10, 10))
            tmpImage.set_colorkey(transColor)
            self.walkImages.append(tmpImage)
    
def Map1():
    path = [(-20, 100),
            (20, 20), (100, 20),
            (60, 60), (100, 60),
            (20, 100), (100, 100),
            (20, 140), (100, 140),
            (20, 180), (60, 180),
            (20, 220), (100, 220),
            (100, 260),
            (60, 300), (100, 300),
            (20, 300), (100, 300),
            (20, 300),
            (20, 340),
            (20, 380), (100, 380),
            (20, 420), (60, 420),
            (60, 460), (100, 460),
            (20, 500), (100, 500)]
    return path

def Map2():
    path = []
    for i in range(3):
        for g in range(5):
            path.append((i*120+random.randrange(20, 120), g*80++random.randrange(20, 120)))
    return path
def Map3():
    path = []
    for i in range(10):
        path.append((random.randrange(i*20, 320), random.randrange(i*20, 460)))
    return path


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize display
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.wave = 1
        self.remaining = 20
        self.font = pygame.font.Font('images/Minecraftia.ttf', 20)
        self.time = 0
        self.distance = 0
        
    def update(self):
        #Display Scoreboard
        self.text = "Health: %d        Wave: %d         Remaining: %d " % (self.health, self.wave, self.remaining)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 10

class Logo(pygame.sprite.Sprite):
    def __init__(self):
        #Sets up necessary variables for scrolling road
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/logo.png")
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()/2), int(self.image.get_height()/2)))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = 320, 50


def intro(score):
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tank Shooter")
    pygame.mouse.set_visible(False) 
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    keepGoing = True

    logo = Logo()
    terrain = Terrain()
    gamebases = []

    if score != 0:
        scoreline = "You made it to Wave %d" % score
    else:
        scoreline = ""

    #Write/Draw instructions plus Score
    insFont = pygame.font.Font('images/Fipps.otf', 18)
    insLabels = []
    instructions = (
    "",
    "",
    scoreline,
    "",
    "Instructions: You are a tank commander",
    "stop the rebels before the bomb HQ!",
    "",sws
    "Shoot, run over powerups,",
    "avoid incomming enemies.",
    "Shoot enemies with <SPACEBAR>.",
    "Aim with Mouse",
    "Rotate with A & D, Move with W & S",
    "",
    "Press any button to Start.",
    )
    for line in instructions:
        tempLabel = insFont.render(line, 0, (0, 0, 0))
        insLabels.append(tempLabel)

    
    for i in range(4):
        gamebases.append(Base(i*120+60))
    allSprites = pygame.sprite.OrderedUpdates(terrain, gamebases, logo)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click to start game
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True

        allSprites.update()
        allSprites.draw(screen)

        #Draws the instructions
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (30, 30+30*i))

        pygame.display.flip()

    return donePlaying
                        
def game():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Rushed Tower Shooter")
    pygame.mouse.set_visible(False) 
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    pathGroup = Map3()
    roadGroup = []
    gamebases = []
    for i in range(4):
        gamebases.append(Base(i*120+60))
    scoreboard = Scoreboard()
    terrain = Terrain()
    towersToPlace = 1
    enemyDelay = 30
    enemyFrames = 0
    fasterDelay = 150
    fasterFrames = 0
    fasterOnField = False
    startEnemies = False
    for path in range(len(pathGroup)):
        roadGroup.append(Road(pathGroup[path]))
    posTower = PosTower()
    posCrossHairs = PosCrossHairs()
    fasterPUp = FasterPUp()
    fasterFirePUp = FasterFirePUp()
    shellNumber = 0
    towerGroup = []
    #tempTowerGroup = []
    shellGroup = []
    enemyGroup = []
    explosion = Explosion()
    scoreSprite = pygame.sprite.Group(scoreboard)

    destroyHQ = False
    position = 0,0
    
    for shells in range(10):
        shellGroup.append(Shell(screen))
    
    powerUpSprites = pygame.sprite.Group(fasterPUp, fasterFirePUp)
    mapSprite = pygame.sprite.OrderedUpdates(terrain, gamebases)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    while keepGoing:
        clock.tick(30)

        pygame.mouse.set_visible(True)
        if towersToPlace > 0:
            mouseSprites = pygame.sprite.Group(posTower)
        else:
            mouseSprites = pygame.sprite.Group(posCrossHairs)
       # tempTowerGroup = towerGroup
       # towerGroup = tempTowerGroup
        if startEnemies:
            if len(enemyGroup) < 10:
    ##            print "Enemy Group Length", len(enemyGroup)
                enemyFrames += 1
                if enemyFrames >= enemyDelay:
                    enemyFrames = 0
                    pathGroup = Map1()
    ##                print "Enemy Added"
    ##                print "Length Path List: ", len(pathGroup)
                    enemyGroup.append(Enemy(pathGroup))
            
            if not fasterOnField:
                fasterFrames += 1
                if fasterFrames >= fasterDelay:
                    whichPUp = random.randrange(1, 5)
                    if whichPUp == 1:
                        fasterPUp.onField()
                    elif whichPUp > 1:
                        fasterFirePUp.onField()
                    fasterOnField = True
                
        
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
                if towersToPlace > 0:
                    if not hitRoad and not hitTower:
                        if not startEnemies:
                            startEnemies = True
                        towersToPlace -= 1
                        towerx, towery = posTower.update()
##                    print(towerx, towery)
                    
                    #shellGroup.append(Shell(screen))
                        towerGroup.append(Tower(screen, shellGroup, towerx, towery, enemyGroup))
                        shellNumber += 1
                        #print "Tower Group Size: ", len(towerGroup)
                        #print towerGroup
        
        turret = Turret(towerGroup)
        explosionSprite = pygame.sprite.Group(explosion)
        towerSprites = pygame.sprite.OrderedUpdates(shellGroup, towerGroup, turret)
        treeSprites = pygame.sprite.Group(roadGroup)
        
        if pygame.sprite.spritecollide(fasterPUp, towerSprites, False):
            for tower in range(len(towerGroup)):
                towerGroup[tower].charge += 5
            fasterPUp.reset()
            fasterFrames = 0
            fasterOnField = False
        
        if pygame.sprite.spritecollide(fasterFirePUp, towerSprites, False):
            for tower in range(len(towerGroup)):
                if towerGroup[tower].delay > 1:
                    towerGroup[tower].delay -= 1
            fasterFirePUp.reset()
            fasterFrames = 0
            fasterOnField = False


        collideRoad = []
        for i in range(len(shellGroup)):
            collideRoad.append(pygame.sprite.spritecollide(shellGroup[i], roadGroup, False))
            for road in collideRoad[i]:
                shellGroup[i].reset()
                        

        hitEnemy = []
        for i in range(len(shellGroup)):
            hitEnemy.append(pygame.sprite.spritecollide(shellGroup[i], enemySprites, False))

            for enemy in hitEnemy[i]:
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.reset()
                shellGroup[i].reset()
                scoreboard.remaining -= 1

        if scoreboard.remaining <= 0:
            scoreboard.remaining = 20
            scoreboard.wave += 1
            for i in range(len(enemyGroup)):
                enemyGroup[i].reset()
            pathGroup = Map2()

        hitBase = []
        for i in range(len(enemyGroup)):
            hitBase.append(pygame.sprite.spritecollide(enemyGroup[i], gamebases, False))

            for base in hitBase[i]:
                if base.alive:
                    destroyHQ = True
                    position = base.rect.center
                    base.explodedBase()
                    enemyGroup[i].reset()
                    base.alive = False

            if gamebases[0].alive == False and gamebases[1].alive == False and gamebases[2].alive == False and gamebases[3].alive == False:
                keepGoing = False
                
        #enemyHitTower = pygame.sprite.spritecollide(enemyGroup, towerSprites, False)
        #if enemyHitTower:
        #    tower.destroyed(towerGroup)
        
        enemyHitTower = []
        if len(towerGroup) > 0:
            for i in range(len(towerGroup)):
                enemyHitTower.append(pygame.sprite.spritecollide(towerGroup[i-1], enemySprites, False))
                if enemyHitTower:
                    for enemy in enemyHitTower[i]:
                        scoreboard.health -= 20
                        enemy.reset()
                        if scoreboard.health <= 0:
                            towerGroup.pop(i-1)
                            keepGoing = False
                        break
            
                
                #enemyGroup[i].reset()
        #for i in range(len(enemyGroup)):
        #    enemyHitTower.append(pygame.sprite.spritecollide(enemyGroup[i], towerSprites, False))
            
        #    for tower in enemyHitTower[i]:
        #        print "Tower Destroyed"
        #        towerGroup.pop(tower)
        #        tower.destroyed(towerGroup)
        #        print "Tower Group Size: ", len(towerGroup)
                #enemyGroup[i].reset()
            
        #    if enemyHitTower:
        #        break
                
        
        towerSprites.clear(screen, background)
        enemySprites.clear(screen, background)
        mapSprite.clear(screen, background)
        powerUpSprites.clear(screen, background)
        mouseSprites.clear(screen, background)
        treeSprites.clear(screen, background)
        explosionSprite.clear(screen, background)
        
        treeSprites.update()
        towerSprites.update()
        enemySprites.update()
        mouseSprites.update()
        mapSprite.draw(screen)
        towerSprites.draw(screen)
        powerUpSprites.draw(screen)
        enemySprites.draw(screen)
        mouseSprites.draw(screen)
        treeSprites.draw(screen)

        #Draw/Update Scoreboard
        scoreSprite.update()
        scoreSprite.draw(screen)
        
        if destroyHQ:
            explosionSprite.update(position)
            explosionSprite.draw(screen)
            if explosion.frame == 23:
                destroyHQ = False
        
        pygame.display.flip()

    return scoreboard.wave

def main():
    #Plays soundtrack for the game
    mixer.init(44100)
    music = mixer.Sound("sounds/test.wav")
    music.set_volume(0.2)
    music.play(loops=-1)
    score = 0
    donePlaying = False

    #The main game loop, keeps playing the game until the player quites it
    while not donePlaying:
        donePlaying = intro(score)
        if not donePlaying:
            score = game()
if __name__ == "__main__":
    main()
