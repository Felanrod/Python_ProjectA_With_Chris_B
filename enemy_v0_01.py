import pygame, random
from pygame import mixer
pygame.init()

background = pygame.image.load("images/overworld_1.png")
bRect = background.get_rect()
size = (width, height) = background.get_size()
screen = pygame.display.set_mode(size)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, xPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.image = self.image.convert()
        transColor = self.image.get_at((1, 1))
        self.image.set_colorkey(transColor)
        self.rect = self.image.get_rect()
        self.rect.centerx = xPos
        self.rect.centery = 90
        
    def update(self):
        xRoad = 300
        yRoad = 290
        if self.rect.centerx < xRoad:
            self.rect.centerx += 1.5
            self.rect.centery += 0
        if self.rect.centerx >= xRoad and self.rect.centery < yRoad:
            self.rect.centery += 1.5
        if self.rect.centerx >= xRoad and self.rect.centery >= yRoad:
            self.rect.centerx += 1.5
        if self.rect.centerx > (screen.get_width() - 40):
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centery = 90
        self.rect.centerx = 0
        
def main():
    mixer.init(44100)
    music = mixer.Sound("sounds/test.wav")
    #music.play(loops=-1)
    pygame.display.set_caption("Simple Tower Enemy")

    screen.blit(background, bRect)
    enemies = []

    for index in range(1, 10):
        enemy = Enemy((index*(-100)))
        enemies.append(enemy)
    
    allSprites = pygame.sprite.Group(enemies)
    clock = pygame.time.Clock()

    keepGoing = True
    while keepGoing:
        clock.tick(100)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
