import sys
import numpy as np
from pulp import *


# https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99


def structure(input_data):
    """
    """
    lines = input_data.split("\n")
    firstLine = lines[0].split()
    number_of_vertices = int(firstLine[0])
    number_of_edges = int(firstLine[1])
    items_conections = np.around(np.empty([number_of_vertices, number_of_vertices]))
    for i in range(1, number_of_edges + 1):
        line = lines[i]
        parts = line.split()
        items_conections[int(parts[0]), int(parts[1])] = 1
        items_conections[int(parts[1]), int(parts[0])] = 1

    return items_conections, number_of_edges, number_of_vertices


def read_data(file_location):
    with open(file_location, "r") as input_data_file:
        output_data = input_data_file.read()
    return output_data


def solve_it(input_data, number_of_possible_colors=100):
    items_conections, number_of_edges, number_of_vertices = structure(input_data)
    y = range(number_of_possible_colors)
    nodes = range(number_of_vertices)

    # initializes lp problem
    lp = LpProblem("Coloring Problem", LpMinimize)

    # variables x_ij to indicate whether node i is colored by color j;
    xij = LpVariable.dicts("x", (nodes, y), lowBound=0, upBound=1, cat="Integer")

    # variables yj to indicate whether color j was used
    yj = LpVariable.dicts("y", y, lowBound=0, upBound=1, cat="Integer")

    # objective is the sum of yj over all j
    obj = lpSum(yj[j] for j in y)
    lp += obj, "Objective Function"

    # constraint s.t. each node uses exactly 1 color
    for r in nodes:
        jsum = 0.0
        for j in y:
            jsum += xij[r][j]
        lp += jsum == 1, ""

    # constraint s.t. adjacent nodes do not have the same color
    for row in range(0, number_of_vertices):
        for col in range(0, number_of_vertices):
            if items_conections[row, col] == 1:
                for j in y:
                    lp += xij[row][j] + xij[col][j] <= 1, ""

    # constraint s.t. if node i is assigned color k, color k is used
    for i in nodes:
        for j in y:
            lp += xij[i][j] <= yj[j], ""

    # constrinat for upper bound on # of colors used
    lp += lpSum(yj[j] for j in y) <= number_of_possible_colors, ""

    lp.solve()

    all_variables = [
        variable.name for variable in lp.variables() if variable.varValue != 0
    ]

    # setting the structure to be as the assigment asks
    colors_index = [item.split("_")[1] for item in all_variables if "y_" in item]
    color_of_each_item = [item.split("_")[2] for item in all_variables if "x_" in item]
    opt_value = len(colors_index)
    output_data = str(int(opt_value)) + " " + str(0) + "\n"
    output_data += " ".join(map(str, color_of_each_item))
    return output_data


if __name__ == "__main__":
    string_file = read_data(sys.argv[1])
    print(solve_it(string_file))

