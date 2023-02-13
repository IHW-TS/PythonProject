# "copy" permet de copier des objets en Python sans les lier à leur source.
import copy

# Entrer le nombre de missionnaires et de cannibales ainsi que la capacité de la barque
n = int(input("Entrez le nombre de missionnaires et de cannibales: "))
p = int(input("Entrez la capacité de la bateau : "))
# On initialise le tableau "start" avec le nombre de missionnaires et cannibales, et la barque sur la rive de départ (1)
start = [n, n, 1]
# On définit la taille de la liste "possible_actions" en prenant le nombre maximal de missionnaires et cannibales
size = n
possible_actions = []


for i in range(p + 1):
    for j in range(p - i + 1):
        if i + j <= p:
            possible_actions.append([i, j, 1])


# "Memo" est une liste qui est utilisée pour stocker les différents états du bateau rencontrés lors de l'exécution de l'algorithme. Cela permet d'éviter de refaire les mêmes étapes plusieurs fois, ce qui accélère l'algorithme. Si un état donné a déjà été vu, l'algorithme ne le considérera pas à nouveau, ce qui évite les boucles infinies et améliore les performances du programme.
# Par exemple, considérons que nous cherchons à déplacer 3 missionnaires et 3 cannibales d'une rive à l'autre en utilisant un bateau qui ne peut transporter qu'une ou deux personnes à la fois. L'algorithme va explorer toutes les possibilités pour trouver la solution optimale en termes de nombre de déplacements de bateau. Si l'algorithme rencontre déjà un état où 2 missionnaires et 1 cannibale sont sur la rive gauche, il n'a plus besoin de recommencer à partir de cet état, car il a déjà été exploré. Au lieu de cela, l'algorithme peut simplement enregistrer cet état dans la liste "memo" et continuer à explorer les autres possibilités.
memo = []
# Le nombre d'étape nécessaire pour toruver la solution 
solution = 0

# Tout d'abord il faut savoir que les fonctions "suppr" et "add" sont des fonctions qui effectuent une opération arithmétique sur des vecteurs de longueur 3 (longeur 3 vous connaissez la raison)
# La fonction "suppr" soustrait chaque élément d'un vecteur à partir de l'élément correspondant d'un autre vecteur. 
# Par exemple, si vec1 = [3, 2, 1] et vec2 = [1, 1, 0], la fonction renverra [2, 1, 1], ce qui signifie que deux missionnaires et un bateau ont été soustraits de la première liste pour obtenir la deuxième liste.
def suppr(vec1, vec2):
    return [vec1[i] - vec2[i] for i in range(3)]

# De même la fonction "add" additionne chaque élément. 
# Par exemple, si vec1 = [3, 2, 1] et vec2 = [1, 1, 0], la fonction renverra [4, 3, 1], ce qui signifie que deux missionnaires et un bateau ont été ajoutés à la première liste pour obtenir la deuxième liste.
def add(vec1, vec2):
    return [vec1[i] + vec2[i] for i in range(3)]

# Vérifie si une action est valide pour ajouter des missionnaires et des cannibales sur la berge gauche
def v_add(vec):
    # Initialisation de la liste qui contiendra les actions valides
    actions = [] 
    # Pour chaque action dans la liste des actions possibles
    for action in possible_actions:
        # vérifie si la somme des deux premiers éléments de la liste "action" est supérieure ou égale à 2. En d'autres termes, cela signifie que la barque doit prendre au moins 2 personnes, missionnaires ou cannibales, à chaque tour. Si la somme est supérieure ou égale à 2, alors la liste "action" est ajoutée à la liste "possible_actions".
        if action[0] + action[1] >= 2:
        # Calcule la nouvelle situation après l'exécution de cette action. Ici on appelle la fonction add avec en paramètre vec qui a les qui prends l'etat inital (barque, misionnaires, cannibales), et action qui va représenter une aciton possible a effectuer. Ainsi add est un nouveau vecteur qui représente l'état résultant de l'exécution de l'action.
            x = add(vec, action) 
        # Le nombre de missionnaires et de cannibales sur l'autre rive est calculé en utilisant la fonction suppr avec [size, size, 1] ( on aurait pu ecrire [3, 3, 1]) comme vecteur de soustraction.
            y = suppr([size, size, 1], x) 
        # Vérifie si la nouvelle situation est valide en suivant les règles de jeu
        # "x[0] >= 0" vérifie que le nombre de missionnaires sur la rive gauche après l'action est supérieur ou égal à zéro.
        # "x[1] >= 0" vérifie que le nombre de cannibales sur la rive gauche après l'action est supérieur ou égal à zéro.
        # "x[0] <= size" vérifie que le nombre de missionnaires sur la rive gauche après l'action est inférieur ou égal à la taille maximale.
        # "x[1] <= size" vérifie que le nombre de cannibales sur la rive gauche après l'action est inférieur ou égal à la taille maximale. 
        # "(x[0] >= x[1] or x[0] == 0)" vérifie que le nombre de missionnaires sur la rive gauche après l'action est supérieur ou égal au nombre de cannibales ou que le nombre de missionnaires est égal à zéro.
        # "(y[0] >= y[1] or y[0] == 0)" vérifie que le nombre de missionnaires sur la rive droite après l'action est supérieur ou égal au nombre de cannibales ou que le nombre de missionnaires est égal à zéro.
            if x[0] >= 0 and x[1] >= 0 and x[0] <= size and x[1] <= size and (x[0] >= x[1] or x[0] == 0) and (y[0] >= y[1] or y[0] == 0):
            # Si toutes les conditions sont remplies, l'action est considérée comme valide et ajoutée à la liste "actions".
            # Pour rappel, la fonction append est une méthode de la classe list en Python qui permet d'ajouter un élément à la fin de la liste.
                actions.append(action)        
    return actions 

# Par Exemple : Supposons que vec = [2, 2, 1] et size = 3.
# La fonction v_add retournerait la liste d'actions [[0, 1, 1]], car seul l'embarquement de 1 cannibale sur l'autre rive respecte les contraintes du problème

# La fonction v_suppr fonctionne de manière similaire à v_add, mais dans le sens inverse. Elle soustrait les personnes de la rive gauche et les ajoute à la rive droite.
def v_suppr(vec):
    actions = []
    for action in possible_actions:
        if action[0] + action[1] >= 2: 
        # Suppr au lieu de add
            x = suppr(vec, action)
            y = suppr([size, size, 1], x)
            if x[0] >= 0 and x[1] >= 0 and x[0] <= size and x[1] <= size and (x[0] >= x[1] or x[0] == 0) and (y[0] >= y[1] or y[0] == 0):
                actions.append(action)
    return actions

def tree_search(vec, moves):
    # l'utilisation de la déclaration globale permet à la fonction tree_search d'accéder à la variable "solution" qui a été définie en dehors de la fonction.
    global solution

    # Vérifier si le vecteur actuel a déjà été vu auparavant
    if vec in memo:
        # Si oui, cela signifie que nous sommes en train de faire un cycle infini et nous retournons sans faire quoi que ce soit
        return
    else:
        # Sinon, ajoutez le vecteur à la liste des vecteurs déjà vus pour éviter les cycles infinis à l'avenir
        memo.append(vec)

    # Copier la liste de mouvements afin d'éviter les problèmes liés à la modification de la même variable dans plusieurs appels récursifs de la fonction.
    moves = copy.deepcopy(moves)
    # Ajouter 1 mouvement pour cette itération 
    moves += 1

    # Fonction qui retourne la liste des actions possibles en fonction de la position du bateau. 
    if vec[2] == 0: 
        # La fonction v_add retourne une liste d'actions qui sont valides pour être effectuées à partir de l'état actuel représenté par le vecteur ( quand le bateau est égale à 0)
        actions = v_add(vec)
    else:
        # Idem avec v_suppr
        actions = v_suppr(vec)

    for action in actions:
        # Créer une nouvelle copie du vecteur d'état actuel
        # new_vec est une copie indépendante de vec, ce qui permet de changer la liste sans affecter l'autre.
        new_vec = copy.deepcopy(vec)
        for i in range(3):
            # Créer une nouvelle copie du vecteur d'état actuel
            # Si new_vec[2] est égal à 0, l'action est ajoutée à l'élément correspondant du vecteur, sinon elle est soustraite. Cela modifie le vecteur d'état pour refléter les actions prises pour résoudre le problème des missionnaires et des cannibales.
            if new_vec[2] == 0:
                # Ajouter l'action à l'élément du vecteur
                new_vec[i] += action[i]
            else:
                # Sinon, soustraire l'action de l'élément du vecteur
                new_vec[i] -= action[i]
        # Cette condition vérifie si la somme de tous les éléments du nouveau vecteur est égale à zéro. Si c'est le cas, cela signifie que tous les missionnaires et les cannibales ont été déplacés de l'autre côté de la rivière et que la solution a été trouvée. Le nombre de mouvements nécessaires est alors affiché et enregistré dans la variable "solution". La fonction retourne ensuite "vrai" pour indiquer que la solution a été trouvée.
        if sum(new_vec) == 0:
            # Afficher le nombre de mouvements et les nouveaux nombres de missionnaires et de cannibales de chaque côté de la rivière
            print("Etape Finale", moves, "=", [new_vec[0], new_vec[1], new_vec[2], size-new_vec[0], size-new_vec[1]])
            # Enregistrer le nombre de mouvements dans la variable "solution"
            solution = moves
            return True
        # Idem sauf que ca permet de nous afficher le nombre d'etat réalisé
        if tree_search(new_vec, moves):
            # Afficher le nombre de mouvements et les nouveaux nombres de missionnaires et de cannibales de chaque côté de la rivière
            print("Etape",moves, "=", [new_vec[0], new_vec[1], new_vec[2], size-new_vec[0], size-new_vec[1]])
            return True
    # Si aucune solution n'a été trouvée, retourner False
    return False

# Appelle la fonction `tree_search` pour trouver une solution pour le vecteur `start` et initialiser à 0 mouvements.
tree_search(start, 0)

print("Le nombre d'etape totale est de =", solution)




