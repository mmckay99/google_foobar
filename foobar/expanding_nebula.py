
def candidate_is_complete_solution(candidate):
    """
    a candidate partial solution is complete when the cursor moves beyond the boundary

    >>> candidate_is_complete_solution((0b0, 16, (4, 4)))
    True
    """
    cursor_position, (width, height) = candidate[1:3]
    return cursor_position >= width * height


def extend_candidate(candidate, fix_cell_value):
    """
    >>> c = (0b000000000, 2, (3, 3))
    >>> extend_candidate(c, 1) == (0b000000100, 3, (3, 3))
    True
    """
    cell_data, cursor_position, size = candidate
    # set the bit at the cursor to fix_cell_value
    new_cell_data = cell_data ^ (-fix_cell_value) & (1 << cursor_position)
    return (new_cell_data, cursor_position + 1, size)


def compute_feasible_extensions(candidate, g):
    """
    In the test case below, the candidate partial solution has fixed
    cells 0 to 12 (counting right to left, bottom to top). Consider
    cell 13 in the candidate (at x=4, y=5 from the top-left).
    Since the three cells at positions 12, 7, 6 (to the right of,
    below, and below-and-to-the-right of cell 13) are all fixed to 0,
    and the 'indicator' cell in g is True (last cell in the 
    second-to-last row, from the top-left), by the rules of nebula
    expansion the only feasible extension of this candidate has cell
    13 set to 1.

    >>> c = (0b00000100011101, 13, (6, 9))
    >>> g = [[True, True, True, True, True],\
        [False, False, True, False, False],\
        [True, True, True, True, True],\
        [False, False, False, False, False],\
        [False, False, False, False, False],\
        [True, False, False, False, True],\
        [True, True, True, True, True],\
        [True, False, False, False, True]]
    >>> compute_feasible_extensions(c, g) == [(0b10000100011101, 14, (6, 9))]
    True
    """
    cell_data, cursor, (width, height) = candidate

    indicator = -1

    cell_below = cell_data >> (cursor - width) & 1 if (cursor >= width) else -1
    cell_right = cell_data >> (cursor - 1) & 1 if (cursor % width > 0) else -1

    cell_below_right = -1
    if cursor >= width and cursor % width != 0:
        indicator_x_in_g = (width - 1) - (cursor % width)
        indicator_y_in_g = (height - 1) - (cursor - (cursor % width)) // width

        indicator = int(g[indicator_y_in_g][indicator_x_in_g])
        cell_below_right = cell_data >> (cursor - width - 1) & 1

    neighbours_below_right = [cell_below, cell_below_right, cell_right]

    live = neighbours_below_right.count(1)
    dead = neighbours_below_right.count(0)

    # the rules of nebula expansion
    possible_cell_values = [0, 1]
    if indicator == 0:
        if dead == 2 and live == 1:
            possible_cell_values = [1]
        elif dead == 3:
            possible_cell_values = [0]
    elif indicator == 1:
        if live > 1:
            # infeasible
            possible_cell_values = []
        elif live == 1:
            possible_cell_values = [0]
        elif dead == 3:
            possible_cell_values = [1]

    return [extend_candidate(candidate, fix_cell_value) for fix_cell_value in possible_cell_values]


def calculate_exposed_part(candidate):
    """
    the "exposed" cells are the only fixed cells that are
    needed to determine if this partial solution can be completed
    (i.e. only the last (width + 1) cells that are fixed)

    >>> candidate = (0b0000001100101010, 10, (4, 4))
    >>> expected_contents = (10, 0b1100111111)
    >>> actual_contents = calculate_exposed_part(candidate)
    >>> actual_contents == expected_contents
    True
    """
    cell_data, cursor, (width, _) = candidate
    # set the last cursor - width cells, if they exist, to 1
    return cursor, cell_data | (1 << max(0, cursor - width - 1)) - 1


def solution(g):
    """
    This function implements a backtracking search of all possible
    nebulas in order to count the number of possible predecessors.

    A caching strategy is used to take advantage of the following property: for
    any two (partial) candidate solutions, if they differ only in cells that are
    before the last (width + 1) fixed cells, then the number of complete solutions
    descendant of both is the same. We refer to the last (width + 1) fixed cells
    as the "exposed part" of this candidate.

    >>> g1 = [[True, False, True], [False, True, False], [True, False, True]]
    >>> solution(g1)
    4

    >>> g2 = [[True, False, True, False, False, True, True, True],\
        [True, False, True, False, False, False, True, False],\
        [True, True, True, False, False, False, True, False],\
        [True, False, True, False, False, False, True, False],\
        [True, False, True, False, False, True, True, True]]
    >>> solution(g2)
    254

    >>> g3_encoded = 0x2a9047b452202091024a90660210f1aaa72801118021c950220c
    >>> g3 = [[g3_encoded >> 50 * y + x & 1 for x in range(50)] for y in range(9)]
    >>> solution(g3)
    403938963384122994507501793513203613645097539241313772075389745381953763
    """
    # the caching strategy is most effective if
    # there are more rows than columns
    if len(g[0]) >= len(g):
        g = [[g[x][y] for x in range(len(g))] for y in range(len(g[0]))]

    initial_candidate = (0, 0, (len(g[0]) + 1, len(g) + 1))
    candidate_stack = [(0, initial_candidate)]

    candidate_exposed_cache = dict()
    number_of_descendant_solutions = dict()
    visited_parents = set()

    while len(candidate_stack) > 0:
        (node_id, candidate) = candidate_stack[-1]

        exposed_part = calculate_exposed_part(candidate)

        if node_id in visited_parents:
            # second visit to this partial solution - compute total from children
            complete_solutions_of_children =\
                number_of_descendant_solutions.get(2 * node_id + 1, 0)\
                + number_of_descendant_solutions.get(2 * node_id + 2, 0)

            number_of_descendant_solutions[node_id] = complete_solutions_of_children
            candidate_exposed_cache[exposed_part] = complete_solutions_of_children
            candidate_stack.pop()
        elif exposed_part in candidate_exposed_cache:
            # cache hit (on this first visit)
            number_of_descendant_solutions[node_id] = candidate_exposed_cache[exposed_part]
            candidate_stack.pop()
        elif candidate_is_complete_solution(candidate):
            number_of_descendant_solutions[node_id] = 1
            candidate_stack.pop()
        else:
            feasible_extensions = compute_feasible_extensions(candidate, g)

            for (index, extension) in enumerate(feasible_extensions):
                extension_id = 2 * node_id + index + 1
                candidate_stack += [(extension_id, extension)]

            visited_parents.add(node_id)

    return number_of_descendant_solutions[0]


def __main__():
    # expect 4
    test_g1 = [[True, False, True], [False, True, False], [True, False, True]]

    # expect 254
    test_g2 = [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True,
                                                                                                                            False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]
    test_g3 = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [
        True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]

    test_g2_transposed = [[True, True, True, True, True], [False, False, True, False, False], [True, True, True, True, True], [False, False, False, False, False], [
        False, False, False, False, False], [True, False, False, False, True], [True, True, True, True, True], [True, False, False, False, True]]

    w = 50
    h = 9

    # exceeds default maximum recursion depth
    test_g4 = [[True, False, True, False, True, False, True, False, False, True, False, False, False, False, False, True, False, False, False, True, True, True, True, False, True, True, False, True, False, False, False, True, False, True, False, False, True, False, False, False, True, False, False, False, False, False, False, False, True, False], [False, False, False, False, True, False, False, True, False, False, False, True, False, False, False, False, False, False, True, False, False, True, False, False, True, False, True, False, True, False, False, True, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False], [True, False, False, False, False, True, False, False, False, False, True, True, True, True, False, False, False, True, True, False, True, False, True, False, True, False, True, False, True, False, False, True, True, True, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, True], [False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, False, True, False, False, True, False, True, False, True, False, False, False, False, False, False, True, False, False, False, True, False, False, False], [False, False, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, True, False,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 False, False, False, False, False, True, False, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True], [False, True, True, False, True, True, False, False, True, False, False, False, False, True, False, False, True, False, False, True, False, True, False, False, False, False, True, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, True, True, False, False, False, True], [False, False, False, False, False, False, False, False, True, False, False, True, False, False, False, True, False, False, True, False, False, True, False, False, True, False, False, True, False, False, True, True, False, True, True, False, False, True, False, False, False, True, False, True, False, False, False, False, True, False], [True, False, False, False, False, False, True, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, True, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True], [False, False, False, False, False, True, False, True, False, False, False, True, True, False, False, True, False, False, False, False, False, True, True, True, False, False, True, False, False, False, False, True, False, True, False, False, False, True, True, False, False, False, True, False, False, False, False, True, True, False]]
    test_gi = test_g4

    # test_gi = [[random.choice([True, False, False]) for _ in range(w)] for _ in range(h)]

    # print(f"{test_gi=}")
    # print(solution(test_gi))


__main__()
