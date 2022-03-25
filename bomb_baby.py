def solution(x, y):
    """
    >>> solution('4', '7')
    '4'

    >>> solution('2', '1')
    '1'

    >>> solution('4', '2')
    'impossible'

    >>> solution('374', '7465')
    '57'

    >>> solution('94843', '948583353')
    '10043'

    >>> solution(str(10 ** 51 + 33), str(10 ** 52 + 495))
    '6060606060606060606060606060606060606060606060631'
    """
    x_as_int = long(x)
    y_as_int = long(y)

    # Consider the process of retracing the steps back, with respect
    # to the two possible replication cycles. Let m', f' be the number
    # of current bombs of each type and m, f be the number of
    # bombs of each type before this replication cycle.
    # Either m' = m - f and f' = f, or f' = f - m and m' = m.
    # We can now see that this algorithm is equivalent to the
    # subtraction-based Euclidean algorithm. The total number of
    # replication cycles is the number of loops in this implementation
    # of the Eucidean algorithm minus 1. For efficiency, here I
    # have implemented the division-based algorithm. The number of steps
    # in the original algorithm is the sum of the quotients for each
    # division (in this algorithm).
    replication_cycles = 0
    while y_as_int > 0:
        replication_cycles += (x_as_int // y_as_int)
        x_as_int, y_as_int = y_as_int, x_as_int % y_as_int

    return str(replication_cycles - 1) if x_as_int == 1 else 'impossible'
