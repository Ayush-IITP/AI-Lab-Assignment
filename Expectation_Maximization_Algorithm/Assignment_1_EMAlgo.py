import random

observations = []
indicatorVariable = []


def generateData(p, p1, p2):
    for i in range(100000):
        r = random.uniform(0, 1)
        if r <= p:
            chosenCoin = 'Coin1'
        else:
            chosenCoin = 'Coin2'
        randForCoinSide = random.uniform(0, 1)
        if chosenCoin == 'Coin1':
            observations.append('H') if randForCoinSide <= p1 else observations.append('T')
        else:
            observations.append('H') if randForCoinSide <= p2 else observations.append('T')

    for observation in observations:
        indicatorVariable.append(1) if observation == 'H' else indicatorVariable.append(0)


def populateExpectation(expectation, pStart, p1Start, p2Start):
    for i in range(len(indicatorVariable)):
        term1 = pStart * pow(p1Start, indicatorVariable[i]) * pow(1 - p1Start, 1 - indicatorVariable[i])
        term2 = (1 - pStart) * pow(p2Start, indicatorVariable[i]) * pow(1 - p2Start, 1 - indicatorVariable[i])
        expectation.append(term1 / (term1 + term2))


def updateChoosingCoin1Probabiliy(expectations):
    c1Count = 0
    for expectation in expectations:
        c1Count += expectation
    return c1Count / len(indicatorVariable)


def updateHeadProbabiliyForCoin2(expectations):
    headCount = sum(indicatorVariable)
    headCountC1 = 0
    for i in range(len(expectations)):
        headCountC1 = headCountC1 + expectations[i] * indicatorVariable[i]
    c1Count = 0
    for expectation in expectations:
        c1Count += expectation
    return (headCount - headCountC1) / (len(indicatorVariable) - c1Count)


def updateHeadProbabiliyForCoin1(expectations):
    headCountC1 = 0
    for i in range(len(expectations)):
        headCountC1 = headCountC1 + expectations[i] * indicatorVariable[i]
    c1Count = 0
    for expectation in expectations:
        c1Count += expectation
    return headCountC1 / c1Count


def estimateProbabilityWithEM():
    isConverged = False
    epsilon = 0.000000000000001
    pCur = 0.1
    p1Cur = 0.1
    p2Cur = 0.1
    while not isConverged:

        expectations = []
        populateExpectation(expectations, pCur, p1Cur, p2Cur)

        pUpd = updateChoosingCoin1Probabiliy(expectations)
        p1Upd = updateHeadProbabiliyForCoin1(expectations)
        p2Upd = updateHeadProbabiliyForCoin2(expectations)

        if abs(pUpd - pCur) <= epsilon and abs(p1Upd - p1Cur) <= epsilon and abs(p2Upd - p2Cur) <= epsilon:
            isConverged = True
            print("Result Converged to value: ")
        print(pUpd, p1Upd, p2Upd)
        pCur = pUpd
        p1Cur = p1Upd
        p2Cur = p2Upd


def startProcess():
    p = float(input("Enter the probability Of choosing Coin 1 : "))
    p1 = float(input("Enter the probability of getting Head on Coin 1 : "))
    p2 = float(input("Enter the probability of getting Head on COin 2 : "))

    # Calling generateData() to generate the data
    generateData(p, p1, p2)
    # print(observations)
    estimateProbabilityWithEM()


if __name__ == '__main__':
    startProcess()
