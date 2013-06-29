""" Name: TD_Tower_Grid v0.01
    Authors: Joel Murphy & Chris Bentley
    Date: June 28, 2013
    Purpose: To try and place the towers into a grid.
"""
    
import pygame, random, math
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Tower(pygame.sprite.Sprite):
    towerx = 20
    towery = 20
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/yes_tower.gif")
        self.rect = self.image.get_rect()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousex % 40 == 20:
            self.towerx = mousex
        if mousey % 40 == 20:
            self.towery = mousey
            
        self.rect.center = (self.towerx, self.towery)
    
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tower Defense: TD_Tower_Grid - Making the grid.")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    tower = Tower()
    
    allSprites = pygame.sprite.Group(tower)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        mousex, mousey = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(math.fmod(mousex, 20))
                print(mousex % 20)
                
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
