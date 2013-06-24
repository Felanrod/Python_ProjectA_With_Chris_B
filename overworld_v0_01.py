""" Name: TD_Overworld v0.01
    Authors: Joel Murphy & Chris Bentley
    Date: June 24, 2013
    Purpose: Overworld
"""
    
import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
    
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Blah")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            
