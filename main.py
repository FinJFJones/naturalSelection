## Modules ##
import pygame
## Files ##
import classes

pygame.init()

displayWidth, displayHeight = 500, 500

screen = pygame.display.set_mode([displayWidth, displayHeight], pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
FPS = 60
iteration = 0

showEnv, showPop = True, True
useOvercrowding = True

environment = classes.Environment(10, 50, (255, 105, 180))
worldPop = classes.Population(2, ((environment.gridSize//2)*environment.plotSize, (environment.gridSize//2)*environment.plotSize), 0.3, (255, 105, 180), 0.3) # Home in centre
#worldPop = classes.Population(100, (1, 1), 0.3, (200, 100, 180), 0.5) # Home at 1, 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                showEnv = not showEnv
            if event.key == pygame.K_2:
                showPop = not showPop
            if event.key == pygame.K_EQUALS:
                worldPop.resistance += 0.1
                worldPop.resistance = round(worldPop.resistance, 1)
            if event.key == pygame.K_MINUS:
                worldPop.resistance -= 0.1
                worldPop.resistance = round(worldPop.resistance, 1)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            displayWidth, displayHeight = event.w, event.h
            surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)

    iteration += 1
    screen.fill((0, 0, 0))

    worldPop.move(environment.gridSize, environment.plotSize)
    worldPop.reproduce(environment.plotSize, useOvercrowding)
    running = False if worldPop.findSurvivors(environment) == False or running == False else True

    #print("x: ", pygame.mouse.get_pos()[0]//environment.plotSize, "   y: ", pygame.mouse.get_pos()[1]//environment.plotSize)
    print(f'''
\n----------\n
Iteration: {iteration}
Pop Size: {len(worldPop.pop)}
Resistance: {worldPop.resistance}
''')

    if showEnv:
        environment.display(screen, displayHeight, displayWidth)
    if showPop:
        worldPop.display(screen, displayHeight, displayWidth, environment.gridSize, environment.plotSize)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
print('Done!')