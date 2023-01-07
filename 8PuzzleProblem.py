""" 
    Author   : Ajinkya Sonawane
"""

import random
import numpy
import datetime
from copy import deepcopy
import statistics

goal = numpy.array(((0, 1, 2), (3, 4, 5), (6, 7, 8)))


def choose_permutations():
    # This function lets the user specify the number of permutations to be run
    random_input = ""
    while random_input.isdigit() is False:
        random_input = input("\nPlease indicate the number of permutations you want to run: ")
        if random_input.isdigit() is False:
            print("Invalid input! Please enter a number.")
        else:
            return int(random_input)


def generate_start_array():
    newState = numpy.array(((0, 1, 2), (3, 4, 5), (6, 8, 7)))
    while is_solvable(newState) is False:
        listOfValues = list(range(9))
        for i in range(3):
            for ii in range(3):
                value = random.choice(listOfValues)
                listOfValues.remove(value)
                newState[i][ii] = value
    return newState


def generate_start_arrays(number: int):
    start_arrays = list()
    appended_array = 0
    while appended_array < number:
        list_of_values = list(range(9))
        new_array = numpy.array(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
        for i in range(3):
            for ii in range(3):
                value = random.choice(list_of_values)
                list_of_values.remove(value)
                new_array[i][ii] = value
        if is_solvable(new_array):
            start_arrays.append(new_array)
            appended_array += 1
    return start_arrays


class Node:
    def __init__(self, data, level, fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.parent = None
        self.level = level
        self.fval = fval

    def generate_children(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x, y = self.find_zero(self.data)
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                child_node.parent = self
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = deepcopy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def find_zero(self, puz):
        """ Specifically used to find the position of the blank space """
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if puz[i][j] == 0:
                    return i, j


def is_solvable(start):
    i = start[start != 0]
    inversions = sum(len(numpy.array(numpy.where(i[ii + 1:] < i[ii])).reshape(-1)) for ii in range(len(i) - 1))
    return inversions % 2 == 0


class Puzzle:
    def __init__(self, start):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.start = start
        self.open = []
        self.closed = []

    def f(self, current, heuristic):
        """ Heuristic Function to calculate heuristic value f(x) = h(x) + g(x) """
        if heuristic == "hamming":
            return self.h_hamming(current.data) + current.level
        elif heuristic == "manhattan":
            return self.h_manhattan(current.data) + current.level
        else:
            print("Error: undefined heuristic chosen")

    def h_hamming(self, current):
        """ Calculates the different between the given puzzles """
        distance = 0
        for i in range(3):
            for j in range(3):
                if current[i][j] != goal[i][j]:
                    distance += 1
        return distance

    def h_manhattan(self, current):
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
            for j in range(3):
                value = current[i][j]
                goal = coordinatesDict.get(value)
                distance += (abs(i - goal[0]) + abs(j - goal[1]))
        return distance

    def get_node_from_open(self, data):
        for existing_node in self.open:
            if numpy.array_equal(existing_node.data, data):
                return existing_node

    def is_node_in_list(self, nodes, new_node):
        unique = []
        for node in nodes:
            if numpy.array_equal(node.data, new_node.data):
                unique.append(1)
            else:
                unique.append(0)
        return any(unique)

    def process(self, heuristic):
        start_node = Node(self.start, -1, 0)
        start_node.fval = self.f(start_node, heuristic)
        # Put the start node in the open list"""
        self.open.append(start_node)
        while True:
            current_node = self.open[0]
            # If the difference between current and goal node is 0 we have reached the goal node
            if self.h_manhattan(current_node.data) == 0:
                print("Puzzle solved")
                path = []
                current = current_node
                while current is not None:
                    path.append(current.data)
                    current = current.parent
                path = path[::-1]  # Reverse path
                # for node in path:
                #     print(node)
                return path

            current_children = current_node.generate_children()
            for child in current_children:
                child.fval = self.f(child, heuristic)
                if not self.is_node_in_list(self.closed, child):
                    if not self.is_node_in_list(self.open, child):
                        child.parent = current_node
                        self.open.append(child)
                    else:
                        existing_node = self.get_node_from_open(child.data)
                        if child.level < existing_node.level:
                            self.open.append(child)

            self.closed.append(current_node)
            del self.open[0]
            # sort the open list based on f value """
            self.open.sort(key=lambda x: x.fval, reverse=False)


class Multiple_puzzle_solver:
    def __init__(self, permutations: int, start_arrays, heuristic):
        self.permutations = permutations
        self.start_arrays = start_arrays
        self.heuristic = heuristic
        self.nodes_explored = list()
        self.execution_time = list()

    def print_statistics(self):
        print("\nStatistics after", self.permutations, "permutations (mean " u"\u00B1" " standard deviation):")
        print(("Nodes explored: {} " u"\u00B1" " {}"
               "\nSearch time [seconds]: {} " u"\u00B1" " {}").format(
            int(round(statistics.mean(self.nodes_explored), 0)), int(round(statistics.stdev(self.nodes_explored), 0)),
            round(statistics.mean(self.execution_time), 2), round(statistics.stdev(self.execution_time), 2)))

    def run(self):
        print("\nStarting calculation using", self.heuristic, "algorithm...")
        run = 1
        for start_array in self.start_arrays:
            print("Running permutation", run, "of", permutations)
            start_time = datetime.datetime.now()
            puz = Puzzle(start_array)
            puz.process(self.heuristic)
            end_time = datetime.datetime.now()
            time_diff = (end_time - start_time).total_seconds()
            self.execution_time.append(time_diff)
            self.nodes_explored.append(len(puz.open))
            run += 1


if __name__ == '__main__':
    permutations = choose_permutations()
    start_arrays = generate_start_arrays(permutations)
    mps = Multiple_puzzle_solver(permutations, start_arrays, "manhattan")
    mps.run()
    mps.print_statistics()

    # mps = Multiple_puzzle_solver(permutations, start_arrays, "hamming")
    # mps.run("")
    # mps.print_statistics()
