import pygame
import sys

pygame.init()
display = pygame.display.set_mode((500,300))
while True:
    if pygame.event.peek():
        event = pygame.event.poll()
        print(event)
        if event.type == pygame.QUIT:
                print("You quit")
                pygame.quit()
                sys.exit()
