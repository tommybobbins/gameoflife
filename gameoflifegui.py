#!/usr/bin/python
"""

    CONWAY'S GAME OF LIFE

    this python version was written by
    JP ARMSTRONG http://www.jparmstrong.com/

    I developed this game just to learn python.

    MIT-LICENSE

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#################################################
"""


import pygame, random, time, random, os
from pygame.locals import *
from boxes import Box

MAX_X = 32
MAX_Y = 24
SIZE = 10
DEBUG = False

DEAD_CELL = '.'
LIVE_CELL = 'o'

rand_col = False
keep_background = False

# MAKING THE BOXES
boxes = [''] * MAX_X
    
for i in range(MAX_X):
    boxes[i] = [''] * MAX_Y

from evdev import InputDevice, list_devices
devices = map(InputDevice, list_devices())
eventX=""
for dev in devices:
    if dev.name == "ADS7846 Touchscreen":
        eventX = dev.fn
#print eventX

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ["SDL_MOUSEDEV"] = eventX


pygame.init()
pygame.display.set_caption('Conway\'s Game of Life by jparmstrong.com')
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])


# MAKING THE BOARD
board = [DEAD_CELL] * MAX_X
    
for i in range(MAX_X):
    board[i] = [DEAD_CELL] * MAX_Y



# ALLOWING THE BOARD TO WRAP AROUND, "INFINITE PLAYING FIELD"
def borderless(n, t):

    if n < 0:
        n = t + n;
    elif n >= t:
        n = abs(n) % t

    return n

# THE RULES TO LIFE
def rulesOfLife(b):

    total_pop = 0;

    pop_list = ['0'] * MAX_X
    
    for i in range(MAX_X):
        pop_list[i] = ['0'] * MAX_Y

   # CHECKING TO SEE WHAT IS POPULATED AROUND EACH CELL
    for y in range(MAX_Y):
        for x in range(MAX_X):

            pop = 0
            buf = []

            # ROW A
            if b[borderless(x-1, MAX_X)][borderless(y-1, MAX_Y)] == LIVE_CELL:
                buf.append("a1 ")
                pop += 1
                
            if b[borderless(x, MAX_X)][borderless(y-1, MAX_Y)] == LIVE_CELL:
                buf.append("a2 ")
                pop += 1
                
            if b[borderless(x+1, MAX_X)][borderless(y-1, MAX_Y)] == LIVE_CELL:
                buf.append("a3 ")
                pop += 1

            # ROW B
            if b[borderless(x-1, MAX_X)][borderless(y, MAX_Y)] == LIVE_CELL:
                buf.append("b1 ")
                pop += 1
            if b[borderless(x+1, MAX_X)][borderless(y, MAX_Y)] == LIVE_CELL:
                buf.append("b3 ")
                pop += 1

            # ROW C
            if b[borderless(x-1, MAX_X)][borderless(y+1, MAX_Y)] == LIVE_CELL:
                buf.append("c1 ")
                pop += 1
                
            if b[borderless(x, MAX_X)][borderless(y+1, MAX_Y)] == LIVE_CELL:
                buf.append("c2 ")
                pop += 1
                
            if b[borderless(x+1, MAX_X)][borderless(y+1, MAX_Y)] == LIVE_CELL:
                buf.append("c3 ")
                pop += 1

            if DEBUG and pop > 0:
                print x,y,":",''.join(buf),pop

            total_pop += pop

            pop_list[x][y] = pop

    
    # NOW THAT WE KNOW WHATS AROUND EACH CELL, WE IMPLEMENT THE RULES OF LIFE
    for y in range(MAX_Y):
        for x in range(MAX_X):

            if b[x][y] == LIVE_CELL and (pop_list[x][y] < 2 or pop_list[x][y] > 3):
                b[x][y] = DEAD_CELL
                
            elif b[x][y] == DEAD_CELL and pop_list[x][y] == 3:
                b[x][y] = LIVE_CELL


def updateDisplay():

    
    for dy in range(MAX_Y):
        for dx in range(MAX_X):
            if board[dx][dy] == LIVE_CELL:
                if rand_col:
                    boxes[dx][dy] = Box([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], [dx * SIZE, dy * SIZE], SIZE)
                else:
                    boxes[dx][dy] = Box([255, 255, 255], [dx * SIZE, dy * SIZE], SIZE)
            elif keep_background == False:
                boxes[dx][dy] = Box([0, 0, 0], [dx * SIZE, dy * SIZE], SIZE)

            screen.blit(boxes[dx][dy].image, boxes[dx][dy].rect)
    
    pygame.display.update()



running = True
button_down = False
keys = pygame.key.get_pressed()


while running:
    for event in pygame.event.get():

        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()
            
        if event.type == KEYDOWN and event.key == K_RETURN:
            running = False
             
        if event.type == KEYDOWN and event.key == K_r:
            # SETTING UP RANDOM GLYDERS
            for i in range(random.randint(10, 20)):
                sx = random.randint(0, MAX_X)
                sy = random.randint(0, MAX_Y)

                if random.randint(0, 1) == 1:
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 0, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 1, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;
                else:
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 0, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 1, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 0, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 1, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;
                    board[borderless(sx + 2, MAX_X)][borderless(sy + 2, MAX_Y)] = LIVE_CELL;

            updateDisplay()
                        
        if event.type == MOUSEBUTTONDOWN:
            button_down = True
            button_type = event.button
            
        if event.type == MOUSEBUTTONUP:
            button_down = False
            
        if button_down:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            sp_x = mouse_x / SIZE;
            sp_y = mouse_y / SIZE;

            if button_type == 1:
                board[sp_x][sp_y] = LIVE_CELL;
            elif button_type == 3:
                board[sp_x][sp_y] = DEAD_CELL;
                
            updateDisplay()


running = True
rand_col = True

while running:
    for event in pygame.event.get():
             
        if event.type == KEYDOWN and event.key == K_b:
            if keep_background == False:
                keep_background = True
            else:
                keep_background = False

        if event.type == QUIT:
                running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                
    
    updateDisplay()
    rulesOfLife(board)
    pygame.time.delay(10)
        
