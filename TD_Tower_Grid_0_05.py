""" Name: TD_Tower_Grid v0.05
    Authors: Joel Murphy & Chris Bentley
    Date: June 28, 2013
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
    
    def __init__(self, towerx, towery):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = towerx
        self.rect.centery = towery

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
    towerGroup = []
    allSprites = pygame.sprite.Group(posTower)
    mapSprite = pygame.sprite.Group(roadGroup)
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(True)
        towerSprites = pygame.sprite.Group(towerGroup)
        hitRoad = pygame.sprite.spritecollide(posTower, roadGroup, False)
        if hitRoad:
            posTower.image = pygame.image.load("images/no_tower.gif")
        else:
            posTower.image = pygame.image.load("images/yes_tower.gif")
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print hitRoad
                if not hitRoad:
                    towerx, towery = posTower.update()
                    print(towerx, towery)
                    towerGroup.append(Tower(towerx, towery))
        
        mapSprite.clear(screen, background)        
        allSprites.clear(screen, background)
        towerSprites.clear(screen, background)
        mapSprite.draw(screen)
        allSprites.update()
        allSprites.draw(screen)
        
        towerSprites.draw(screen)
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
