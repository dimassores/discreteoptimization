import sys
import numpy as np
import gurobipy as gp
from gurobipy import GRB


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
    print(items_conections)
    print(number_of_edges)
    print(number_of_vertices)
    number_of_possible_colors = 2
    y = number_of_possible_colors
    nodes = number_of_vertices
    # Create a new model
    m = gp.Model("mip1")
    # Create decision variables for the RAP model
    xij = m.addVars(nodes, y, name="x", vtype=GRB.BINARY)
    yj = m.addVars(y, name="y", vtype=GRB.BINARY)
    # Set objective
    m.setObjective(yj.sum(), GRB.MINIMIZE)

    # Add constraint: each node uses exact one color
    one_color = m.addConstrs((xij.sum(i, "*") == 1 for i in range(y)), name="one_color")

    # Add constraint: adjacent nodes do not have the same color

    for row in range(0, nodes):
        for col in range(0, nodes):
            if col > row:
                if items_conections[row, col] == 1:
                    m.addConstrs(
                        (xij[row, j] + xij[col, j] <= 1 for j in range(y)),
                        name="adj_color",
                    )

    # constraint s.t. if node i is assigned color k, color k is used

    m.addConstrs(
        (xij[i, j] <= yj[j] for i in range(nodes) for j in range(y)),
        name="color_k_is_used",
    )

    # constrinat for upper bound on # of colors used
    m.addConstr(yj.sum() <= y, name="upper_bound")

    # Optimize model
    m.optimize()

    # for v in m.getVars():
    #     print("%s %g" % (v.varName, v.x))

    # setting the output to be as the assigment asks
    all_variables = [variable.varName for variable in m.getVars() if variable.x != 0]
    colors_index = [item.split("[")[1][0] for item in all_variables if "y" in item]
    color_of_each_item = [
        item.split(",")[1][0] for item in all_variables if "x" in item
    ]
    opt_value = len(colors_index)
    output_data = str(int(opt_value)) + " " + str(0) + "\n"
    output_data += " ".join(map(str, color_of_each_item))

    return output_data


# try:

#     # Create a new model
#     m = gp.Model("mip1")
#     nodes = 5
#     y = 5
#     # Create decision variables for the RAP model
#     xij = m.addVars(nodes, y, name="x", vtype=GRB.BINARY)
#     yj = m.addVars(y, name="y", vtype=GRB.BINARY)
#     # Set objective
#     m.setObjective(yj.sum(), GRB.MINIMIZE)

#     # Add constraint: each node uses exact one color
#     one_color = m.addConstrs((xij.sum(i, "*") == 1 for i in range(y)), name="one_color")

#     # Add constraint: adjacent nodes do not have the same color

#     for row in range(0, nodes):
#         for col in range(0, nodes):
#             if col > row:
#                 if items_conections[row, col] == 1:
#                     m.addConstrs(
#                         (xij[row, j] + xij[col, j] <= 1 for j in range(y)),
#                         name="adj_color",
#                     )

#     # constraint s.t. if node i is assigned color k, color k is used

#     m.addConstrs(
#         (xij[i, j] <= yj[j] for i in range(nodes) for j in range(y)),
#         name="color_k_is_used",
#     )

#     # constrinat for upper bound on # of colors used
#     m.addConstr(yj.sum() <= y, name="upper_bound")

#     # Optimize model
#     m.optimize()

#     for v in m.getVars():
#         print("%s %g" % (v.varName, v.x))
#     all_variables = [variable.varName for variable in m.getVars() if variable.x != 0]
#     colors_index = [item.split("[")[1][0] for item in all_variables if "y" in item]
#     color_of_each_item = [
#         item.split(",")[1][0] for item in all_variables if "x" in item
#     ]
#     opt_value = len(colors_index)
#     output_data = str(int(opt_value)) + " " + str(0) + "\n"
#     output_data += " ".join(map(str, color_of_each_item))
#     print(output_data)

#     # print("Obj: %g" % m.objVal)

# except gp.GurobiError as e:
#     print("Error code " + str(e.errno) + ": " + str(e))

# except AttributeError:
#     print("Encountered an attribute error")

if __name__ == "__main__":
    input_data = read_data(sys.argv[1])
    solve_it(input_data)
