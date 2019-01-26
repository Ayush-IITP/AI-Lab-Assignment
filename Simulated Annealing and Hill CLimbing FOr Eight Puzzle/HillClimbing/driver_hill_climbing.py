from HillClimbing import hill_climbing
import Heuristic
from datetime import datetime


def write_to_file(file, heuristic_choice, start_state, goal_state):
    file.write("Heuristic Chosen : ")
    if heuristic_choice == 1:
        file.write("number of tiles displaced from their destined position \n")
    elif heuristic_choice == 2:
        file.write("Total Manhattan distance \n")
    else:
        file.write("Total Manhattan distance + number of tiles displaced from their destined position\n")
    file.write("Start State : \n")
    file.write(start_state[:3] + "\n" + start_state[3:6] + "\n" + start_state[6:] + "\n")
    file.write("Goal State : \n")
    file.write(goal_state[:3] + "\n" + goal_state[3:6] + "\n" + goal_state[6:] + "\n")
    file.close()


def main():
    startState = ""
    goalState = ""
    file = open("hill_climbing_result.txt", "w+")

    with open("A*StartState") as f:
        for line in f:
            line = line.strip()
            line = line.replace(" ", "")
            startState += line

    with open("A*GoalState") as f:
        for line in f:
            line = line.strip()
            line = line.replace(" ", "")
            goalState += line

    startState = startState.replace("B", "0")

    goalState = goalState.replace("B", "0")

    displayMenu()
    HeuristicChoice = int(input("Waiting for Choice"))
    write_to_file(file, HeuristicChoice, startState, goalState)
    is_tile_included = int(input("Enter 1 if consider tile as another tile else 0 \n"))
    if is_tile_included:
        Heuristic.isTileInclude = True

    start_time = datetime.now()
    puzzle_solver = hill_climbing(startState, goalState)
    status = puzzle_solver.solve_eight_puzzle(startState, HeuristicChoice)
    file = open("hill_climbing_result.txt", "a")
    if status == 1:
        file.write("Search Status : Failed\n")
    file.write("Time Taken : {} ".format(str(datetime.now() - start_time)))
    file.close()


def displayMenu():
    print("Enter Choice depending on Heuristic :")
    print("1.h1(n) = number of tiles displaced from their destined position")
    print("2.h​2 ​(n)= Total Manhattan distance")
    print("3.h3(n)= h1(n) + h2(n)")


if __name__ == '__main__':
    main()
