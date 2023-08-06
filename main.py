## Modules ##
import pygame
import multiprocessing
## Files ##
import classes

def gameLogicProcess(worldPop, environment, settings, worldPopLock, environmentLock, settingsLock):
    useOvercrowding = settings['useOvercrowding']

    while settings['running'] == True:
        with worldPopLock, environmentLock, settingsLock:
            worldPop.move(environment.gridSize, environment.plotSize)
            worldPop.reproduce(environment.plotSize, useOvercrowding)
            settings['running'] = False if worldPop.findSurvivors(environment) == False or settings['running'] == False else True

def renderProcess(worldPop, environment, settings, worldPopLock, environmentLock, settingsLock):
    pygame.init()

    displayWidth, displayHeight = settings['displayWidth'], settings['displayHeight']

    screen = pygame.display.set_mode([displayWidth, displayHeight], pygame.RESIZABLE)
    clock = pygame.time.Clock()
    FPS = settings['FPS']
    iteration = 0

    showEnv, showPop = settings['showEnv'], settings['showPop']

    with worldPopLock, environmentLock, settingsLock:
        while settings['running']:
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
                    settings['running'] = False
                if event.type == pygame.VIDEORESIZE:
                    displayWidth, displayHeight = event.w, event.h
                    screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)

            iteration += 1
            screen.fill((0, 0, 0))

            #print("x: ", pygame.mouse.get_pos()[0]//environment.plotSize, "   y: ", pygame.mouse.get_pos()[1]//environment.plotSize)
            print(f'\n----------\n\nIteration: {iteration}\nPop Size: {len(worldPop.pop)}\nResistance: {worldPop.resistance}\n')

            if showEnv:
                environment.display(screen, displayHeight, displayWidth)
            if showPop:
                worldPop.display(screen, displayHeight, displayWidth, environment.gridSize, environment.plotSize)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    environment = classes.Environment(10, 50, (255, 105, 180))
    worldPop = classes.Population(2, ((environment.gridSize//2)*environment.plotSize, (environment.gridSize//2)*environment.plotSize), 0.3, (255, 105, 180), 0.3) # Home in centre
    #worldPop = classes.Population(100, (1, 1), 0.3, (200, 100, 180), 0.5) # Home at 1, 1
    settings = {
        'displayWidth': 500,
        'displayHeight': 500,
        'FPS': 60,
        'showEnv': True,
        'showPop': True,
        'useOvercrowding': True,
        'running': True
    }
    
    environmentLock = multiprocessing.Lock()
    worldPopLock = multiprocessing.Lock()
    settingsLock = multiprocessing.Lock()

    gameLogicProc = multiprocessing.Process(target=gameLogicProcess, args=(worldPop, environment, settings, worldPopLock, environmentLock, settingsLock))
    renderingProc = multiprocessing.Process(target=renderProcess, args=(worldPop, environment, settings, worldPopLock, environmentLock, settingsLock))

    gameLogicProc.start()
    renderingProc.start()

    gameLogicProc.join()
    renderingProc.join()