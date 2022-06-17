import pygame
import numpy
import random
import math
import objects as objs
import solver
import textBox


width = 1920
height = 1000
FPS = 160
substeps = 8


# Define Colors 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
ballColour = pygame.Color("#ffaf87")
ballOutlineColour = pygame.Color("#ed6a5e")
attractorColour = pygame.Color("#c1d37f")
backgroundColour = pygame.Color("#626c66")
OOBColour = pygame.Color("#434a42")

ballRadius = 50

pygame.init()
gameSolver = solver.solver([0,1000],width, height)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Verlet Physics")
clock = pygame.time.Clock()     

myfont = pygame.font.SysFont("monospace", 30)

frameTimes = []
objects = []
lastTick = 0

## Game loop
running = True
while running:

    #1 Process input/events
    dt = (clock.tick(FPS) / 1000)    # get delta time
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if gameSolver.getDist(pos,(width/2,height/2)) < (0.4*height):
                canSpawn = True
                currentTick = pygame.time.get_ticks()

                if currentTick - lastTick < 50:
                    canSpawn = False

                if canSpawn:    
                    objects.append(objs.ball(pos,ballRadius,ballColour,ballOutlineColour))
                    lastTick = currentTick



        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            objects.append(objs.attractor(pygame.mouse.get_pos(),10,attractorColour,200))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if ballRadius <= 145:
                ballRadius +=5

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if ballRadius > 5:
                ballRadius -=5
        


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                objects = []
            elif event.key == pygame.K_g:
                gameSolver.updateG()
            elif event.key == pygame.K_BACKSPACE and objects:
                objects.pop()
            elif event.key == pygame.K_EQUALS:
                substeps += 1
            elif event.key == pygame.K_MINUS:
                if substeps >= 2:
                    substeps -= 1

       
    screen.fill(OOBColour)
    pygame.draw.circle(screen,backgroundColour,gameSolver.getCenter(),gameSolver.getRadius())

    gameSolver.solve(objects,dt,substeps)

    for obj in objects:
        pygame.draw.circle(screen, obj.outlineColour, obj.pos, obj.radius)
        pygame.draw.circle(screen, obj.colour, obj.pos, obj.radius-math.ceil(0.1*obj.radius))
        
    
    #calculate FPS
    ticks = pygame.time.get_ticks()
    if ticks % 100 ==0:
        frameTimes = []
    frameTimes.append(dt)
    currentFPS = math.floor(1/numpy.average(frameTimes))
    
    # render text
    FPSCounter = myfont.render(f"{currentFPS} FPS", 1, white)
    screen.blit(FPSCounter, (10, 10))

    objectCounter = myfont.render(f"{len(objects)} balls", 1, white)
    screen.blit(objectCounter, (10, 50))

    if gameSolver.getGravity() == [0,0]:
        gravityLabel = myfont.render(f"Gravity: OFF", 1, white)
    else:
        gravityLabel = myfont.render(f"Gravity: ON", 1, white)

    screen.blit(gravityLabel,(10,90))

    radiusLabel = myfont.render(f"Radius: {ballRadius}", 1, white)
    screen.blit(radiusLabel,(10,130))

    substepsLabel = myfont.render(f"{substeps} substeps", 1, white)
    screen.blit(substepsLabel,(10,170))
    
    textArea = pygame.Rect((10,120),(gameSolver.getCenter()[0]-(gameSolver.getRadius()+50),height-10))
    
    text1 = f"Verlet Integration based particle simulation.\nControls:\nLeft mouse to add a particle\nRight mouse to add a point of attraction\nG to toggle gravity\nC to clear all objects\nScroll to change the radius of new particles\nBackspace to delete most recent object\n+ and - to increase and decrease substeps (lower substeps means more FPS, but the physics is more buggy)\nPerformance is based on number of balls, not ball size"

    textSurface = textBox.multiLineSurface(text1,myfont,textArea,white,OOBColour)
    screen.blit(textSurface,(10,210))

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
