

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


def check_valid(opt_matrix_current):
    n, p = opt_matrix_current.shape
    n = n-1
    p = p-1

    if opt_matrix_current[n, p] == opt_matrix_current[n, p-1]:
        return 0
    else:
        return 1


def items_selection(opt_matrix_current, weights):
    ''' '''
    n, p = opt_matrix_current.shape
    n = n-1
    p = p-1
    taken = [0]*(p)
    for column in range(p, 0, -1):
        if opt_matrix_current.shape[0] == 1:
            taken[column-1] = 0
        taken[column-1] = check_valid(opt_matrix_current)
        if taken[column-1] == 1:
            capacity_of_the_selected_item = weights[column]
            # note that the total of zeros is the exact position of the next search
            opt_matrix_current = opt_matrix_current[0:(n - capacity_of_the_selected_item), 0:(column)]
        else:
            opt_matrix_current = opt_matrix_current[:, 0:(column)]
    return taken
