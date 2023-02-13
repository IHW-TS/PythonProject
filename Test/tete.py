# "copy" permet de copier des objets en Python sans les lier à leur source.
import copy

n = int(input("Entrez le nombre de missionnaires et de cannibales: "))
p = int(input("Entrez la capacité de la bateau : "))

start = [n, n, 1]
size = n
possible_actions = []

for i in range(p + 1):
    for j in range(p - i + 1):
        if i + j <= p:
            possible_actions.append([i, j, 1])

memo = []
solution = 0

def suppr(vec1, vec2):
    return [vec1[i] - vec2[i] for i in range(3)]

def add(vec1, vec2):
    return [vec1[i] + vec2[i] for i in range(3)]

def v_add(vec):
    actions = [] 
    for action in possible_actions:
        if action[0] + action[1] >= 1:
            x = add(vec, action) 
            y = suppr([size, size, 1], x) 
            if x[0] >= 0 and x[1] >= 0 and x[0] <= size and x[1] <= size and (x[0] >= x[1] or x[0] == 0) and (y[0] >= y[1] or y[0] == 0):
                actions.append(action)        
    return actions 

def v_suppr(vec):
    actions = []
    for action in possible_actions:
        if action[0] + action[1] >= 1: 
            x = suppr(vec, action)
            y = suppr([size, size, 1], x)
            if x[0] >= 0 and x[1] >= 0 and x[0] <= size and x[1] <= size and (x[0] >= x[1] or x[0] == 0) and (y[0] >= y[1] or y[0] == 0):
                actions.append(action)
    return actions

def tree_search(vec, moves):
    global solution

    if vec in memo:
        return
    else:
        memo.append(vec)

    moves = copy.deepcopy(moves)
    moves += 1

    if vec[2] == 0: 
        actions = v_add(vec)
    else:
        actions = v_suppr(vec)

    for action in actions:
        new_vec = copy.deepcopy(vec)
        for i in range(3):
            if new_vec[2] == 0:
                new_vec[i] += action[i]
            else:
                new_vec[i] -= action[i]
        if sum(new_vec) == 0:
            print("Etape Finale", moves, "=", [new_vec[0], new_vec[1], new_vec[2], size-new_vec[0], size-new_vec[1]])
            solution = moves
            return True
        if tree_search(new_vec, moves):
            print("Etape",moves, "=", [new_vec[0], new_vec[1], new_vec[2], size-new_vec[0], size-new_vec[1]])
            return True
    return False

tree_search(start, 0)

print("Le nombre d'etape totale est de =", solution)




