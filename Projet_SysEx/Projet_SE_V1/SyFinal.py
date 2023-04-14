# coding: utf-8
# On l'utilise pour créer un graphe orienté et ajouter les nœuds en fonction des tâches et dépendances définies dans TaskSystem.
import networkx as nx 
# permet de dessiner le graph
import matplotlib.pyplot as plt 

# chaque instance de la class task peut avoir un nom différent c pourquoi on déclare "name" en tant que variable d'instance dans le constructeur (__init__) de la classe.
class Task:
    # utilisation de self pour les instances de classe (on peut acceder aux attributs et aux methodes des classes)
    def __init__(self):  
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

# initialisation de la classe TaskSystem pour une liste de tache
class TaskSystem:  
    # utilisation du dictionnaire init qui va prendre en entrée une liste de tache
    def __init__(self, tasks, precedence):  
        # crée une liste des noms des tâches à partir de la liste des tâches
        task_names = [task.name for task in tasks]
        # boucle qui parcourt la liste task_names 
        for task_name in task_names: 
            # on utilise la méthode count pour compter le nombre de fois ou ce nom apparait dans la liste 
            if task_names.count(task_name) > 1: 
                raise ValueError("Task dupliquée : " + task_name)
        # vérifie si les tâches dépendantes existent dans la liste des tâches
        for task_name, dependencies in precedence.items(): 
            # condition si la tâche actuelle existe dans la liste des tâches
            if task_name not in task_names: 
                raise ValueError("La Task " + task_name + " n'existe pas dans la liste des tâches")
            # boucle qui vérifie si les dépendances de la tâche actuelle existent dans la liste des tâches
            for dependency in dependencies: 
                if dependency not in task_names:
                    raise ValueError("La Task " + dependency + " n'existe pas dans la liste des tâches")

        self.tasks = tasks
        self.precedence = precedence
    
    def draw(self):
        # création d'un graph orienté 
        G = nx.DiGraph()
        # boucle for qui parcours les taches dans self.task 
        for task in self.tasks:
            # ajoute chaque tâche dans le graphe en utilisant la méthode add_node() 
            G.add_node(task.name) 
        # boucle qui permet de parcourir les tâches et leurs dépendances dans la variable self.precedence, en utilisant items() pour accéder aux clés et aux valeurs du dictionnaire.
        for task_name, dependencies in self.precedence.items(): 
            for dependency in dependencies:
                # joute des arêtes au graphe pour chaque dépendance en utilisant la méthode add_edge()
                G.add_edge(dependency, task_name)
        # utilisation de la fonction draw() de NetworkX pour dessiner le graphe, en spécifiant "with_labels = True" pour afficher les étiquettes des nœuds.
        nx.draw(G, with_labels=True) 
        # afficher le graphe.
        plt.show() 


    # Prend en entré le nom d'un tache et renvoie les taches sui provient de cette dépendance
    def getDependencies(self, task_name):
        return self.precedence[task_name]

    def run(self):
        # créer un ensemble de tâches pouvant être exécutées en parallèle
        # declaration d'un ensemble vide avec set(), chaque élément doit être unique et immuable
        parallel_tasks = set()
        # boucle for qui parcours les taches dans self.task qui autorise l'execution de chaque task
        for task in self.tasks:  
            run_task = True
            # permet d'obtenir la liste des tasks en cours à partir du nom
            for dependency in self.getDependencies(task.name):
                # si la taks en cours n'est pas dans la liste des noms des taches en cours alors la boucle renvoie false et s'arrête
                if dependency not in [t.name for t in parallel_tasks]:
                    run_task = False
                    break
            # la task  en cours et alors rajouté a parallel_tasks
            if run_task:  
                parallel_tasks.add(task)

        # on lance des taches parallèlles une fois que toute les tasks on été parcourues avec la boucle for on les exécutes
        for task in parallel_tasks:
            task.run()


# indique que les variables n'ont pas de valeur, ce qui permet d'être sûr qu'elles n'ont pas de valeur avant d'être utilisées par les fonctions.

X = 0
Y = 0
Z = 0

# initialisation des fonctions en variables globales mpeme si leur utilsaiton en globale peut rendre le code plus vulnérables aux erreures et peut le rendre moins modulaire et utilisable

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

# Critère de la tâche a executer
s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]}) 
# lance la fonction def run 
s1.run()
# lance la fonction def draw 
s1.draw() 

# Affiche les valeurs de X Y Z 
print(X)
print(Y)
print(Z)
