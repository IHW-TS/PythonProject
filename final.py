import networkx as nx #  On l'utilise pour créer un graphe orienté et ajouter les nœuds en fonction des tâches et dépendances définies dans TaskSystem.
import matplotlib.pyplot as plt # permet de dessiner le graph

class Task:
    # chaque instance de la class task peut avoir un nom différent c pourquoi on déclare "name" en tant que variable d'instance dans le constructeur (__init__) de la classe.
    def __init__(self):  # utilisation de self pour les instances de classe (on peut acceder aux attributs et aux methodes des classes)
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None


class TaskSystem:  # initialisation de la classe TaskSystem pour une liste de tache
    def __init__(self, tasks, precedence):  # utilisation du dictionnaire init qui va prendre en entrée une liste de tache

        # crée une liste des noms des tâches à partir de la liste des tâches
        task_names = [task.name for task in tasks]

        for task_name in task_names: # boucle qui parcourt la liste task_names 
            if task_names.count(task_name) > 1: # on utilise la méthode count pour compter le nombre de fois ou ce nom apparait dans la liste 
                raise ValueError(f"Task dupliqué : {task_name}")

        for task_name, dependencies in precedence.items(): # vérifie si les tâches dépendantes existent dans la liste des tâches

            if task_name not in task_names: # condition si la tâche actuelle existe dans la liste des tâches
                raise ValueError(f"La Task {task_name} n'existe pas dans la liste des tâches")

            for dependency in dependencies: # boucle qui vérifie si les dépendances de la tâche actuelle existent dans la liste des tâches
                if dependency not in task_names:
                    raise ValueError(f"La Task {dependency} n'existe pas dans la liste des tâches")

        self.tasks = tasks
        self.precedence = precedence
    
    def draw(self):
        G = nx.DiGraph() # création d'un graph orienté 
        for task in self.tasks:  # boucle for qui parcours les taches dans self.task 
            G.add_node(task.name) # ajoute chaque tâche dans le graphe en utilisant la méthode add_node() 
        for task_name, dependencies in self.precedence.items(): # boucle qui permet de parcourir les tâches et leurs dépendances dans la variable self.precedence, en utilisant items() pour accéder aux clés et aux valeurs du dictionnaire.
            for dependency in dependencies:
                G.add_edge(dependency, task_name) # joute des arêtes au graphe pour chaque dépendance en utilisant la méthode add_edge()
        nx.draw(G, with_labels=True) # utilisation de la fonction draw() de NetworkX pour dessiner le graphe, en spécifiant "with_labels = True" pour afficher les étiquettes des nœuds.
        plt.show() # afficher le graphe.


    # Prend en entré le nom d'un tache et renvoie les taches sui provient de cette dépendance
    def getDependencies(self, task_name):
        return self.precedence[task_name]

    def run(self):
        # créer un ensemble de tâches pouvant être exécutées en parallèle
        # declaration d'un ensemble vide avec set(), chaque élément doit être unique et immuable
        parallel_tasks = set()
        for task in self.tasks:  # boucle for qui parcours les taches dans self.task qui autorise l'execution de chaque task
            run_task = True
            # permet d'obtenir la liste des tasks en cours à partir du nom
            for dependency in self.getDependencies(task.name):
                # si la taks en cours n'est pas dans la liste des noms des taches en cours alors la boucle renvoie false et s'arrête
                if dependency not in [t.name for t in parallel_tasks]:
                    run_task = False
                    break
            if run_task:  # la task  en cours et alors rajouté a parallel_tasks
                parallel_tasks.add(task)

        # on lance des taches parallèlles une fois que toute les tasks on été parcourues avec la boucle for on les exécutes
        for task in parallel_tasks:
            task.run()


# indique que les variables n'ont pas de valeur, ce qui permet d'être sûr qu'elles n'ont pas de valeur avant d'être utilisées par les fonctions.

X = 0
Y = 0
Z = 0

# initialisation des fonctions en variables globales

def runT1():
    global X
    X = X + 1

def runT2():
    global Y
    Y = Y + 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

# on crée une instande de la classe "task" que l'on appelle "T1" ou on initialise les informations de cette instance grâce au constructeur "__init__"

t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

# crée une tache
s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
s1.run()
s1.draw()

print(X)
print(Y)
print(Z)
