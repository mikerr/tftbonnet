# mandelbrot fractal

# move with cursors,
# Y/A to zoom in/out
# X invert colours
# B grayscale

import time, math
import pygame
import RPi.GPIO as GPIO         

buttons = {
           "A":5,
           "B":6,
           "UP":17,
           "DOWN":22,
           "LEFT":27,
           "RIGHT":23,
           "CENTER":4
}

# setup gpio
GPIO.setmode(GPIO.BCM)         
for btn in buttons:
    GPIO.setup(buttons[btn], GPIO.IN)

def pressed(btn) :
    return ( GPIO.input(buttons[btn]) != True) 

WIDTH = HEIGHT = 240

screen = pygame.display.set_mode()

def mandel(i,res) :
    max_iter = 255  // res
    y = (i - HEIGHT/2) * scale + cy;
    for j in range (0,WIDTH, res):
        x = (j - WIDTH/2) * scale + cx;
        
        xs = (x - 0.25)
        zx = math.sqrt(xs * xs + y * y)
        if (x < zx - 2 * zx * zx + 0.25) : continue
        if ((x + 1)*(x + 1) + y * y < 1/16) : continue

        zx = zy = zx2 = zy2 = 0
        iter = 0
        for n in range (max_iter -1):
            iter = n
            zy = 2 * zx * zy + y
            zx = zx2 - zy2 + x
            zx2 = zx * zx
            zy2 = zy * zy
            if (zx2 + zy2 > 4) : break
            
        if (iter < max_iter):
                c = iter * res
                colorpixel(j,i,c)

def colorpixel(x,y,c):
    c = clr [c]
    if invertcolors : c = 255 -c
    
    grayscale = 1
    if not grayscale :
        if c == 0 or c == 255: pen = (0,0,0)
        else: pen = (hsv(c / 256,1,1))
    else : 
        r = g = b = c 
        pen = (r,g,b)
    screen.set_at((x,y),pen)
    
scale = 1./96
cx = -.6
cy = 0
invertcolors = 0
grayscale  = 0

clr= [int(255*((i/255)**12)) for i in range(255,-1,-1)]

while True:
    res = 4
    i = 0

    while True :
        #if i == 0: t_start = time.ticks_ms()
               
        #scrub previous scanline
        pen = (0,0,0)
        pygame.draw.rect(screen,pen,(0,i,WIDTH,res))
        
        if (res > 0) : mandel(i,res)
        pygame.display.flip()
                   
        i += res
        if i > HEIGHT :
            i = 0  
            #t_end = time.ticks_ms()
            #print(f"resolution {res} in {t_end - t_start} ms")
            res = res // 2
            
        if pressed("CENTER") :
            invertcolors = not invertcolors
            break
        if pressed("CENTER") :
            grayscale = not grayscale
            break
        if pressed("B") :
            scale = scale * 0.95
            break
        if pressed("A") :
            scale = scale * 1.05
            break
        move = scale *2
        if pressed("LEFT") :
            cx -= move
            break
        if pressed("RIGHT") :
            cx += move
            break
        if pressed("UP") :
            cy -= move
            break
        if pressed("DOWN") :
            cy += move
            break
