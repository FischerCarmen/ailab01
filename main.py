import random
import statistics
import time

import numpy

goalState = numpy.array(((0, 1, 2), (3, 4, 5), (6, 7, 8)))
calculationTimeHammingDistance = list()
calculationTimeManhattenDistance = list()
allowedMoves = dict([((0, 0), ((0, 1), (1, 0))),
                     ((0, 1), ((0, 0), (0, 2), (1, 1))),
                     ((0, 2), ((0, 1), (1, 2))),
                     ((1, 0), ((0, 0), (1, 1), (2, 0))),
                     ((1, 1), ((0, 1), (1, 0), (1, 2), (2, 1))),
                     ((1, 2), ((0, 2), (1, 1), (2, 2))),
                     ((2, 0), ((1, 0), (2, 1))),
                     ((2, 1), ((2, 0), (2, 2), (1, 1))),
                     ((2, 2), ((2, 1), (1, 2)))])


# generates stated number of start states to solve
def generateStates(states: int) -> list:
    print("Number of states:", states)
    listOfStates = list()
    appendedState = 0
    while appendedState < states:
        listOfValues = list(range(9))
        newState = numpy.array(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
        for i in range(3):
                for ii in range(3):
                    value = random.choice(listOfValues)
                    listOfValues.remove(value)
                    newState[i][ii] = value
        if isSolvable(newState):
            listOfStates.append(newState)
            appendedState += 1
    return listOfStates

def isSolvable(state) -> bool:
    i = state[state != 0]
    inversions = sum(len(numpy.array(numpy.where(i[ii + 1:] < i[ii])).reshape(-1)) for ii in range(len(i) - 1))
    return inversions % 2 == 0

# calculates the hamming distance of a given state
def hammingDistance(state) -> int:
    if len(state) != len(goalState):
        raise Exception("states do not have the same length")
    distance = 0
    for i in range(3):
        for ii in range(3):
            if state[i][ii] != goalState[i][ii]:
                distance += 1
    print("Hamming Distance: ", distance)
    return distance


# calculates the manhatten distance of a given state
def manhattenDistance(state) -> int:
    if len(state) != len(goalState):
        raise Exception("states do not have the same length")
    distance = 0
    coordinatesDict = dict([(0, (0, 0)),
                            (1, (0, 1)),
                            (2, (0, 2)),
                            (3, (1, 0)),
                            (4, (1, 1)),
                            (5, (1, 2)),
                            (6, (2, 0)),
                            (7, (2, 1)),
                            (8, (2, 2))])
    for i in range(3):
        for ii in range(3):
            value = state[i][ii]
            goal = coordinatesDict.get(value)
            distance += (abs(i-goal[0]) + abs(ii-goal[1]))
    print("Manhatten Distance: ", distance)
    return distance


# finds the empty position in a state
def findZero(state) -> tuple:
    for i in range(len(state)):
        for ii in range(len(state[i])):
            if state[i][ii] == 0:
                return i, ii


# calculates all allowed new states from a given sate
def nextSteps(state, startPositionOf0, currentAllowedMoves) -> list:
    nextCalculatedSteps = list()
    for move in currentAllowedMoves:
        print(move)
        newState = state.copy()
        # phyton way of saying swap two objects a, b = b, a
        newState[startPositionOf0[0]][startPositionOf0[1]], newState[move[0]][move[1]] = newState[move[0]][move[1]], newState[startPositionOf0[0]][startPositionOf0[1]]
        nextCalculatedSteps.append(newState)
    return nextCalculatedSteps


# solves a given state
def solveHamming(state):
    gScore = 0
    fScores = list()
    processedStates = list()
    processedStates.append(state)
    openStates = dict()
    heuristicValueOfState = hammingDistance(state)
    openStates.update({state, heuristicValueOfState})
    currentState = state
    while not (numpy.array_equal(currentState, goalState)):
        print("currentState:\n", currentState)
        startPositionOf0 = findZero(currentState)
        currentPossibleMoves = allowedMoves.get(startPositionOf0)
        nextPossibleStates = nextSteps(currentState, startPositionOf0, currentPossibleMoves)
        for state in nextPossibleStates:
            print("possibility:\n", state)
            index = 0
            for processedState in processedStates:
                if numpy.array_equal(state, processedState):
                    print("State in processedStates -> to be removed:\n", nextPossibleStates[index])
                    del nextPossibleStates[index]
            index += 1
        print("nextPossibleStates:\n", nextPossibleStates)
        for state in nextPossibleStates:
            hScore = hammingDistance(state)
            fScores.append(hScore + gScore)
            if not (state in openStates):
                openStates.update({state, hScore + gScore})
            else:
                if openStates.get(state) > hScore + gScore:
                    openStates.update({state, hScore + gScore})
        if not (currentState in processedStates):
            processedStates.append(currentState)
            openStates.pop(currentState)
        else:
            while not (currentState in processedStates):
                nextState = openStates[fScores.index(min(fScores))]
            if not (currentState in processedStates):
                processedStates.append(currentState)
        print("nextState chosen:\n", nextState)
        processedStates.append(nextState)
        gScore += 1
        fScores.clear()
        currentState = nextState


def solveManhatten(state):
    gScore = 0
    fScores = list()
    closedStates = list()
    openStates = list()
    openStates.append(state)
    nextState = state
    currentState = nextState
    while not (numpy.array_equal(currentState, goalState)):
        startPositionOf0 = findZero(currentState)
        currentAllowedMoves = allowedMoves.get(startPositionOf0)
        nextAllowedSteps = nextSteps(currentState, startPositionOf0, currentAllowedMoves)
        openStates.append(nextAllowedSteps)
        for step in nextAllowedSteps:
            hScore = manhattenDistance(step)
            print("Where")
            fScores.append(hScore + gScore)
            print("the")
            nextState = nextAllowedSteps[fScores.index(min(fScores))]
            print("fuck")
        if not (currentState in closedStates):
            closedStates.append(currentState)
        else:
            while not (currentState in closedStates):
                nextAllowedSteps.remove(nextState)
                nextState = nextAllowedSteps[fScores.index(min(fScores))]
            if not (currentState in closedStates):
                closedStates.append(currentState)
        print("Am")
        gScore += 1
        print("I")
        fScores.clear()
        print("?")
        currentState = nextState
        print(nextState)

def solveWithHeuristic(state, heuristic):
    # stateType = [("board", list), das brauchen wir noch
   #              ("parent", int),
    #             ("gFunction", int),
     #            ("hFunction", int)]
    gScore = 0
    fScores = list()
    processedStates = list()
    processedStates.append(state)
    openStates = dict()
    heuristicValueOfState = heuristic(state)
    openStates.update({state, heuristicValueOfState})
    currentState = state
    while not (numpy.array_equal(currentState, goalState)):
        print("currentState:\n", currentState)
        startPositionOf0 = findZero(currentState)
        currentPossibleMoves = allowedMoves.get(startPositionOf0)
        nextPossibleStates = nextSteps(currentState, startPositionOf0, currentPossibleMoves)
        for state in nextPossibleStates:
            print("possibility:\n", state)
            index = 0
            for processedState in processedStates:
                if numpy.array_equal(state, processedState):
                    print("State in processedStates -> to be removed:\n", nextPossibleStates[index])
                    del nextPossibleStates[index]
            index += 1
        print("nextPossibleStates:\n", nextPossibleStates)
        for state in nextPossibleStates:
            hScore = heuristic(state)
            fScores.append(hScore + gScore)
            if not (state in openStates):
                openStates.update({state, hScore + gScore})
            else:
                if openStates.get(state) > hScore + gScore:
                    openStates.update({state, hScore + gScore})
        if not (currentState in processedStates):
            processedStates.append(currentState)
            openStates.pop(currentState)
        else:
            while not (currentState in processedStates):
                nextState = openStates[fScores.index(min(fScores))]
            if not (currentState in processedStates):
                processedStates.append(currentState)
        print("nextState chosen:\n", nextState)
        processedStates.append(nextState)
        gScore += 1
        fScores.clear()
        currentState = nextState

# runs the A* Algorithm
def aStar(states, heuristics):

    # uses the hamming distance
    for state in states:
        startTime = time.time()
        solveWithHeuristic(state, heuristics[0])
        endTime = time.time()
        calculationTimeHammingDistance.append(endTime-startTime)

    # uses the manhatten distance
    for state in states:
        startTime = time.time()
        solveWithHeuristic(state, heuristics[1])
        endTime = time.time()
        calculationTimeManhattenDistance.append(endTime-startTime)


# program starts here
if __name__ == '__main__':
    runs = int(input("Please enter the number of samples to run:"))
    startStates = generateStates(runs)
#    for state in startStates:
#        manhattenDistance(state)
#        hammingDistance(state)
    hammingDistanceFunc = hammingDistance
    manhattenDistanceFunc = manhattenDistance
    heuristicList = [hammingDistanceFunc, manhattenDistanceFunc]
    aStar(startStates, heuristicList)
    print("STATISTICS FOR ", len(calculationTimeManhattenDistance), "RUNS:")
    print("*** Hamming Distance ***")
    print("---Execution Time---")
    print("Mean:", statistics.mean(calculationTimeHammingDistance))
    print("standard deviation:", statistics.stdev(calculationTimeHammingDistance))
    print("*** ManhattenDistance ***")
    print("---Execution Time---")
    print("Mean:", statistics.mean(calculationTimeManhattenDistance))
    print("standard deviation:", statistics.stdev(calculationTimeManhattenDistance))
