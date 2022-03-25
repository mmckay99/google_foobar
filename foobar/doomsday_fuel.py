"""
s = [[0, 1, 0, 0, 0, 1],
     [4, 0, 0, 3, 2, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]


s = [[0, 1/2, 0, 0, 0, 1/2],
     [4/9, 0, 0, 3/9, 2/9, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]

expected = [0, 3, 2, 9, 14]



s = [[0, 1, 0, 0, 0, 1],
     [4, 0, 0, 3, 2, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]










s1 = [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]]

expected = [7, 6, 8, 21]

s3 = [1 out of tot]
s4 = [3 out of s1]
s5 = [4 out of s1]

so,

s0 = [s0 out of tot]
s1 = [2 out of tot]

so s4 = [3 out of [2 out of tot]]
so s5 = [4 out of [2 out of tot]]

1/3
2/7
8/21







denom = 1

# there are

s = [[0, 0, 0, 0, 0, 0],
     [4, 0, 0, 3, 2, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [9, 9, 9, 9, 9, 9]]


s = [[0, 9, 0, 0, 0, 9],
     [4, 0, 0, 3, 2, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [9, 9, 9, 9, 9, 9]]


incumbent_solution = [0, 1, 0, 0, 0, 1], 2

next = [0, 1, 0, 0, 0, 1]

"""

from fractions import Fraction, gcd

s = [[0, 1, 0, 0, 0, 1],
     [0, 99, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]


def solution(m):
    """
    Doomsday fuel

    >>> s = [\
        [0, 1, 0, 0, 0, 1],\
        [0, 99, 1, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0]]
     >>> solution(s)
     [1, 0, 0, 1, 2]

    >>> s = [\
        [0, 1, 0, 0, 0, 1],\
        [4, 0, 0, 3, 2, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0, 0]]
    >>> solution(s)
    [0, 3, 2, 9, 14]

    >>> s = [\
        [0, 2, 1, 0, 0],\
        [0, 0, 0, 3, 4],\
        [0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0],\
        [0, 0, 0, 0, 0]]
    >>> solution(s)
    [7, 6, 8, 21]
     """
    # construct a new input n where n has an additional start state - reason explained below
    old_states = range(0, len(m))

    # We want to count how many paths end in each state. For a given state sk, this count C[sk] can be
    # expressed as a function of how many paths end in every state (including itself). In fact, this
    # function is a linear expression of the form:
    #   C[sk] = c0 * C[s0] + c1 * C[s1] + ... + cn * C[sn]
    # Initially, we can calculate a set of coefficients for each sk where the coefficient cm is
    # the probability that sm becomes sk, which can be calculated from the input matrix. For example,
    # in the first doctest example,
    #   C[s1] = (1/2) * C[s0] + (99/100) * C[s1] + (0) * C[s2] + ...
    # because state 0 has a 1/2 probability to evolve into state 1 and state 1 has a 99/100 probability
    # to stay in state 1. The coefficients of the equations for each state are stored in path_count_equation_coefficients.
    # The ultimate goal is to express each state path count C[sk] as a function of only one count
    # C[s0]. Assuming that C[s0] = 1 means that the counts for C[s1], ..., C[sn] are thus the probabilities
    # that each terminal state is reached.
    path_count_equation_coefficients = [[Fraction(m[col][row], max(1, sum(m[col])))
                                         for col in old_states] for row in old_states]

    # To make things easier, we add a new state to the scenario
    # where that new state leads to s1 (the old s0) with probability 1.
    new_states = range(0, len(m) + 1)
    for old_state in old_states:
        path_count_equation_coefficients[old_state] = [
            0] + path_count_equation_coefficients[old_state]

    path_count_equation_coefficients = [
        [0] * len(new_states)] + path_count_equation_coefficients
    path_count_equation_coefficients[1][0] = 1

    # It may be that some states, e.g. sk, lead to themselves, so the number of paths that reach them C[sk]
    # is a function of C[sk]. We re-write C[sk] using only the coefficients for other states.
    for state in new_states[1:]:
        old_coefficients = path_count_equation_coefficients[state]
        scale_factor = 1 / (1 - old_coefficients[state])
        new_coefficients = [coefficient * scale_factor for coefficient in old_coefficients]
        new_coefficients[state] = 0
        path_count_equation_coefficients[state] = new_coefficients

    # In this loop the algorithm eliminates each coefficient from the equations corresponding
    # to each state, except s0. To be concrete, for each state_to_eliminate sk where k > 0, it ensures that
    # for each other state sl where l > 0 the equation expressed in the lth row of path_count_equation_coefficients,
    # which expresses C[sl], the coefficient ck for C[sk] is zero. This is accomplished by algebraically
    # substituting in the equation C[sk] into the equation for C[sl]. Since we always tidy up
    # any self-references, the equation C[sk] does not involve C[sk], so the resulting equation for
    # C[sk] does not depend on C[sl].
    for state_to_eliminate in new_states[1:]:
        for state_to_modify in new_states[1:]:
            if state_to_eliminate == state_to_modify:
                continue

            old_coefficients = path_count_equation_coefficients[state_to_modify]

            new_coefficients = []
            for state_to_consider in new_states:
                new_coefficient = 0
                if state_to_consider == state_to_eliminate or state_to_consider == state_to_modify:
                    new_coefficient = 0
                else:
                    # this line can be proven algebraically
                    new_coefficient = old_coefficients[state_to_consider] + (old_coefficients[state_to_eliminate] *
                                                                             path_count_equation_coefficients[state_to_eliminate][state_to_consider])
                new_coefficients += [new_coefficient]

            self_referential_scale_factor = 1 / (1 - (old_coefficients[state_to_eliminate] *
                                                 path_count_equation_coefficients[state_to_eliminate][state_to_modify]))

            # algebraic manipulation to ensure no self reference, i.e. that C[sk] does not depend on C[sk]
            new_coefficients = [coefficient *
                                self_referential_scale_factor for coefficient in new_coefficients]
            new_coefficients[state_to_modify] = 0

            path_count_equation_coefficients[state_to_modify] = new_coefficients

    # we must return the 'terminal' state coefficients in order - don't forget that we added the new state
    terminal_state_coefficients = [path_count_equation_coefficients[old_state + 1][0]
                                   for old_state in range(0, len(m)) if sum(m[old_state]) == 0]

    final_denominator = int(1 / reduce(gcd, terminal_state_coefficients))

    final_numerators = map(
        int, [coefficient * final_denominator for coefficient in terminal_state_coefficients])

    return final_numerators + [final_denominator]


print(solution(s))
