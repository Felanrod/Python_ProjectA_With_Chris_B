""" Name: TowerShooter v1.04
    Authors: Chris Bentley, Joel Murphy
    Date: August 15, 2013
    Purpose: Birds eye view tank shooter defend buildings from advancing enemies.
"""


import pygame, random, math, operator, mixer
pygame.init()

screen = pygame.display.set_mode((640, 480))

#After tank placement the PosTower changes to Cross Hairs that allow you to aim
#the tank's barrel at enemies
class PosCrossHairs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Cross_Hairs.gif")
        self.rect = self.image.get_rect()
        #self.distance = []
    
    #follows the mouse
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, mousey)

#Tank class
class Tank(pygame.sprite.Sprite):
    
    def __init__(self, screen, shell, towerx, towery):
        self.shell = shell
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("images/base.png")
        self.imageMaster = self.imageMaster.convert()
        self.transColor = self.imageMaster.get_at((1, 1))
        self.imageMaster.set_colorkey(self.transColor)
        self.rect = self.imageMaster.get_rect()
        self.tankPlaced = False

        pygame.mixer.init()
        self.pew = pygame.mixer.Sound("sounds/pew.wav")
        self.death = pygame.mixer.Sound("sounds/death.wav")
        self.explosion = pygame.mixer.Sound("sounds/explosion.wav")
        self.pickup = pygame.mixer.Sound("sounds/pickup.wav")

        self.pew.set_volume(0.5)
        self.death.set_volume(0.5)
        
        self.rect.centerx = towerx
        self.rect.centery = towery
        
        #Self explanatory variables of the tank
        self.charge = 5
        self.speed = 2
        self.vdir = 0

        self.health = 100
        self.healthbar = HealthBar(self.health)

        self.centerx = 0
        self.centery = 0
        self.delay = 15
        self.pause = 0
        self.turnRate = 2
        self.destroyed = False
        self.normalSpeed = True
        
    #record the the mouse position and calculations
    def followMouse(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = self.rect.centerx - mouseX
        dy = self.rect.centery - mouseY
        dy *= -1
        
        radians = math.atan2(dy, dx)
        self.dir = radians * 180 / math.pi
        self.dir += 180
    
    def update(self):
        if not self.tankPlaced:
            self.tankMouse()
        self.pause += 1
        self.followMouse()
        self.checkKeys()
        self.checkBorders()
        self.rotate()
        self.healthbar.level = self.health
        self.healthbar.rect.center = self.centerx,self.centery-45
    
    def tankMouse(self):
        self.centerx,self.centery = pygame.mouse.get_pos()
        self.rect.center = pygame.mouse.get_pos()
    
    #sets the speed and direction of the shell associated with the tank
    def shoot(self):
        if self.shell.rect.centerx == -100:
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.dir
            self.shell.notFired = False

    #Ensure the tank doesn't drive off the map
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

    #Check the keys for movement and firing presses
    def checkKeys(self):
        moveX, moveY = 0,0
        keys = pygame.key.get_pressed()
        #Only do the button presses if the tank isn't destroyed
        if not self.destroyed:
            if keys[pygame.K_SPACE]:
                #Make sure the nth shell is off screen before firing it again
                for index in range(10):
                    if self.shell[index].x == -100:
                        if self.pause >= self.delay:
                            self.pew.play()
                            self.pause = 0
                            self.shell[index].x = self.rect.centerx
                            self.shell[index].y = self.rect.centery
                            self.shell[index].speed = self.charge
                            self.shell[index].dir = self.dir
                            break
            #Move tank forward
            if keys[pygame.K_w]:
                moveY -= math.cos(math.radians(self.vdir)) * (2 * self.speed)
                moveX -= math.sin(math.radians(self.vdir)) * (2 * self.speed)
                self.rect.centery += moveY
                self.rect.centerx += moveX
            #Move tank backward
            if keys[pygame.K_s]:
                moveY -= math.cos(math.radians(self.vdir)) * (2 * self.speed)
                moveX -= math.sin(math.radians(self.vdir)) * (2 * self.speed)
                self.rect.centery -= moveY
                self.rect.centerx -= moveX
            #Rotate tank left
            if keys[pygame.K_a]:
                self.vdir += self.turnRate
                if self.vdir > 360:
                    self.vdir = self.turnRate
            #Rotate tank right
            if keys[pygame.K_d]:
                self.vdir -= self.turnRate
                if self.vdir < 0:
                    self.vdir = 360 - self.turnRate

    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.vdir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
    #returns tank position
    def getPosition(self):
        return self.rect.center

#The tank's barrel
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
    
    #follows the mouse
    def update(self):
        self.rect.center = self.tower.rect.center
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
    
    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
        
#The shell that is fired from the tank
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
        
        self.pause = 0
        self.delay = 5
        self.frames = 0
        
        self.reset()
    
    #Calculates angle, movement, and position 
    def update(self):
        self.calcVector()
        self.calcPos()
        self.checkBounds()
        self.rect.center = (self.x, self.y)
    
    #Calculates angle and speed of firing
    def calcVector(self):
        radians = self.dir * math.pi / 180
        self.dx = self.speed * math.cos(radians)
        self.dy = self.speed * math.sin(radians)
        self.dy *= -1
    
    def calcPos(self):
        self.x += self.dx
        self.y += self.dy
    
    #if shell reaches the screen boundaries reset it
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
    
    #move shell off screen and stops
    def reset(self):
        self.x = -100
        self.y = -100
        self.speed = 0

#The Power Up that makes the shells move faster
class FasterPUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/faster_pUp.gif")
        self.rect = self.image.get_rect()
        self.pause = 0
        self.delay = 120
        self.reset()
    
    #Called to place it randomly on the field
    def onField(self):
        self.rect.center = (random.randrange(60, 280), random.randrange(20, 460))
    
    #resets it's position
    def reset(self):
        self.rect.center = (-500, -500)

#The Power Up that makes the rate of fire faster
class FasterFirePUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/faster_fire_pUp.gif")
        self.rect = self.image.get_rect()
        self.reset()
    
    #Called to place it randomly on the field
    def onField(self):
        self.rect.center = (random.randrange(60, 280), random.randrange(20, 460))
    
    #resets it's position
    def reset(self):
        self.rect.center = (-500, -500)

#The Power Up that completely heals your Tank
class HealPowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/heal_PUp.gif")
        self.rect = self.image.get_rect()
        self.reset()
    
    #Called to place it randomly on the field
    def onField(self):
        self.rect.center = (random.randrange(60, 280), random.randrange(20, 460))
    
    #resets it's position
    def reset(self):
        self.rect.center = (-500, -500)

#The enemies that walk toward your barracks        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadanimation()
        self.image = pygame.image.load("images/enemov0.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.alive = True
        self.maxHealth = 1
        self.frame = 0
        self.delay = 0
        self.yMov = 0
        self.reset()
    
    #Makes the enemies walk if they're alive
    def update(self):
        self.delay += 1
        if self.delay > 2:
            self.frame += 1
            self.delay = 0
            self.yMov = random.randrange(-2,4,2)
            
        if self.health > 0 and self.alive:
            self.rect.centerx += self.moveSpeed
            self.rect.centery += self.yMov
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > 480:
                self.rect.bottom = 480
            if self.frame >= len(self.walkImages):
                self.frame = 0
                self.afterHit = False
            else:
                self.image = self.walkImages[self.frame]
        if self.rect.centerx > screen.get_width():
            self.reset()
        
    #Loads the enemies animations
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
    
    #Resets their positions
    def reset(self):
        self.rect.centerx = -20
        self.rect.centery = random.randrange(20, 460, 30)
        self.moveSpeed = 2
        self.health = self.maxHealth

#The enemy vehicle that charges at you at the end of the level
class EnemyVehicle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemyV.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.alive = True
        self.maxHealth = 1
        self.frame = 0
        self.delay = 0
        self.reset()
    
    #Makes the enemy vehicle walk if it's alive
    def update(self):
        if self.health > 0 and self.alive:
            self.rect.centerx += self.moveSpeed
        if self.rect.centerx > screen.get_width():
            self.reset()
    
    #Resets their positions
    def reset(self):
        self.rect.centerx = -20
        self.rect.centery = random.randrange(20, 460, 30)
        self.moveSpeed = 5
        self.health = self.maxHealth

#Trees block shells
class Tree(pygame.sprite.Sprite):
    def __init__(self, road):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/tree.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = road

#The background
class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/terrain.jpg")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (640, 480)) 
        self.rect = self.image.get_rect()

#Supposed to display health above sprite but it didn't work
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

#The barracks you are defending
class Base(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/hq.gif")
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.rect = self.image.get_rect()
        self.rect.center = 600, y
        self.oldrect = self.rect.center
        self.alive = True
    
    #barracks death
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

#Text at the top to provide info of how well you do
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize display
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.wave = 1
        self.level = 1
        self.remaining = 20
        self.font = pygame.font.Font('images/Minecraftia.ttf', 20)
        self.time = 0
        
    def update(self):
        #Display Scoreboard
        self.text = "Health: %d  Level: %d  Wave: %d  Remaining: %d " % (self.health, self.level, self.wave, self.remaining)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 10

#Sprite of the logo
class Logo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/logo.png")
        self.transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(self.transColor)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()/2), int(self.image.get_height()/2)))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = 320, 50

class gameOverScreen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Write/Draw instructions plus Score

    def update(self):
        for line in self.overLabel:
            tempLabel = self.insFont.render(line, 0, (255, 255, 255))
            self.insLabels.append(tempLabel)

        for i in range(len(self.insLabels)):
            screen.blit(insLabels[i], (30, 30+30*i))

        
#Random placement of trees
def treeMap(treeNum):
    path = []
    for i in range(treeNum):
        path.append((random.randrange(i*20, 320), random.randrange(i*20, 460)))
    return path

#The splash screen
def startScreen():
    logo = pygame.image.load("images/tankLogo.png")
    titleScreen = pygame.image.load("images/TitleScreen.png")
    pygame.display.set_caption("Tank Shooter")
    count = 0
    stayOnTitle = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while stayOnTitle and count < 60:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stayOnTitle = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                stayOnTitle = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stayOnTitle = False
                    donePlaying = True

        count += 1
        screen.blit(titleScreen, (0, 0))
        screen.blit(logo, (60, 330))
        pygame.display.flip()
        pygame.time.delay(20)

    if count >= 60:
        donePlaying = False
    
    return donePlaying

#The intro screen with information
def intro(level, wave, toggle):
    if toggle:
        screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
    else:
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

    if wave != 0:
        scoreline = "You made it to Level %d Wave %d" % (level, wave)
    else:
        scoreline = ""

    #Write/Draw instructions plus Score
    insFont = pygame.font.Font('images/Fipps.otf', 16)
    insLabels = []
    instructions = (
    "",
    scoreline,
    "",
    "Instructions: You are a tank commander",
    "stop the rebels before the bomb HQ!",
    "",
    "Shoot, run over powerups,",
    "avoid incomming enemies.",
    "Shoot enemies with <SPACEBAR>.",
    "Aim with Mouse",
    "Rotate with A & D, Move with W & S",
    "Toggle Fullscreen with T",
    "",
    "Press any button to Start.",
    )
    for line in instructions:
        tempLabel = insFont.render(line, 0, (255, 255, 255))
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
                if event.key == pygame.K_t:
                    toggle = not toggle
                    if toggle:
                        screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((640, 480))
                    
                    

        allSprites.update()
        allSprites.draw(screen)

        #Draws the instructions
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (30, 30+30*i))

        pygame.display.flip()

    return donePlaying, toggle
                        
def game(fullScreen):
    if fullScreen:
        screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tank Shooter")
    pygame.mouse.set_visible(False) 
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    treeNum = 2
    pathGroup = treeMap(treeNum)
    roadGroup = []
    gamebases = []
    for i in range(4):
        gamebases.append(Base(i*120+60))
    scoreboard = Scoreboard()
    terrain = Terrain()
    newLevel = True
    enemyDelay = 30
    enemyFrames = 0
    pUpPause = 0
    pUpDelay = 120
    enemyNum = 5
    fasterDelay = 150
    fasterFrames = 0
    fasterOnField = False
    startEnemies = False
    
    #Set up the trees
    for path in range(len(pathGroup)):
        roadGroup.append(Tree(pathGroup[path]))
        
    posCrossHairs = PosCrossHairs()
    fasterPUp = FasterPUp()
    fasterFirePUp = FasterFirePUp()
    healPUp = HealPowerUp()
    shellGroup = []
    enemyGroup = []
    enemyVehicleGroup = []
    enemyVAdded = False
    explosion = Explosion()
    scoreSprite = pygame.sprite.Group(scoreboard)

    destroyHQ = False
    position = 0,0
    
    for shells in range(20):
        shellGroup.append(Shell(screen))
    
    tank = Tank(screen, shellGroup, -300, -300)
    
    powerUpSprites = pygame.sprite.Group(fasterPUp, fasterFirePUp, healPUp)
    mapSprite = pygame.sprite.OrderedUpdates(terrain)
    baseSprite = pygame.sprite.Group(gamebases)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    #While you haven't lost keep rolling at 30 frames per second
    while keepGoing:
        clock.tick(30)

        pygame.mouse.set_visible(False)
        
        #if tank is placed then switch cursor to cross hairs
        if tank.tankPlaced:
            mouseSprites = pygame.sprite.Group(posCrossHairs)
        else:
            mouseSprites = pygame.sprite.Group()
            
        
        #if the tank has been placed wait a second before sending enemies
        if startEnemies:
            if newLevel:
                if len(enemyGroup) < enemyNum:
                    enemyFrames += 1
                    if enemyFrames >= enemyDelay:
                        enemyFrames = 0
                        enemyGroup.append(Enemy())
                        for i in range(len(enemyGroup)):
                            #enemyGroup[i].reset()
                            enemyGroup[i].maxHealth = scoreboard.level
                else:
                    newLevel = False
                    
            
            #If there isn't a power up on the field start the timer to bring one out
            if not fasterOnField:
                fasterFrames += 1
                if fasterFrames >= fasterDelay:
                    whichPUp = random.randrange(1, 5)
                    if whichPUp == 1:
                        fasterPUp.onField()
                    elif whichPUp == 2:
                        healPUp.onField()
                    else:
                        fasterFirePUp.onField()
                    fasterOnField = True
                
        hitRoad = pygame.sprite.spritecollide(tank, roadGroup, False)

        enemySprites = pygame.sprite.Group(enemyGroup, enemyVehicleGroup)
        
        #Check for key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not tank.tankPlaced:
                    if not hitRoad:
                        if not startEnemies:
                            startEnemies = True
                        tank.tankPlaced = True
        
        turret = Turret(tank)
        explosionSprite = pygame.sprite.Group(explosion)
        towerSprites = pygame.sprite.OrderedUpdates(shellGroup, tank, turret)
        treeSprites = pygame.sprite.Group(roadGroup)
        
        #If a power up is on the field start the countdown to remove it
        if fasterOnField:
            pUpPause += 1
            if pUpPause >= pUpDelay:
                fasterOnField = False
                pUpPause = 0
                fasterFrames = 0
                fasterPUp.reset()
                fasterFirePUp.reset()
                healPUp.reset()
        
        #If you hit the Faster Power Up increases speed of shells
        if pygame.sprite.spritecollide(fasterPUp, towerSprites, False):
            tank.pickup.play()
            tank.charge += 1
            fasterPUp.reset()
            fasterFrames = 0
            fasterOnField = False
            pUpPause = 0
        
        #If you hit the Faster Fire Power Up increases rate of fire
        if pygame.sprite.spritecollide(fasterFirePUp, towerSprites, False):
            tank.pickup.play()
            if tank.delay > 1:
                tank.delay -= 1
            fasterFirePUp.reset()
            fasterFrames = 0
            fasterOnField = False
            pUpPause = 0

        #If you hit the Faster Fire Power Up increases rate of fire
        if pygame.sprite.spritecollide(healPUp, towerSprites, False):
            tank.pickup.play()
            healPUp.reset()
            fasterFrames = 0
            scoreboard.health = 100
            fasterOnField = False
            pUpPause = 0


        collideRoad = []
        #If the shell hits a tree have it disappear
        for i in range(len(shellGroup)):
            collideRoad.append(pygame.sprite.spritecollide(shellGroup[i], roadGroup, False))
            for road in collideRoad[i]:
                shellGroup[i].reset()
                        

        hitEnemy = []
        #If a shell hits an enemy have it deal a point of damage
        for i in range(len(shellGroup)):
            hitEnemy.append(pygame.sprite.spritecollide(shellGroup[i], enemySprites, False))

            for enemy in hitEnemy[i]:
                enemy.health -= 1
                if enemy.health <= 0:
                    tank.death.play()
                    scoreboard.remaining -= 1
                    enemy.reset()
                shellGroup[i].reset()
                
        #When the scoreboard remaining amount is equal to the level
        #and its wave 5 send in the vehicles
        if scoreboard.remaining == scoreboard.level and scoreboard.wave == 5 and not enemyVAdded:
            enemyVAdded = True
            enemyGroup = []
            enemyVehicleGroup = []
            for eV in range(scoreboard.level):
                enemyVehicleGroup.append(EnemyVehicle())
            enemySprites = pygame.sprite.Group(enemyGroup, enemyVehicleGroup)
        
        #When waves reach 0 start a new one with stronger enemies and an extra enemy
        elif scoreboard.remaining <= 0:
            scoreboard.wave += 1
            scoreboard.remaining = 20
            enemyGroup.append(Enemy())
            if scoreboard.wave == 5:
                scoreboard.remaining = 20 + scoreboard.level
            
            #Reset numbers when level advances
            #Add 2 trees to the map
            elif scoreboard.wave >= 6:
                scoreboard.level += 1
                scoreboard.wave = 1
                enemyVehicleGroup = []
                enemyGroup = []
                newLevel = True
                enemyVAdded = False
                treeNum += 2
                pathGroup = treeMap(treeNum)
                roadGroup = []
                for path in range(len(pathGroup)):
                    roadGroup.append(Tree(pathGroup[path]))
                enemySprites = pygame.sprite.Group(enemyGroup)

        hitBase = []
        #If the enemy hits one of the four bases it explodes
        for i in range(len(enemyGroup)):
            hitBase.append(pygame.sprite.spritecollide(enemyGroup[i], gamebases, False))

            for base in hitBase[i]:
                if base.alive:
                    destroyHQ = True
                    tank.explosion.play()
                    position = base.rect.center
                    base.explodedBase()
                    enemyGroup[i].reset()
                    base.alive = False
                    enemyNum += 1
                    enemyGroup.append(Enemy())
                    enemySprites = pygame.sprite.Group(enemyGroup)

            if gamebases[0].alive == False and gamebases[1].alive == False and gamebases[2].alive == False and gamebases[3].alive == False:
                keepGoing = False
        
        vehicleHitBase = []
        #If the enemy vehicle hits one of the four bases it explodes
        for i in range(len(enemyVehicleGroup)):
            vehicleHitBase.append(pygame.sprite.spritecollide(enemyVehicleGroup[i], gamebases, False))

            for base in vehicleHitBase[i]:
                if base.alive:
                    tank.explosion.play()
                    destroyHQ = True
                    position = base.rect.center
                    base.explodedBase()
                    enemyVehicleGroup[i].reset()
                    base.alive = False
                    enemyNum += 1
                    enemySprites = pygame.sprite.Group(enemyGroup, enemyVehicleGroup)

            if gamebases[0].alive == False and gamebases[1].alive == False and gamebases[2].alive == False and gamebases[3].alive == False:
                keepGoing = False
                
        #If the enemy hits the tank you lose 20 health
        enemyHitTank = pygame.sprite.spritecollide(tank, enemySprites, False)
        if enemyHitTank:
            for enemy in enemyHitTank:
                scoreboard.health -= 20
                enemy.reset()
                if scoreboard.health <= 0:
                    keepGoing = False
                break
        
        #Refreshing of the sprites
        towerSprites.clear(screen, background)
        baseSprite.clear(screen, background)
        enemySprites.clear(screen, background)
        mapSprite.clear(screen, background)
        powerUpSprites.clear(screen, background)
        mouseSprites.clear(screen, background)
        treeSprites.clear(screen, background)
        explosionSprite.clear(screen, background)
        
        treeSprites.update()
        towerSprites.update()
        enemySprites.update()
        baseSprite.update()
        mouseSprites.update()
        
        mapSprite.draw(screen)
        powerUpSprites.draw(screen)
        baseSprite.draw(screen)
        enemySprites.draw(screen)
        towerSprites.draw(screen)
        treeSprites.draw(screen)
        mouseSprites.draw(screen)
        

        #Draw/Update Scoreboard
        scoreSprite.update()
        scoreSprite.draw(screen)
        
        if destroyHQ:
            explosionSprite.update(position)
            explosionSprite.draw(screen)
            if explosion.frame == 23:
                destroyHQ = False

        if not keepGoing:
            insFont = pygame.font.Font('images/Fipps.otf', 28)
            insLabels = []
            overLabel = (
            "GAME OVER",
            "",
            "You reached: ",
            "Level %d" % scoreboard.level,
            "Wave %d" % scoreboard.wave
            )

            for line in overLabel:
                tempLabel = insFont.render(line, 0, (255, 255, 255))
                insLabels.append(tempLabel)

            for i in range(len(insLabels)):
                screen.blit(insLabels[i], (180, 130+50*i))
        
        pygame.display.flip()

        if not keepGoing:
            pygame.time.delay(3000)
    
    gameOver = True

    return scoreboard.level, scoreboard.wave, gameOver

def main():
    #Plays soundtrack for the game
    mixer.init(44100)
    music = mixer.Sound("sounds/test.wav")
    music.set_volume(0.1)
    music.play(loops=-1)
    level = 0
    wave = 0
    donePlaying = False
    gameOver = False
    fullScreen = False

    #The main game loop, keeps playing the game until the player quits it
    while not donePlaying:
        if not gameOver:
            donePlaying = startScreen()
        if not donePlaying:
            donePlaying, fullScreen = intro(level, wave, fullScreen)
            if not donePlaying:
                level, wave, gameOver = game(fullScreen)
                
if __name__ == "__main__":
    main()
