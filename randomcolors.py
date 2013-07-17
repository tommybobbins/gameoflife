import pygame, random
from pygame.locals import *
from boxes import Box

MAX_X = 20
MAX_Y = 20
SIZE = 15

# MAKING THE BOXES
boxes = [''] * MAX_X
    
for i in range(MAX_X):
    boxes[i] = [''] * MAX_Y

    

pygame.init()
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])


while pygame.event.poll().type != KEYDOWN :
    for y in range(MAX_Y):
        for x in range(MAX_X):
            boxes[x][y] = Box([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], [x * SIZE, y * SIZE], SIZE)
            screen.blit(boxes[x][y].image, boxes[x][y].rect)
            

    pygame.display.update()
    pygame.time.delay(10)
