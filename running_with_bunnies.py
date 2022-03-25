import itertools


def all_pairs_shortest_paths(weights):
    """
    Use the Floyd-Warshall algorithm to construct a matrix of all-pairs shortest
    path costs, given the edge-weight matrix of a complete weighted graph.

    >>> weights = [\
        [0, 4, 100, 100, 100, 100, 10, 4],\
        [100, 0, 9, 100, 100, 7, 8, 1],\
        [100, 100, 0, 100, 10, 100, 100, 100],\
        [100, 100, 100, 0, 100, 100, 100, 100],\
        [100, 100, 6, 5, 0, 5, 100, 100],\
        [100, 100, 100, 100, 10, 0, 100, 100],\
        [100, 6, 100, 100, 100, 7, 0, 100],\
        [100, 100, 5, 100, 100, 100, 100, 0],\
        ]
    >>> expected_costs = all_pairs_shortest_paths(weights)
    >>> expected_costs == [\
        [0, 4, 9, 24, 19, 11, 10, 4],\
        [100, 0, 6, 21, 16, 7, 8, 1],\
        [100, 100, 0, 15, 10, 15, 100, 100],\
        [100, 100, 100, 0, 100, 100, 100, 100],\
        [100, 100, 6, 5, 0, 5, 100, 100],\
        [100, 100, 16, 15, 10, 0, 100, 100],\
        [100, 6, 12, 22, 17, 7, 0, 7],\
        [100, 100, 5, 20, 15, 20, 100, 0],\
        ]
    True
    """
    vertices = range(len(weights))

    for (k, i, j) in itertools.product(vertices, repeat=3):
        if weights[i][j] > weights[i][k] + weights[k][j]:
            weights[i][j] = weights[i][k] + weights[k][j]

    return weights


def shortest_paths_costs_contain_negative_cycle(costs_matrix):
    return any(costs_matrix[vertex][vertex] < 0 for vertex in range(len(costs_matrix)))


def solution(times, time_limit):
    """
    This problem is a variation of the Travelling Salesman Problem (TSP) in
    which cities may be revisited, except the tour begins and ends at specific vertices.
    This variation can be reduced in polynomial time to Metric TSP, showing that
    the problem of finding an bunny-saving-route within the time limit saving
    a maximum number of bunnies is strongly NP-hard (for an arbitrary number of bunnies).

    The polynomial-time reduction, which is implemented here, involves constructing a graph
    on the same set of locations except the time between each pair of locations is the
    time taken on the shortest path between those locations in the original hallway. 
    This reduction is used in order to reduce the bunny problem to one in which each
    bunny is visited at most once. This means that the search space in the reduced problem
    comprises n! possible routes (since no bunnies are revisited), where n is the number
    of bunnies.

    Since n <= 5, n! <= 120 so a brute-force search of solutions in the reduced problem
    may be acceptable. For larger n, one possibility would be to use a Metric TSP
    approximation algorithm, e.g. Christofides' algorithm, to place a lower bound on
    possible route times.

    >>> times_1 = [\
    [0, 2, 1, 1, -1],\
    [8, 0, 1, 1, -1],\
    [8, 2, 0, 1, -1],\
    [8, 2, 1, 0, -1],\
    [9, 3, 2, 2, 0]]

    >>> solution(times_1, 1)
    [1, 2]

    >>> times_2 = [\
    [0, 8, 8, 8, 1],\
    [8, 0, 8, 8, 1],\
    [8, 8, 0, 8, 8],\
    [8, 8, 8, 0, 8],\
    [9, 1, 2, 2, 0]]

    Can do 0 -> 4 -> 2 -> 3 -> 1 -> 4 (weight 1 + 2 + 8 + 8 + 1 = 20).
    >>> solution(times_2, 20)
    [0, 1, 2]
    >>> solution(times_2, 19)
    [0, 1]

    >>> times_3 = [\
    [0, 997, 96, 473, 97, 781, 536],\
     [67, 0, 740, 569, 785, 625, 819],\
     [525, 928, 0, 957, 786, 288, 734],\
     [635, 609, 779, 0, 747, 39, 640],\
     [148, 546, 820, 761, 0, 738, 486],\
     [525, 0, 740, 810, 53, 0, 708],\
     [841, 300, 604, 604, 624, 628, 0]]

    >>> solution(times_3, 999)
    [0, 1, 4]

    >>> times_4 = [\
    [0, 8, 8, 8, 8],\
    [8, 0, 8, 8, 1],\
    [8, 8, 0, 8, 8],\
    [8, 8, 8, 0, 8],\
    [9, 1, 2, 2, 0]]


    >>> solution(times_4, 1)
    []
    """
    bunny_locations = list(range(1, len(times) - 1))
    shortest_paths_times = all_pairs_shortest_paths(times)

    if shortest_paths_costs_contain_negative_cycle(shortest_paths_times):
        # go backwards in time arbitrarily far and save all bunnies
        return list(range(0, len(times) - 2))

    for bunny_route_length in range(len(bunny_locations), 0, -1):
        for bunny_route_in_reduced_graph in itertools.permutations(bunny_locations, bunny_route_length):
            full_route_in_reduced_graph = [0] + \
                list(bunny_route_in_reduced_graph) + [len(times) - 1]

            # calculate the full route time, including possible revisits, in the original graph
            full_route_time = 0
            for path_step in range(1, bunny_route_length + 2):
                from_location = full_route_in_reduced_graph[path_step - 1]
                to_location = full_route_in_reduced_graph[path_step]
                full_route_time += shortest_paths_times[from_location][to_location]

            if full_route_time <= time_limit:
                # This path is acceptable and uses the lowest bunny indices for this path
                # length (since we consider bunny paths in permutation order). Since we
                # started with the longest paths this is the best path possible.
                return sorted([location - 1 for location in bunny_route_in_reduced_graph])

    return []
