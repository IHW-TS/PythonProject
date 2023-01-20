import queue

def is_valid_state(state):
    m, c = state[0], state[1]
    return m >= 0 and c >= 0 and (m == 0 or m >= c) and m + c <= 3

def is_goal_state(state):
    return state == (0, 0)

def get_next_states(state):
    m, c = state
    next_states = []
    if m > 0:
        next_states.append((m-1, c))
        next_states.append((m-1, c-1))
    if c > 0:
        next_states.append((m, c-1))
        next_states.append((m-1, c-1))
    if m > 1:
        next_states.append((m-2, c))
    if c > 1:
        next_states.append((m, c-2))
    if m > 0 and c > 1:
        next_states.append((m-1, c-2))
    return [state for state in next_states if is_valid_state(state)]

def bfs(start_state):
    q = queue.Queue()
    q.put((start_state, []))
    visited = set()
    while not q.empty():
        state, path = q.get()
        if state in visited:
            continue
        visited.add(state)
        if is_goal_state(state):
            return path
        for next_state in get_next_states(state):
            q.put((next_state, path + [next_state]))
    return None

start_state = (3, 3)
path = bfs(start_state)
if path is not None:
    print("Solution found:", path)
else:
    print("No solution found.")
