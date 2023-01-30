# "sys" fournit des fonctionnalités pour interagir avec le système
# "copy" permet de copier des objets en Python sans les lier à leur source.
import sys
import copy

# Nombre de missionnaires et de cannibales sur la berge gauche au départ, initialisé à 3 et la barque à 1 (0 quand il sera sur la rive de gauche) 
start = [3, 3, 1]
# Taille maximale des groupes de missionnaires et de cannibales et du "bateau"
size = 3
# Liste des actions possibles pour faire les missionnaires et les cannibales, la dernière valeur correspond à la barque 
# On peut prendre en exemple le premier cas [1, 0, 1] : Ici on donne la possibilité au programme de réaliser l'action de faire traverser un missionnaire de l'autre coté du fleuve si le nombre de canniblaes est à 0 et que le bateau est à droite (pour rappelle l'indice signifie que la barque se trouve dans le côté droit de la rivière)
possible_actions = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [0, 2, 1], [1, 1, 1]]
# "Memo" est une liste qui est utilisée pour stocker les différents états du bateau rencontrés lors de l'exécution de l'algorithme. Cela permet d'éviter de refaire les mêmes étapes plusieurs fois, ce qui accélère l'algorithme. Si un état donné a déjà été vu, l'algorithme ne le considérera pas à nouveau, ce qui évite les boucles infinies et améliore les performances du programme.
# Par exemple, considérons que nous cherchons à déplacer 3 missionnaires et 3 cannibales d'une rive à l'autre en utilisant un bateau qui ne peut transporter qu'une ou deux personnes à la fois. L'algorithme va explorer toutes les possibilités pour trouver la solution optimale en termes de nombre de déplacements de bateau. Si l'algorithme rencontre déjà un état où 2 missionnaires et 1 cannibale sont sur la rive gauche, il n'a plus besoin de recommencer à partir de cet état, car il a déjà été exploré. Au lieu de cela, l'algorithme peut simplement enregistrer cet état dans la liste "memo" et continuer à explorer les autres possibilités.
memo = []
# Le nombre d'étape nécessaire pour toruver la solution 
solution = 0

# Tout d'abord il faut savoir que les fonctions "substract" et "add" sont des fonctions qui effectuent une opération arithmétique sur des vecteurs de longueur 3 (longeur 3 vous connaissez la raison)
# La fonction "substract" soustrait chaque élément d'un vecteur à partir de l'élément correspondant d'un autre vecteur. 
# Par exemple, si vec1 = [3, 2, 1] et vec2 = [1, 1, 0], la fonction renverra [2, 1, 1], ce qui signifie que deux missionnaires et un bateau ont été soustraits de la première liste pour obtenir la deuxième liste.
def substract(vec1, vec2):
    return [vec1[i] - vec2[i] for i in range(3)]

# De même la fonction "add" additionne chaque élément. 
# Par exemple, si vec1 = [3, 2, 1] et vec2 = [1, 1, 0], la fonction renverra [4, 3, 1], ce qui signifie que deux missionnaires et un bateau ont été ajoutés à la première liste pour obtenir la deuxième liste.
def add(vec1, vec2):
    return [vec1[i] + vec2[i] for i in range(3)]

# Vérifie si une action est valide pour ajouter des missionnaires et des cannibales sur la berge gauche
def valid_add(vec):
    # Initialisation de la liste qui contiendra les actions valides
    actions = [] 
    # Pour chaque action dans la liste des actions possibles
    for action in possible_actions:
        # Calcule la nouvelle situation après l'exécution de cette action. Ici on appelle la fonction add avec en paramètre vec qui a les qui prends l'etat inital (barque, misionnaires, cannibales), et action qui va représenter une aciton possible a effectuer. Ainsi add est un nouveau vecteur qui représente l'état résultant de l'exécution de l'action.
        added = add(vec, action) 
        # Le nombre de missionnaires et de cannibales sur l'autre rive est calculé en utilisant la fonction substract avec [size, size, 1] ( on aurait pu ecrire [3, 3, 1]) comme vecteur de soustraction.
        other = substract([size, size, 1], added) 
        # Vérifie si la nouvelle situation est valide en suivant les règles de jeu
        # "added[0] >= 0" vérifie que le nombre de missionnaires sur la rive gauche après l'action est supérieur ou égal à zéro.
        # "added[1] >= 0" vérifie que le nombre de cannibales sur la rive gauche après l'action est supérieur ou égal à zéro.
        # "added[0] <= size" vérifie que le nombre de missionnaires sur la rive gauche après l'action est inférieur ou égal à la taille maximale.
        # "added[1] <= size" vérifie que le nombre de cannibales sur la rive gauche après l'action est inférieur ou égal à la taille maximale. 
        # "(added[0] >= added[1] or added[0] == 0)" vérifie que le nombre de missionnaires sur la rive gauche après l'action est supérieur ou égal au nombre de cannibales ou que le nombre de missionnaires est égal à zéro.
        # "(other[0] >= other[1] or other[0] == 0)" vérifie que le nombre de missionnaires sur la rive droite après l'action est supérieur ou égal au nombre de cannibales ou que le nombre de missionnaires est égal à zéro.
        if added[0] >= 0 and added[1] >= 0 and added[0] <= size and added[1] <= size and (added[0] >= added[1] or added[0] == 0) and (other[0] >= other[1] or other[0] == 0):
            # Si toutes les conditions sont remplies, l'action est considérée comme valide et ajoutée à la liste "actions".
            # Pour rappel, la fonction append est une méthode de la classe list en Python qui permet d'ajouter un élément à la fin de la liste.
            actions.append(action)        
    return actions 

# Par Exemple : Supposons que vector = [2, 2, 1] et size = 3.
# La fonction valid_add retournerait la liste d'actions [[0, 1, 1]], car seul l'embarquement de 1 cannibale sur l'autre rive respecte les contraintes du problème

# La fonction valid_substract fonctionne de manière similaire à valid_add, mais dans le sens inverse. Elle soustrait les personnes de la rive gauche et les ajoute à la rive droite.
def valid_substract(vec):
    actions = []
    for action in possible_actions:
        substracted = substract(vec, action)
        other = substract([size, size, 1], substracted)
        if substracted[0] >= 0 and substracted[1] >= 0 and substracted[0] <= size and substracted[1] <= size and (substracted[0] >= substracted[1] or substracted[0] == 0) and (other[0] >= other[1] or other[0] == 0):
            actions.append(action)

    return actions


def solve(vec, moves):
    # l'utilisation de la déclaration globale permet à la fonction solve d'accéder à la variable "solution" qui a été définie en dehors de la fonction.
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

    # Déterminer les actions valides en fonction de l'état actuel
    if vec[2] == 0:
        # Si le bateau est sur la rive gauche, les actions valides sont les actions d'ajout
        actions = valid_add(vec)
    else:
        # Sinon, le bateau est sur la rive droite et les actions valides sont les actions de soustraction
        actions = valid_substract(vec)

    # Boucle sur les actions valides pour trouver une solution
    for action in actions:
        # Copier le vecteur actuel pour éviter tout effet de bord
        new_vector = copy.deepcopy(vec)
        # Appliquer l'action au vecteur
        for i in range(3):
            if new_vector[2] == 0:
                new_vector[i] += action[i]
            else:
                new_vector[i] -= action[i]

        # Si la somme des éléments du nouveau vecteur est 0, cela signifie que tout le monde est de l'autre côté
        if sum(new_vector) == 0:
            # Imprimez le nombre de mouvements et les nombres de missionnaires et de cannibales de chaque rive
            print(moves, [new_vector[0], new_vector[1], new_vector[2]*2, size-new_vector[0], size-new_vector[1]])
            # Stockez le nombre de mouvements dans la variable globale solution
            solution = moves
            # Retournez True pour indiquer que la solution a été trouvée
            return True

        # Teste si la fonction `solve` renvoie True pour le vecteur `new_vector` et le nombre de mouvements `moves`.
        if solve(new_vector, moves):
            # Si `solve` renvoie True, imprime le nombre de mouvements et la distribution des missionnaires et des cannibales sur les deux rives.
            print(moves, [new_vector[0], new_vector[1], new_vector[2]*2, size-new_vector[0], size-new_vector[1]])
            # Renvoie True pour signaler que la solution a été trouvée.
            return True

        # Si la solution n'a pas été trouvée, renvoie False.
        return False

# Appelle la fonction `solve` pour trouver une solution pour le vecteur `start` et 0 mouvements.
solve(start, 0)

# Imprime le nombre de mouvements pour trouver la solution.
print(solution)
