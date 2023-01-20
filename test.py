start, end = [3, 3, 1], [0, 0, 0]


def do_action(state, action):
    if state[2] == 1:
        return [state[i] - action[i] for i in range(3)]
    else:
        return [state[i] + action[i] for i in range(3)]


def is_legal(state):
    if 0 <= state[0] <= 3 and 0 <= state[1] <= 3:
        return True
    else:
        return False


def is_bank_safe(bank):
    if bank[1] > bank[0] and bank[0] != 0:
        return False
    else:
        return True


def is_state_safe(state):
    other_bank = [start[i]-state[i] for i in range(3)]
    if is_bank_safe(state) and is_bank_safe(other_bank):
        return True
    else:
        return False

def next_possible_actions(state):
    actions = [[1, 0, 1], [0, 1, 1], [1, 1, 1], [2, 0, 1], [0, 2, 1]]
    moves = []
    for i in actions:
        j = do_action(state, i)
        if is_legal(j) and is_state_safe(j):
            moves.append(j)
    return moves

solutions = []

def solve(next_action, path):
    _path = path.copy()
    if next_action == end:
        _path.append(next_action)
        solutions.append(_path)
        return
    elif next_action in path:
        return
    else:
        _path.append(next_action)
        for i in next_possible_actions(next_action):
            solve(i, _path)

solve([3, 3, 1], [])
print(*solutions, sep="\n")
