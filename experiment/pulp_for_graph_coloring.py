from pulp import *
import sys
from collections import namedtuple
from typing import List, NamedTuple
import numpy as np

# https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99
# Item = namedtuple("Item", ["index", "color", "item_conections"])


class Item(NamedTuple):
    """ 
	"""

    index: int
    color: int
    item_conections_index: List[int]


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

    # all_items = set([line.split()[0] for line in lines[1:]])
    # items_list = [Item(int(item), None, []) for item in all_items]
    # for i in range(1, number_of_edges + 1):
    #     line = lines[i]
    #     parts = line.split()
    #     items.append(Item(int(parts[0]), None, []))
    return items_conections, number_of_edges, number_of_vertices


def read_data(file_location):
    with open(file_location, "r") as input_data_file:
        output_data = input_data_file.read()
    return output_data


def solve_it(input_data):
    item_list, K, _ = structure(input_data)

    items = [item.index for item in item_list]
    value = dict(zip(items, [item.value for item in item_list]))
    weight = dict(zip(items, [item.weight for item in item_list]))

    prob = LpProblem("knapsack", LpMaximize)
    decision_vars = LpVariable.dicts("item", items, cat="Binary")
    prob += lpSum([value[i] * decision_vars[i] for i in items])
    prob += lpSum([weight[f] * decision_vars[f] for f in items]) <= K
    prob.solve()

    name_piked = [
        variable.name for variable in prob.variables() if variable.varValue != 0
    ]

    picked = [item for item in item_list if "item_" + item.index in name_piked]
    taken = [0 if item not in picked else 1 for item in item_list]

    opt_value = sum([item.value for item in picked])
    output_data = str(int(opt_value)) + " " + str(1) + "\n"
    output_data += " ".join(map(str, taken))
    return output_data


if __name__ == "__main__":
    string_file = read_data(sys.argv[1])
    print(structure(string_file))

