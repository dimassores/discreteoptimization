#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pulp as pl


def structure(input_data: str):
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


def read_data(file_location: str):
    with open(file_location, "r") as input_data_file:
        output_data = input_data_file.read()
    return output_data


def solve_it(input_data: str):
    items_conections, number_of_edges, number_of_vertices = structure(input_data)
    number_of_possible_colors = int(number_of_vertices)
    y = range(number_of_possible_colors)
    nodes = range(number_of_vertices)

    # initializes lp problem
    lp = pl.LpProblem("Coloring Problem", pl.LpMinimize)

    # variables x_ij to indicate whether node i is colored by color j;
    xij = pl.LpVariable.dicts("x", (nodes, y), cat="Binary")

    # variables yj to indicate whether color j was used
    yj = pl.LpVariable.dicts("y", y, cat="Binary")

    # objective is the sum of yj over all j
    obj = pl.lpSum(yj[j] for j in y)
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
    lp += pl.lpSum(yj[j] for j in y) <= number_of_possible_colors, ""

    # solves lp and prints optimal solution/objective value
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
    input_data = read_data(sys.argv[1])
    solve_it(input_data)
