import pygame, random
from pygame import mixer
pygame.init()

background = pygame.image.load("images/overworld_test.png")
bRect = background.get_rect()
size = (width, height) = background.get_size()
screen = pygame.display.set_mode(size)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
    def update(self):
        if self.rect.top < 200:
            self.rect.centerx += 0
            self.rect.centery += 1
        if self.rect.top >= 100 and self.rect.left > 100:
            self.rect.centerx -= 1
        if self.rect.top >= 100 and self.rect.left <= 100:
            self.rect.centery += 1
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = 450
        
def main():
    mixer.init(44100)
    music = mixer.Sound("sounds/test.wav")
    music.play(loops=-1)
    pygame.display.set_caption("Simple Tower Enemy")

    screen.blit(background, bRect)
    enemy = Enemy()
    
    allSprites = pygame.sprite.Group(enemy)
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
