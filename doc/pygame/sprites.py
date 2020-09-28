import pygame
import time

pygame.init()
display = pygame.display.set_mode((1080,720))
settingsImage = pygame.image.load("settings.png").convert()
display.blit(settingsImage, (0,0))
pygame.display.flip()
time.sleep(2)
