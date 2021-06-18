def to_tuple(t):
    return tuple(map(to_tuple, t)) if isinstance(t, (tuple, list)) else t


def prettyList(board):
    for row in board:
        for x in row:
            print(str(x).ljust(12), end=" | ")
        print()
    print()
