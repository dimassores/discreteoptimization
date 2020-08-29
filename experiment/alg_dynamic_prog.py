import numpy as np
value = [0, 5, 6, 3]
weight = [0, 4, 5, 2]
K = 9
number_of_items = 3
opt_matrix = np.empty([K+1, number_of_items+1])


def search_dynamic(weight_list, value_list, item_position, k_limit, opt_matrix_current):
    ''' search_dynamic '''
    if item == 0:
        return 0
    elif weight_list[item_position] <= k_limit:
        max_value = max(opt_matrix_current[k_limit, item_position - 1],
                        value_list[item_position] +
                        opt_matrix_current[k_limit - weight_list[item_position], item_position - 1])
        return max_value
    else:
        return opt_matrix_current[k_limit, item_position-1]


for item in range(number_of_items+1):
    for k in range(K+1):
        opt_matrix[k, item] = search_dynamic(weight, value, item, k, opt_matrix)


if __name__ == "__main__":
    print(opt_matrix)
