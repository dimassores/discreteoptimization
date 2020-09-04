#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
from pulp import *
import sys

Item = namedtuple("Item", ["index", "value", "weight"])


def structure(input_data):
    """
    """
    lines = input_data.split("\n")
    firstLine = lines[0].split()
    number_of_items = int(firstLine[0])
    K = int(firstLine[1])
    items = []
    for i in range(1, number_of_items + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(str(i - 1), int(parts[0]), int(parts[1])))
    return items, K, number_of_items


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
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
        )
