from typing import List, NamedTuple


class Bag(NamedTuple):
    """ 
	"""

    value: int
    items: List[Item]


def remove_unsuitable_candidates(capacity: int, candidates: List[Item]):
    """ 
	"""
    return [item for item in candidates if item.weight <= capacity]


def optimize_bag(capacity: int, items: List[Item]):
    """
	"""

    return search_result(
        capacity,
        sorted(items, key=lambda item: item.value / item.weight, reverse=True),
        [],
        Bag(0, []),
    )


def search_result(
    capacity: int, candidates: List[Item], picked: List[Item], best_result: Bag
):
    """ 
	"""

    candidates = remove_unsuitable_candidates(capacity, candidates)
    if not candidates:
        current_value = sum(item.value for item in picked)
        return (
            best_result
            if best_result.value > current_value
            else Bag(current_value, picked)
        )

    optmist_estimate = sum(item.value for item in candidates + picked)
    if optmist_estimate < best_result.value:
        return best_result

    next_candidate = candidates[0]

    # Inclusive branch
    best_result = search_result(
        capacity - next_candidate.weight,
        candidates[1:],
        picked + [next_candidate],
        best_result,
    )

    # Exclusive branch
    best_result = search_result(capacity, candidates[1:], picked, best_result,)

    return best_result
