import heapq

def is_valid_state(state):
    m, c = state[0], state[1]
    return m >= 0 and c >= 0 and (m == 0 or m >= c) and m + c <= 3

def is_goal_state(state):
    return state == (0, 0)

def heuristic(state):
    m, c, boat_side = state
    return 3 - m + 3 - c

def get_next_states(state, boat_side):
    m, c, _ = state
    next_states = []
    if boat_side == 'left':
        if m > 0:
            next_states.append((m-1, c, 'right'))
            if c > 0:
                next_states.append((m-1, c-1, 'right'))
        if c > 0:
            next_states.append((m, c-1, 'right'))
        if m > 1:
            next_states.append((m-2, c, 'right'))
        if c > 1:
            next_states.append((m, c-2, 'right'))
        if m > 0 and c > 1:
            next_states.append((m-1, c-2, 'right'))
    else:
        if m < 3:
            next_states.append((m+1, c, 'left'))
            if c < 3:
                next_states.append((m+1, c+1, 'left'))
        if c < 3:
            next_states.append((m, c+1, 'left'))
        if m < 2:
            next_states.append((m+2, c, 'left'))
        if c < 2:
            next_states.append((m, c+2, 'left'))
        if m < 3 and c < 2:
            next_states.append((m+1, c+2, 'left'))
    return [state for state in next_states if is_valid_state(state)]

def IDAstar(start_state, threshold, path):
    m, c, boat_side = start_state
    if (m, c) in path:
        return None
    if m == 0 and c == 0 and boat_side == 'right':
        return path
    if threshold == 0:
        return None
    min_cost = len(path)
    for next_state in get_next_states(start_state, boat_side):
        new_path = path + [(m, c, boat_side)]
        cost = IDAstar(next_state, threshold - 1, new_path)
        if cost is not None and len(cost) < min_cost:
            path = cost
    return path

def print_solution(path):
    left_m, left_c, boat = path[0]
    print("[{}, {}, {}, {}, {}]".format(left_m, left_c, boat, 3-left_m, 3-left_c))
    for i in range(1, len(path)):
        left_m, left_c, boat = path[i-1]
        right_m, right_c, _ = path[i]
        print("[{}, {}, {}, {}, {}]".format(right_m, right_c, boat, 3-right_m, 3-right_c))

start_state = (3, 3, 'left')
path = []
threshold = heuristic(start_state)
while path is None:
    path = IDAstar(start_state, threshold, path)
    threshold += 1

if path is not None:
    print("Solution found:")
    print_solution(path)
else:
    print("No solution found.")
