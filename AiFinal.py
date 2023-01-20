import math
import heapq

def heuristic(state):
    m, c = state[0], state[1]
    return (3 - m) + (3 - c) # retourne le nombre de missionnaires et cannibales restant sur la rive actuelle

def is_valid_state(state, boat_pos):
    m, c = state[0], state[1]
    if boat_pos:
        return m >= c and m <= 3 and c <= 3
    else:
        return m >= c and m >= 0 and c >= 0

def is_goal_state(state):
    return state == (0, 0)

def get_next_states(state, boat_pos):
    m, c = state[0], state[1]
    next_states = []
    if m > 0 and c > 0:
        if boat_pos:
            next_states.append(((m-1, c-1), not boat_pos))
        else:
            next_states.append(((m+1, c+1), not boat_pos))
    elif m > 0:
        if boat_pos:
            next_states.append(((m-1, c), not boat_pos))
        else:
            next_states.append(((m+1, c), not boat_pos))
    elif c > 0:
        if boat_pos:
            next_states.append(((m, c-1), not boat_pos))
        else:
            next_states.append(((m, c+1), not boat_pos))
    if m > 1:
        if boat_pos:
            next_states.append(((m-2, c), not boat_pos))
        else:
            next_states.append(((m+2, c), not boat_pos))
    if c > 1:
        if boat_pos:
            next_states.append(((m, c-2), not boat_pos))
        else:
            next_states.append(((m, c+2), not boat_pos))
    if m > 0 and c > 1:
        if boat_pos:
            next_states.append(((m-1, c-2), not boat_pos))
        else:
            next_states.append(((m+1, c+2), not boat_pos))
    return [(x, y) for x, y in next_states if is_valid_state(x, y)]

def ida_star(start_state, limit, path=[], visited={}):
    f = len(path) + heuristic(start_state[0])
    if f > limit:
        return f
    if is_goal_state(start_state[0]):
        return path
    if start_state in visited and visited[start_state] <= f:
        return math.inf
    visited[start_state] = f
    min_cost = math.inf
    priority_queue = []
    for next_state in get_next_states(start_state[0], start_state[1]):
        g = len(path) + 1
        h = heuristic(next_state[0])
        f = g + h
        heapq.heappush(priority_queue, (f, g, next_state))
    while priority_queue:
        _, g, next_state = heapq.heappop(priority_queue)
        result = ida_star(next_state, limit, path + [next_state], visited)
        if isinstance(result, list):
            return result
        min_cost = min(min_cost, result)
    limit = min_cost
    return min_cost

visited = {}
path = []
start_state = ((3, 3), True)
limit = heuristic(start_state[0])
count = 0

while True:
    result = ida_star(start_state, limit, path, visited)
    if isinstance(result, list):
        print("Solution found:", result)
        break
    limit = result
    count += 1
    if count > 1000:
        print("No solution found after iterations.")
        break
else:
    print("No solution found.")