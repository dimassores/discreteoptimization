import dynamic_config as data
import numpy as np

value = data.value
weight = data.weight
K = data.K
number_of_items = data.number_of_items

opt_matrix = np.empty([K+1, number_of_items+1])


def search_dynamic(weight_list, value_list, item_position, k_limit, opt_matrix_current):
    ''' search_dynamic '''
    if item_position == 0:
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


def check_valid(opt_matrix_current):
    n, p = opt_matrix_current.shape
    n = n-1
    p = p-1
    if opt_matrix_current[n, p] == opt_matrix_current[n, p-1]:
        return 0
    else:
        return 1


def items_selection(opt_matrix_current):
    ''' '''
    n, p = opt_matrix_current.shape
    n = n-1
    p = p-1
    taken = [0]*(p)
    for column in range(p, 0, -1):
        taken[column-1] = check_valid(opt_matrix_current)
        if taken[column-1] == 1:
            column_next = opt_matrix_current[:, column-1]
            is_zero_total = sum(column_next == 0)
            # note that the total of zeros is the exact position of the next search
            opt_matrix_current = opt_matrix_current[0:(is_zero_total+1), 0:(column)]
        else:
            opt_matrix_current = opt_matrix_current[:, 0:(column)]
    return taken


if __name__ == "__main__":

    print(opt_matrix)
    print(items_selection(opt_matrix))
