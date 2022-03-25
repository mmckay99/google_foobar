import itertools


class Forest:
    def __init__(self):
        self.children_dict = {}
        self._elements_in_forest = set()

    def elements_in_forest(self):
        return self._elements_in_forest

    def contains(self, element):
        return element in self._elements_in_forest

    def add(self, element, parent=None):
        self._elements_in_forest.add(element)

        self.children_dict[element] = set()
        if parent is not None:
            self.children_dict[parent].add(element)

    def parent_of(self, element):
        """
        returns None if element is a root node

        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.parent_of(2)
        1
        """
        assert element in self._elements_in_forest, "element " + \
            str(element) + " not in this forest"

        for possible_parent in self._elements_in_forest:
            if element in self.children_dict[possible_parent]:
                return possible_parent
        else:
            return None

    def path_to_root(self, element):
        """
        path includes start and end

        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.add(3, 2)
        >>> forest.add(4, 3)
        >>> forest.add(5, 4)

        >>> forest.path_to_root(5)
        [5, 4, 3, 2, 1]

        >>> forest.path_to_root(2)
        [2, 1]

        >>> forest.path_to_root(1)
        [1]
        """
        return self.path_to_ancestor(element, None)

    def distance_to_root(self, element):
        """
        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.add(3, 2)
        >>> forest.add(4, 3)
        >>> forest.add(5, 4)
        >>> forest.distance_to_root(5)
        4

        >>> forest.distance_to_root(1)
        0
        """
        return len(self.path_to_root(element)) - 1

    def path_to_ancestor(self, element, ancestor):
        """
        path includes start and end
        if ancestor is not in the path then the path is to the root

        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.add(3, 2)
        >>> forest.add(4, 3)
        >>> forest.add(5, 4)
        >>> forest.path_to_ancestor(5, 3)
        [5, 4, 3]

        >>> forest.path_to_ancestor(5, 5)
        [5]

        >>> forest.path_to_ancestor(5, 9)
        [5, 4, 3, 2, 1]
        """
        parent = self.parent_of(element)

        if element == ancestor or parent is None:
            return [element]
        else:
            return [element] + self.path_to_ancestor(parent, ancestor)

    def root_of(self, element):
        """
        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.add(3, 2)
        >>> forest.root_of(3)
        1
        """
        return self.path_to_root(element)[-1]

    def path(self, from_element, to_element):
        """
        includes from_element and to_element in the path

        >>> forest = Forest()
        >>> forest.add(1)
        >>> forest.add(2, 1)
        >>> forest.add(3, 2)
        >>> forest.add(4, 3)
        >>> forest.add(5, 4)
        >>> forest.add(6, 5)
        >>> forest.add(7, 4)
        >>> forest.add(8, 7)
        >>> forest.add(9, 8)

        >>> forest.path(9, 6)
        [9, 8, 7, 4, 5, 6]

        >>> forest.path(2, 9)
        [2, 3, 4, 7, 8, 9]
        """
        if from_element == to_element:
            return [from_element]
        else:
            ancestors_of_from_element = self.path_to_root(from_element)
            ancestors_of_to_element = self.path_to_root(to_element)

            for ancestor_of_from_element in ancestors_of_from_element:
                if ancestor_of_from_element in ancestors_of_to_element:
                    lowest_common_ancestor = ancestor_of_from_element

                    return self.path_to_ancestor(from_element, lowest_common_ancestor)[:-1]\
                        + self.path_to_ancestor(to_element, lowest_common_ancestor)[::-1]
            else:
                assert "error in Forest.path, elements " + \
                    str(from_element) + ", " + str(to_element) + " have no common ancestor"


def will_thumb_wrestle_forever(a_bananas, b_bananas):
    """
    >>> will_thumb_wrestle_forever(1, 21)
    True

    >>> will_thumb_wrestle_forever(1, 3)
    False

    >>> will_thumb_wrestle_forever(1, 7)
    False

    >>> will_thumb_wrestle_forever(11, 693)
    False

    >>> will_thumb_wrestle_forever(40, 80)
    True

    >>> will_thumb_wrestle_forever(9, 18)
    True

    >>> will_thumb_wrestle_forever(13, 15)
    True

    Suppose the sequence terminates after one step. Then the only possibility is that
    the second-to-last pair was (a, 3a) for some integer a >= 1. Thus, if
    (a, b) is the second-to-last pair then the sequence terminates if and
    only if (b / a) == 3. Similarly, if the sequence has length three or
    more, then it terminates if and only if (b / a) == 7, since this happens
    if and only if the second-to-last pair satisfies (b / a) == 3. This is
    true since (a, 7a) +> (2a, 6a) == ((2a), 3(2a)). More generally,
    a sequence terminates with length k if and only if
    (b / a) == 2^k - 1.
    """
    smaller_or_equal, larger = (
        a_bananas, b_bananas) if a_bananas <= b_bananas else (b_bananas, a_bananas)

    if larger % smaller_or_equal != 0:
        return True
    else:
        quotient = larger // smaller_or_equal
        return (quotient + 1) & quotient != 0


def contract_blossom(B, G, M):
    """
    >>> G1 = [\
        [0, 1, 0, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0, 0],\
        [0, 0, 0, 1, 0, 1, 0, 0, 1],\
        [0, 0, 0, 0, 1, 0, 1, 0, 0],\
        [0, 0, 0, 0, 0, 1, 0, 1, 0],\
        [0, 0, 0, 0, 0, 0, 1, 0, 1],\
        [0, 0, 0, 0, 1, 0, 0, 1, 0],\
    ]
    >>> B1 = [4, 5, 6, 7, 8]
    >>> M1 = {1: 2, 2: 1, 3: 4, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7}
    >>> Gp1 = [\
        [0, 1, 0, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0, 0],\
        [0, 0, 0, 1, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 0, 0],\
    ]
    >>> Mp1 = {1: 2, 2: 1, 3: 4, 4: 3}

    >>> contract_blossom(B1, G1, M1) == (Gp1, Mp1)
    True
    """
    V = list(range(len(G)))
    Gp = [[G[u][v] for u in V] for v in V]
    # the first vertex in B becomes the supervertex, the others become just isolated vertices
    supervertex = B[0]
    non_supervertices = B[1:]

    # make the supervertex adjacent to all vertices that are adjacent to any in the blossom
    for non_supervertex in non_supervertices:
        for possible_neighbour in V:
            if G[non_supervertex][possible_neighbour] and possible_neighbour != supervertex:
                Gp[supervertex][possible_neighbour] = 1
                Gp[possible_neighbour][supervertex] = 1

    # make the non-supervertices isolated in Gp (will be ignored)
    for non_supervertex in non_supervertices:
        for possible_neighbour in V:
            Gp[possible_neighbour][non_supervertex] = 0
            Gp[non_supervertex][possible_neighbour] = 0

    # reconstruct the matching M
    Mp = {u: M[u] for u in M if u not in non_supervertices and M[u] not in non_supervertices}

    return Gp, Mp


def lift_augmenting_path(Pp, B, G):
    """
    returns a new path P in G where if Pp traverses
    the blossom 'supervertex' P traverses correctly around the blossom

    >>> Pp1 = [0, 1, 2, 3, 6, 7, 8]
    >>> B1 = [3, 4, 5, 10, 9]
    >>> G1 = [\
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],\
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],\
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],\
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],\
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],\
    ]
    >>> P1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    >>> lift_augmenting_path(Pp1, B1, G1) == P1
    True

    >>> Pp2 = [0, 1, 2, 3, 6, 7, 8]
    >>> B2 = [3, 4, 5, 10, 9]
    >>> G2 = [\
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],\
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],\
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],\
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],\
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],\
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],\
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0],\
    ]
    >>> P2 = [0, 1, 2, 3, 9, 10, 6, 7, 8]
    >>> lift_augmenting_path(Pp2, B2, G2) == P2
    True

    >>> Pp3 = [0, 1]
    >>> B3 = [1, 2, 3, 4, 5, 6, 7]
    >>> G3 = [\
        [0, 1, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0],\
        [0, 0, 0, 1, 0, 1, 0, 0],\
        [0, 0, 0, 0, 1, 0, 1, 0],\
        [0, 0, 0, 0, 0, 1, 0, 1],\
        [0, 0, 0, 0, 0, 0, 1, 0],\
    ]
    >>> P3 = [0, 1, 2, 3, 4, 5, 6, 7]
    >>> lift_augmenting_path(Pp3, B3, G3) == P3
    True

    in this test case, there is
    no alternating path in Gp
    >>> Pp4 = []
    >>> B4 = [1, 2, 3, 4, 5, 6, 7]
    >>> G4 = []
    >>> P4 = []
    >>> lift_augmenting_path(Pp4, B4, G4) == P4
    True

    in this test case, there is a blossom to expand but
    the alternating path does not intersect it
    >>> Pp5 = [1, 2, 3]
    >>> B5 = [4, 5, 6, 7, 8]
    >>> G5 = [\
        [0, 1, 0, 0, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0, 0, 0],\
        [0, 0, 1, 0, 1, 0, 0, 0],\
        [0, 0, 0, 1, 0, 1, 0, 0],\
        [0, 0, 0, 0, 1, 0, 1, 0],\
        [0, 0, 0, 0, 0, 1, 0, 1],\
        [0, 0, 0, 0, 0, 0, 1, 0],\
    ]
    >>> P5 = [1, 2, 3]
    >>> lift_augmenting_path(Pp5, B5, G5) == P5
    True
    """
    # find the "root" vertex (where Pp intersects the blossom)
    blossom_index_in_Pp = 0
    for path_vertex in Pp:
        if path_vertex in B:
            break
        else:
            blossom_index_in_Pp += 1
    else:
        # the path Pp does not intersects the blossom - no need to modify it
        return Pp

    root_of_blossom = Pp[blossom_index_in_Pp]

    # find the "exit" vertex in the blossom
    exit_node = None
    if blossom_index_in_Pp == len(Pp) - 1:
        # if the blossom is at the end of the path Pp, just "exit" at the end of the blossom
        exit_node = B[-1]
    else:
        first_vertex_in_Pp_not_in_blossom = Pp[blossom_index_in_Pp + 1]
        for possible_exit_node in B:
            if G[possible_exit_node][first_vertex_in_Pp_not_in_blossom]:
                exit_node = possible_exit_node
                break

    # Now we must calculate which way around the blossom to travel. we want to identify
    # an even number of edges in the blossom from the root to the exit node to ensure
    # the alternating path has even length
    index_of_exit_node = B.index(exit_node)
    index_of_root_node = B.index(root_of_blossom)
    distance_in_forward_direction = index_of_exit_node - index_of_root_node

    path_through_blossom = []
    if distance_in_forward_direction % 2 == 0:
        # go "forwards" through the blossom
        path_through_blossom = B[index_of_root_node: index_of_exit_node + 1]
    else:
        # go "backwards" through the blossom
        path_through_blossom = B[index_of_root_node: 0: -1] + \
            [B[0]] + B[-1: index_of_exit_node: -1] + [B[index_of_exit_node]]

    return Pp[0: blossom_index_in_Pp] + path_through_blossom + Pp[blossom_index_in_Pp + 1:]


def find_augmenting_path(G, M):
    """
    The code is based on the pseudocode from
    https://en.wikipedia.org/wiki/Blossom_algorithm#Finding_an_augmenting_path .
    Variable names and code structure match the pseudocode where possible (G' => Gp).

    >>> G1 = [\
        [0, 1, 0, 0, 0, 0],\
        [1, 0, 1, 0, 0, 0],\
        [0, 1, 0, 1, 0, 0],\
        [0, 0, 1, 0, 1, 0],\
        [0, 0, 0, 1, 0, 1],\
        [0, 0, 0, 0, 1, 0]\
    ]
    >>> M1 = {1: 2, 2: 1, 3: 4, 4: 3}
    >>> P1 = [0, 1, 2, 3, 4, 5]
    >>> find_augmenting_path(G1, M1) == P1
    True

    Test case 2 is the example containing 19 vertices in
    https://en.wikipedia.org/wiki/Blossom_algorithm#Examples
    and requires the contraction of a blossom.

    >>> G2 = [[0 for _ in range(20)] for _ in range(20)]
    >>> for (u, v) in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),\
               (5, 6), (4, 7), (7, 8), (4, 9), (9, 10),\
               (10, 11), (11, 12), (12, 13), (13, 14), (12, 15),\
               (15, 16), (11, 17), (17, 18), (18, 19), (19, 12)]:\
            G2[u][v], G2[v][u] = 1, 1

    >>> M2 = {0: 1, 1: 0, 3: 4, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7, 9: 10, 10: 9,\
      11: 17, 17: 11, 18: 19, 19: 18, 12: 13, 13: 12, 15: 16, 16: 15}
    >>> P2 = [2, 3, 4, 9, 10, 11, 17, 18, 19, 12, 13, 14]
    >>> find_augmenting_path(G2, M2) == P2
    True
    """
    V = list(range(len(G)))
    F = Forest()

    # unmark all vertices and edges in the graph
    unmarked_vertices = set(V)
    unmarked_edges = set()
    for (v, w) in itertools.combinations(V, 2):
        if G[v][w]:
            unmarked_edges.add(frozenset({v, w}))

    # mark all edges in the matching (also calculate exposed vertices while we are here)
    exposed_vertices = set(V)
    for (v, w) in M.items():
        unmarked_edges.discard(frozenset({v, w}))
        exposed_vertices.discard(v)
        exposed_vertices.discard(w)

    # for each exposed vertex v, create a singleton tree {v} and add it to F
    for v in exposed_vertices:
        F.add(v, None)

    # while there is an unmarked vertex v in F with distance(v, root(v)) even do
    while True:
        v = next((u for u in F.elements_in_forest() if F.distance_to_root(u) %
                  2 == 0 and u in unmarked_vertices), None)
        if v is None:
            break

        # while there exists an unmarked edge e = { v, w } do
        while True:
            w = next((w for w in V if frozenset({v, w}) in unmarked_edges), None)
            if w is None:
                break

            if not F.contains(w):
                # w is matched, so add e and w's matched edge to F
                x = M[w]
                F.add(w, v)
                F.add(x, w)
            else:
                if F.distance_to_root(w) % 2 == 1:
                    # do nothing
                    pass
                else:
                    v_root = F.root_of(v)
                    w_root = F.root_of(w)
                    if F.root_of(v) != F.root_of(w):
                        # report an augmenting path in F \cup { e } from root of v to v
                        # then to w then up to w's root
                        return F.path(v_root, v) + F.path(w, w_root)
                    else:
                        # contract a blossom in the graph and recurse
                        B = F.path(v, w)
                        Gp, Mp = contract_blossom(B, G, M)
                        Pp = find_augmenting_path(Gp, Mp)
                        P = lift_augmenting_path(Pp, B, G)

                        return P

            # mark e = { v, w }
            unmarked_edges.remove(frozenset({v, w}))
        # mark v
        unmarked_vertices.remove(v)
    return []


def augment_matching(M, P):
    """
    >>> test_M = {0: None, 1: 2, 2: 1, 3: 4, 4: 3, 5: None, 6: 7, 7: 6, 8: 9, 9: 8}
    >>> test_P = [0, 1, 2, 3, 4, 5]
    >>> expected_augmented_M = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8}
    >>> actual_augmented_M = augment_matching(test_M, test_P)
    >>> actual_augmented_M == expected_augmented_M
    True
    """
    Mp = dict(M)
    for v_index in range(len(P)):
        # for odd numbered vertices
        if v_index % 2 == 1:
            if v_index < len(P) - 1:
                # remove the old edge (goes forwards)
                Mp.pop(P[v_index + 1])

            # add the new edge (goes backwards)
            Mp[P[v_index - 1]] = P[v_index]
            Mp[P[v_index]] = P[v_index - 1]

    return Mp


def find_maximum_matching(G):
    """
    Pseudocode used from https://en.wikipedia.org/wiki/Blossom_algorithm .
    G is represented using a 0/1 adjacency matrix.
    The return value is a dictionary M in which M[a] == b iff a is matched
    to b (unmatched vertices do not appear).
    """
    def blossom_algorithm(G, M):
        P = find_augmenting_path(G, M)

        if len(P) == 0:
            return M
        else:
            M_augmented_along_P = augment_matching(M, P)
            return blossom_algorithm(G, M_augmented_along_P)

    initial_matching = dict()
    return blossom_algorithm(G, initial_matching)


def solution(banana_list):
    """
    Returns the fewest possible number of trainers left to watch the workers after
    pairing the trainers up. The optimal strategy is to find a maximum matching in
    the graph constructed with the vertices as the set of trainers and an edge
    between two trainers if they will play forever.

    >>> solution([1, 7, 3, 21, 13, 19])
    0

    >>> solution([1, 1])
    2

    >>> solution([1, 1, 31])
    3

    >>> solution([10, 10, 310, 10, 10, 630, 10, 10, 10737418230])
    7
    """
    trainers = range(0, len(banana_list))
    trainers_graph = [[0 for _ in trainers] for _ in trainers]

    # construct the trainers graph as an 0/1 adjacency matrix
    for a_trainer, b_trainer in itertools.combinations(trainers, 2):
        a_b_will_thumb_wrestle_forever = will_thumb_wrestle_forever(
            banana_list[a_trainer], banana_list[b_trainer])

        trainers_graph[a_trainer][b_trainer] = int(a_b_will_thumb_wrestle_forever)
        trainers_graph[b_trainer][a_trainer] = int(a_b_will_thumb_wrestle_forever)

    maximum_matching_of_trainers = find_maximum_matching(trainers_graph)

    unmatched_trainers = [
        trainer for trainer in trainers if trainer not in maximum_matching_of_trainers]

    return len(unmatched_trainers)


# print solution([1, 1])
# print(solution([1, 1, 31, 1, 1, 63, 1, 1, 15]))
# while True:
#     xs = [random.randint(1, 1073741823) for _ in range(50)]
#     sol = solution(xs)
#     if sol > 2:
#         print(xs)
#         break
#     else:
#         print(".", flush=True, end='')


xs = [203161946, 46012376, 454235495, 9872262, 860780278, 197464525, 643057098, 662264437, 423982331, 144996911, 934830905, 701846349, 860387750, 867507160, 337490049, 476779286, 623834766, 156829067, 305062633, 1039106442, 1023704758, 911993184, 14603919, 721338620, 314214148, 457984596, 1024582044, 969117571, 985158986, 874241179, 723909975, 1071523793, 180609666, 664291922, 355526708, 156039954, 317160798, 139317759, 687761421, 62136336, 91845915, 604109522, 981873294, 964072635, 37731476, 760987531, 559483713, 4883062, 241263168,
      382575783, 972363985, 551378921, 538959284, 991630244, 737730354, 426932060, 811438376, 861701019, 859358096, 777388852, 771562389, 111173427, 453535601, 718472425, 198119448, 88269878, 746436447, 30549235, 64336272, 104197032, 594172351, 398445185, 696646185, 108333305, 325434458, 995753609, 530973358, 939619701, 541487198, 390691903, 38014202, 750015501, 735627533, 427261824, 102619031, 883292254, 719791379, 819780009, 586982754, 238620470, 415443497, 34247781, 143369387, 671543525, 700277994, 969504215, 1035429122, 115483185, 421991849]
print xs
print solution(xs)
