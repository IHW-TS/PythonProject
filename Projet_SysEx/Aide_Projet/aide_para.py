import threading
import networkx as nx

# Définir la classe Task avec un nom et une fonction d'exécution
class Task:
    def __init__(self, name, run):
        self.name = name
        self.run = run

# Définir la classe TaskSystem pour gérer l'exécution des tâches
class TaskSystem:
    # Initialiser la classe avec une liste de tâches et un dictionnaire de précédence
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        # Construire le graphe de précédence à partir des informations fournies
        self.graph = self.build_graph()

    # Construire le graphe de précédence en utilisant la bibliothèque NetworkX
    def build_graph(self):
        # Créer un graphe dirigé vide
        G = nx.DiGraph()
        # Parcourir toutes les tâches
        for task in self.tasks:
            # Ajouter un noeud pour chaque tâche, en utilisant son nom
            G.add_node(task.name)
            # Parcourir les dépendances de la tâche actuelle
            for dep in self.precedence[task.name]:
                # Ajouter un arc dirigé entre chaque dépendance et la tâche actuelle
                G.add_edge(dep, task.name)
        # Retourner le graphe construit
        return G

    # Exécuter les tâches de manière séquentielle en utilisant un tri topologique du graphe
    def run_sequential(self):
        # Effectuer un tri topologique sur le graphe pour obtenir l'ordre d'exécution des tâches
        ordered_tasks = list(nx.topological_sort(self.graph))
        # Parcourir les tâches dans l'ordre obtenu
        for task_name in ordered_tasks:
            # Trouver l'instance de la tâche correspondante à partir de son nom
            task = next(t for t in self.tasks if t.name == task_name)
            # Exécuter la fonction d'exécution de la tâche
            task.run()


    # Exécuter les tâches de manière parallèle en utilisant des threads
    def run_parallel(self):
        # Obtenir la liste des tâches ordonnées en utilisant un tri topologique du graphe de précédence
        ordered_tasks = list(nx.topological_sort(self.graph))

        # Créer une liste vide pour stocker les threads qui seront créés
        threads = []

        # Parcourir la liste des tâches ordonnées
        for task_name in ordered_tasks:
            # Trouver l'objet tâche correspondant au nom de la tâche
            task = next(t for t in self.tasks if t.name == task_name)

            # Créer un nouveau thread pour exécuter la fonction run de la tâche
            thread = threading.Thread(target=task.run)

            # Démarrer le thread
            thread.start()

            # Ajouter le thread à la liste des threads
            threads.append(thread)

        # Attendre que tous les threads aient terminé
        for thread in threads:
            thread.join()


# Exemple d'utilisation
# Définir les fonctions pour les tâches
def task1():
    print("Exécution de la tâche 1")

def task2():
    print("Exécution de la tâche 2")

def task3():
    print("Exécution de la tâche 3")

# Créer des instances de la classe Task pour chaque tâche
t1 = Task("T1", task1)
t2 = Task("T2", task2)
t3 = Task("T3", task3)

# Créer une instance de la classe TaskSystem avec les tâches et les relations de précédence
task_system = TaskSystem([t1, t2, t3], {"T1": [], "T2": ["T1"], "T3": ["T1", "T2"]})

# Exécuter les tâches de manière séquentielle et parallèle pour tester le système
print("Exécution séquentielle :")
task_system.run_sequential()

print("\nExécution parallèle :")
task_system.run_parallel()