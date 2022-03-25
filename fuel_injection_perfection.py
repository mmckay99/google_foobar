import itertools


def solution(n):
    """
    # 260 -> 130 -> 65 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1
    >>> solution('260')
    9

    # 261 -> 260 -> 130 -> 65 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1
    >>> solution('261')
    10

    # 15 -> 16 -> 8 -> 4 -> 2 -> 1
    >>> solution('15')
    5

    # 40 -> 20 -> 10 -> 5 -> 4 -> 2 -> 1
    >>> solution('40')
    6

    # 171 -> 172 -> 86 -> 43 -> 44 -> 22 -> 11 -> 12 -> 6 -> 3 -> 2 -> 1
    >>> solution('171')
    11

    >>> solution('278')
    11

    >>> solution('1024')
    10

    >>> solution('18374234484')
    45

    # 309 digits
    >>> solution('366233290575978524550582993069186414224868283843517523061010110915440741548502\
2860158331029780968443604907624171418682681766502589715062379848329738155616223666222477\
0618381506892695801424375091697595578055143991430107532819846749236561764963212095175159\
6264229412096184664734595815300439573064682582671958952')
    1372

    # 310 digits
    >>> solution('256037366842495950619823855882936824359653730274461091366138364341234716118958\
4445195298865186263188470819309088513429290475127160174231086983117921063627289746653430\
3787727649346930313533313690021479368440936861245506455834656044582754971682450644704607\
79205581191254718747967649333688150143164059303197641513')
    1369
    """
    def quantum_pellet_operations(n_as_int):
        if n_as_int == 1:
            return 0
        elif n_as_int == 3:
            # could subtract one then half the number (2 operations)
            return 2
        else:
            # The trick is to consider the binary representation of n. We can rephrase the problem
            # in terms of operations on this binary string. In particular, counting the number of
            # operations to reduce n to 0b1 where an operation is either removing a final "0" (halving),
            # turning the last "1" into a "0" (subtracting 1), or turning a run of "1"s at the end of
            # the binary string into "0"s and then turning the previous character into a "1" (adding 1).
            # An optimal algorithm is described below. We count how many operations are required
            # to "delete" this last run, and then call the algorithm recursively on the number with the
            # resulting binary representation.

            # note that since n >= 4 it must be that there is more than one run
            # to get the last run we reverse n as a binary string and use itertools.groupby
            n_as_binary_reversed = format(n_as_int, 'b')[::-1]
            last_run = next(itertools.groupby(n_as_binary_reversed))
            last_run_char, last_run_count = last_run[0], len(list(last_run[1]))

            if last_run_char == '0':
                # all zeroes so half the number last_run_count times (last_run_count operations)
                return last_run_count + quantum_pellet_operations(n_as_int / (2 ** last_run_count))

            elif last_run_count >= 2:
                # a run of 1s of length two or more, so add one then half the number
                # last_run_count times (1 + last_run_count operations)
                return 1 + last_run_count + quantum_pellet_operations(1 + (n_as_int / (2 ** last_run_count)))

            else:
                # a single run of "1", subtract one and then half (2 operations)
                return 2 + quantum_pellet_operations((n_as_int - 1) / 2)

    return quantum_pellet_operations(int(n))
