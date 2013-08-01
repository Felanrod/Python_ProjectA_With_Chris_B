""" followMouse.py 
    a version of the turret game that
    uses the arctangent function 
    and pythagoras to get
    angle and distance from dx and dy
"""

import pygame, math 
pygame.init()

class Label(pygame.sprite.Sprite):
    """ Label Class (simplest version) 
        Properties:
            font: any pygame font object
            text: text to display
            center: desired position of label center (x, y)
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = ""
        self.center = (320, 240)
                
    def update(self):
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center


class Turret(pygame.sprite.Sprite):
    def __init__(self, shell, enemy, enemy2):
        self.shell = shell
        self.enemy = enemy
        self.enemy2 = enemy2
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("images/turret.gif")
        self.imageMaster = self.imageMaster.convert()
        self.imageMaster = pygame.transform.scale2x(self.imageMaster)
        self.rect = self.imageMaster.get_rect()
        self.rect.center = (320, 240)
        self.dir = 0
        self.distance1 = 0
        self.distance2 = 0
        self.charge = 20

    def update(self):
        self.findEnemy()
        self.shoot()
        self.rotate()

    def shoot(self):
        if(self.shell.notFired):
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.dir
            self.shell.notFired = False
    
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

    def checkEnemy(self):
        dx = self.rect.centerx - self.enemy.rect.centerx
        dy = self.rect.centery - self.enemy.rect.centery
        self.distance1 = math.sqrt((dx * dx) + (dy * dy))

        olddx = dx
        olddy = dy
        
        dx = self.rect.centerx - self.enemy2.rect.centerx
        dy = self.rect.centery - self.enemy2.rect.centery
        self.distance2 = math.sqrt((dx * dx) + (dy * dy))

        if self.distance1 < self.distance2:
            dx = olddx
            dy = olddy
            self.distance = self.distance1
        else:
            self.distance = self.distance2
        

        if self.enemy.dir == 'Right':
            dx -= (10*self.enemy.moveSpeed + self.distance/20)
        elif self.enemy.dir == 'Left':
            dx += (10*self.enemy.moveSpeed + self.distance/20)
        elif self.enemy.dir == 'Up':
            dy += (10*self.enemy.moveSpeed + self.distance/20)
        elif self.enemy.dir == 'Down':
            dy -= (10*self.enemy.moveSpeed + self.distance/20)

        return dx, dy

    def findEnemy(self):
##        dx = self.rect.centerx - self.enemy.rect.centerx
##        dy = self.rect.centery - self.enemy.rect.centery
##        self.distance = math.sqrt((dx * dx) + (dy * dy))

        dx, dy = self.checkEnemy()            
        dy *= -1

        radians = math.atan2(dy, dx)
        self.dir = radians * 180 / math.pi
        self.dir += 180
        
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
        #self.image = pygame.transform.scale(self.image, (5, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        
        self.speed = 0
        self.dir =0
        self.reset()
        
        
    def update(self):
        self.calcVector()
        self.calcPos()
        self.checkBounds()
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
        global misses
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
        self.x = -100
        self.y = -100
        self.speed = 0
        self.notFired = True

class LblDist(Label):
    def __init__(self, turret):
        Label.__init__(self)
        self.turret = turret
        self.center = (150, 20)
    
    def update(self):
        Label.update(self)
        self.text = "angle: %d, dist1: %d px, dist2: %d px" % \
        (self.turret.dir, self.turret.distance1, self.turret.distance2)

class EnemyTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
## Simple left to right, down to up and repeat.
        if self.health != 0:
            if self.rect.centerx >= 50:
                if self.rect.centerx <= 550 and self.dir == 'Right':
                    self.rect.centerx += self.moveSpeed
                else:
                    if self.rect.centery >= 100 and self.dir != 'Up' and self.dir !='Left':
                        if self.rect.centery <= 450:
                            self.rect.centery += self.moveSpeed
                            self.dir = 'Down'
                        else:            
                            self.rect.centery = 450
                            self.dir = 'Up'
                    elif self.rect.centery > 100 and self.dir == 'Up':
                        self.rect.centery -= self.moveSpeed
                    else:
                        self.rect.centery = 100
                        self.rect.centerx -= self.moveSpeed
                        self.dir = 'Left'
            else:
                self.rect.centerx = 50
                self.dir = 'Right'
        else:
            self.reset()

    def reset(self):
        self.rect.centerx = 50
        self.rect.centery = 100
        self.moveSpeed = 5
        self.health = 3
        self.dir = 'Right'


def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption ("Rotating Turret")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0x00, 0xCC, 0x00))
    screen.blit(background, (0, 0))

    shell = Shell(screen)
    shell2 = Shell(screen)
    enemy = EnemyTest()
    enemy2 = EnemyTest()
    turret = Turret(shell, enemy, enemy2)

    enemy2.rect.centerx = 300

    lblDist = LblDist(turret)
    allSprites = pygame.sprite.Group(shell, turret, enemy, enemy2, lblDist)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        if shell.rect.colliderect(enemy.rect):
            print "Hit!"
            enemy.health -= 1
            shell.reset()

        if shell.rect.colliderect(enemy2.rect):
            print "Hit!"
            enemy2.health -= 1
            shell.reset()
        
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
