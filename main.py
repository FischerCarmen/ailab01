import random
import statistics
import time
import numpy

goalState = numpy.array(((0, 1, 2), (3, 4, 5), (6, 7, 8)))
calculationTimeHammingDistance = list()
calculationTimeManhattenDistance = list()
NodesExpandedHammingDistance = list()
NodesExpandedManhattenDistance = list()
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
    #print("Number of states:", states)
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
    #print(listOfStates)
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

    #print("Hamming Distance: ", distance)
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

    #print("Manhatten Distance: ", distance)
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
        #print(move)
        newState = state.copy()
        # phyton way of saying swap two objects a, b = b, a
        newState[startPositionOf0[0]][startPositionOf0[1]], newState[move[0]][move[1]] = newState[move[0]][move[1]], newState[startPositionOf0[0]][startPositionOf0[1]]
        nextCalculatedSteps.append(newState)

    return nextCalculatedSteps

def isNotInList(list, value) -> bool:
    for item in list:
        if numpy.array_equal(item, value):
            return False
    return True
def solveWithHeuristic(state, heuristic):
    gScore = 0
    openStates = list()
    closedStates = list()
    currentState = state
    currentFScore = gScore + heuristic(currentState)
    openStates.append((currentFScore, currentState))

    while True:

        if heuristic(currentState) == 0:
            if heuristic == hammingDistance:
                NodesExpandedHammingDistance.append(len(openStates) + len(closedStates))
            else:
                NodesExpandedManhattenDistance.append(len(openStates) + len(closedStates))
            return

        positionOf0 = findZero(currentState)
        allowedNextSteps = nextSteps(currentState, positionOf0, allowedMoves[positionOf0])

        for step in allowedNextSteps:
            if isNotInList(closedStates, step):
                fScore = gScore + heuristic(step)
                for state in openStates:
                    if numpy.array_equal(step, state[1]):
                        if state[0] > fScore:
                            openStates.remove((state[0], state[1]))
                            openStates.append((fScore, step))
                openStates.append((gScore + heuristic(step), step))


        closedStates.append(currentState)
        openStates.remove((currentFScore, currentState))
        openStates.sort(key=lambda x: x[0], reverse=False)
        currentState = openStates[0][1]
        currentFScore = openStates[0][0]



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

    hammingDistanceFunc = hammingDistance
    manhattenDistanceFunc = manhattenDistance
    heuristicList = [hammingDistanceFunc, manhattenDistanceFunc]

    aStar(startStates, heuristicList)

    print("STATISTICS FOR", len(calculationTimeManhattenDistance), "RUNS:")
    print("*** Hamming Distance ***")
    print("---Execution Time---")
    print("Mean:", statistics.mean(calculationTimeHammingDistance))
    print("Standard Deviation:", statistics.stdev(calculationTimeHammingDistance))
    print("---Number of Nodes Expanded---")
    print("Mean:", statistics.mean(NodesExpandedHammingDistance))
    print("Standard Deviation:", statistics.stdev(NodesExpandedHammingDistance))
    print("*** ManhattenDistance ***")
    print("---Execution Time---")
    print("Mean:", statistics.mean(calculationTimeManhattenDistance))
    print("standard deviation:", statistics.stdev(calculationTimeManhattenDistance))
    print("---Number of Nodes Expanded---")
    print("Mean:", statistics.mean(NodesExpandedManhattenDistance))
    print("standard deviation:", statistics.stdev(NodesExpandedManhattenDistance))
