import numpy

from week5.Transform import Transform

isTileInclude = False


class Heuristic:
    def __init__(self, goalState="123456780"):
        self.goalState = goalState

    def tilesDisplacedHeuristic(self, state):
        transform = Transform()
        currentPuzzleState = transform.convertStringToEightPuzzle(state)
        goalPuzzleState = transform.convertStringToEightPuzzle(self.goalState)
        h = 0
        for i in range(3):
            for j in range(3):
                if currentPuzzleState[i][j] != goalPuzzleState[i][j]:
                    h += 1
                if currentPuzzleState[i][j] == 0 and currentPuzzleState[i][j] != goalPuzzleState[i][
                    j] and isTileInclude == False:
                    h -= 1
        return h

    def manhattanHeuristic(self, state):
        transform = Transform()
        currentPuzzleState = transform.convertStringToEightPuzzle(state)
        goalPuzzleState = transform.convertStringToEightPuzzle(self.goalState)
        currentCoOrdinate = numpy.arange(18).reshape((9, 2))

        for i in range(3):
            for j in range(3):
                currentCoOrdinate[currentPuzzleState[i][j]][0] = i
                currentCoOrdinate[currentPuzzleState[i][j]][1] = j

        h = 0
        for i in range(3):
            for j in range(3):
                if goalPuzzleState[i][j] != 0:
                    h += abs(i - currentCoOrdinate[goalPuzzleState[i][j]][0]) + \
                         abs(j - currentCoOrdinate[goalPuzzleState[i][j]][1])
                if goalPuzzleState[i][j] == 0 and isTileInclude:
                    h += abs(i - currentCoOrdinate[goalPuzzleState[i][j]][0]) + \
                         abs(j - currentCoOrdinate[goalPuzzleState[i][j]][1])
        return h

    def getHeuristicEstimation(self, state, HeuristicChoice):
        return {
            1: self.tilesDisplacedHeuristic(state),
            2: self.manhattanHeuristic(state),
            3: self.manhattanHeuristic(state) + self.tilesDisplacedHeuristic(state),
            4: self.manhattanHeuristic(state) * self.manhattanHeuristic(state)
        }[HeuristicChoice]
