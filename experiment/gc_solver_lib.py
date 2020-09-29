# https://towardsdatascience.com/colour-maps-using-integer-programming-e46b6297aad4
from vertex_colorer.solver import Solver

adj_matrix = [
    [1, 1, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1],
]
solver = Solver(adj_matrix)
solver.solve("IP")

print(solver.solution)
