""" Name: TD_Overworld v0.01
    Authors: Joel Murphy & Chris Bentley
    Date: June 24, 2013
    Purpose: Overworld
"""
    
import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)
    


def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tower Defense v0.1")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))

    pygame.mouse.set_visible(True)
    
if __name__ == "__main__":
    main()
            
