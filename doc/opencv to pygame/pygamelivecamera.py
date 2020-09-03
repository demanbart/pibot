import pygame
import cv2
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([640, 480])
#I've set screen size equal to the camera dimensions

try:
    while True:
        ret, frame = camera.read()
        
        screen.fill([0, 0, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        pygame.surfarray.blit_array(screen, frame)
        pygame.display.update()

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
