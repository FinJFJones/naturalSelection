## Modules ##
import random
import operator
import pygame
## Files ##
import functions

class Population:
    def __init__(self, size, home, birthRate, startingColours, resistance):
        self.size = size
        self.home = home
        self.birthRate = birthRate
        self.resistance = resistance
        self.pop = []

        for i in range(self.size):
            self.pop.append([(startingColours[0], startingColours[1], startingColours[2]), tuple(map(operator.add, self.home, (random.randint(-10, 10), random.randint(-10, 10))))])

    def display(self, screen, displayHeight, displayWidth, gridSize, plotSize):
        blobSize = max(1, min(displayHeight, displayWidth)//(gridSize*plotSize))

        for blob in self.pop:
            pygame.draw.circle(screen, blob[0], tuple(centre//((gridSize*plotSize)/min(displayHeight, displayWidth)) for centre in blob[1]), blobSize)

    def move(self, gridSize, plotSize):
        for i in range(len(self.pop)):
            x, y = self.pop[i][1]
            dx, dy = (random.randint(-1, 1), random.randint(-1, 1))
            
            newX = max(0, min(x + dx, (gridSize*plotSize)-1))
            newY = max(0, min(y + dy, (gridSize*plotSize)-1))

            self.pop[i][1] = (newX, newY)
    
    def reproduce(self, plotSize, useOvercrowding):
        parentList = self.pop.copy()
        for i in range(len(self.pop)):
            if random.random() < self.birthRate and self.pop[i] in parentList:
                parentList.remove(self.pop[i])
                closestBlob = self.findClosestBlob(self.pop[i][1], parentList, plotSize)
                partner, distance = closestBlob if closestBlob != None else (None, None)
                if partner != None and (False if useOvercrowding and distance != None and distance < 5 else True):
                    self.pop.append([functions.calculateAverage([self.pop[i][0], partner[0]]), functions.calculateAverage([self.pop[i][1], partner[1]])])
                    self.pop[-1] = [functions.applyMutation(self.pop[-1][0], 3), self.pop[-1][1]] # Child mutation

    def distanceBetweenPoints(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    
    def findInRangeBlob(self, target, pointList, threshold):
        for point in pointList:
            distance = self.distanceBetweenPoints(target, point[1])
            if distance < threshold:
                return point, distance
            
        return None

    def findClosestBlob(self, target, pointList, threshold):
        closestPoint = None
        minDistance = float('inf')

        for point in pointList:
            distance = self.distanceBetweenPoints(target, point[1])
            if distance < minDistance and distance < threshold:
                minDistance = distance
                closestPoint = point

        return closestPoint, minDistance

    def findSurvivors(self, environment):
        for blob in self.pop:
            popCopy = self.pop.copy()
            popCopy.remove(blob)
            if max(0, random.random()+self.resistance) < functions.colourDistance(blob[0], environment.plots[blob[1][0]//environment.plotSize][blob[1][1]//environment.plotSize]):
                self.pop.remove(blob)

        return True if len(self.pop) > 0 else False
        
class Environment:
    def __init__(self, gridSize, plotSize, seed):
        self.gridSize = gridSize
        self.plotSize = plotSize
        self.plots = []

        for width in range(gridSize):
            self.plots.append([])
            for length in range(gridSize):
                self.plots[width].append((None, None, None))
        
        self.plots[0][0] = seed

        for x in range(gridSize):
            for y in range(gridSize):
                neighbouringPlots = []
                if self.plots[x][y] == (None, None, None):
                    if (x-1) >= 0:
                        if self.plots[x-1][y] != (None, None, None):
                            neighbouringPlots.append(self.plots[x-1][y])
                    if (x+1) <= gridSize-1:
                        if self.plots[x+1][y] != (None, None, None):
                            neighbouringPlots.append(self.plots[x+1][y])
                    if (y-1) >= 0:
                        if self.plots[x][y-1] != (None, None, None):
                            neighbouringPlots.append(self.plots[x][y-1])
                    if (y+1) <= gridSize-1:
                        if self.plots[x][y+1] != (None, None, None):
                            neighbouringPlots.append(self.plots[x][y+1])
                    
                    self.plots[x][y] = functions.calculateAverage(neighbouringPlots)
                    self.plots[x][y] = functions.applyMutation(self.plots[x][y], 2) # mutationRate = 4 is up to 10 rgb change for each colour

    def display(self, screen, displayHeight, displayWidth):
        blockSize = max(1, min(displayHeight, displayWidth)//self.gridSize)

        for x in range(self.gridSize):
            for y in range(self.gridSize):
                pygame.draw.rect(screen, self.plots[x][y], pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize))
