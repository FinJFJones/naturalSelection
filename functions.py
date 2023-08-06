import random
import math

def calculateAverage(tupleList):
    tupleLen = len(tupleList[0])
    averages = []
    
    for i in range(tupleLen):
        total = 0
        for t in tupleList:
            total += t[i]
        average = total / len(tupleList)
        averages.append(int(average))
    
    return tuple(averages)

def applyMutation(givenTuple, mutationRate):
    mutatedList = []
    for value in givenTuple:
        mutationRange = (mutationRate * 255) // 100
        mutatedValue = value + random.randint(-mutationRange, mutationRange)
        mutatedValue = max(0, min(255, mutatedValue))
        mutatedList.append(mutatedValue)

    return tuple(mutatedList)

def colourDistance(rgbColour1, rgbColour2):
    distance = math.sqrt((rgbColour1[0]-rgbColour2[0])**2+(rgbColour1[1]-rgbColour2[1])**2+(rgbColour1[2]-rgbColour2[2])**2)
    distPercentage = distance/math.sqrt(195075)

    return distPercentage