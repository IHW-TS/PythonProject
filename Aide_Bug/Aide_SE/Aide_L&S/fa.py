import threading
import random 
import networkx as nx
import time 
import matplotlib.pyplot as plt


class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

class TaskSysteme:
    def __init__(self, taches, parent):
        self.taches = taches # PTN DE MERD....... TU L'AS APPELER TACHES SA FAIT 10MN JE CHERCHE PK CA MARCHE PAS JE SAIS QUE C TOI SAJ ET DANS LA FONCTION RUN TU L4APPELLES TASKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
        self.parent = parent
        self.X = None
        self.Y = None
        self.Z = None

    def verif(self):
        task_names = [task.name for task in self.taches]
        if len(task_names) != len(set(task_names)):
            print("Le nom des taches a été dupliqué, il doit être unique")

        for task in self.taches:
            if task.name not in self.parent.keys():
                print("Les parents n'existent pas") 
    
    def getDependies(self, nomTache):
        return self.parent.get(nomTache, [])
       
    # Fonction runSeq modifié parce que vous avez litéraleemnt faire de la merde 
    def runSeq(self):
        order = []
        remaining_tasks = set(self.taches)
        while remaining_tasks:
            for task in list(remaining_tasks):
                dependencies = self.getDependies(task.name)
                if all(dep in [t.name for t in order] for dep in dependencies):
                    task.run()
                    order.append(task)
                    remaining_tasks.remove(task)
                    break
            else:
                print("Cycle de dépendances détecté")
                break

    def run(self):
        self.verif()
        order = []
        remaining_tasks = set(self.taches)
        while remaining_tasks:
            for task in list(remaining_tasks):
                dependencies = self.getDependies(task.name)
                if all(dep in [t.name for t in order] for dep in dependencies):
                    order.append(task)
                    remaining_tasks.remove(task)
                    break
            else:
                print("Cycle de dépendances détecté")
                break

        threads = []
        for task in order:
            t = threading.Thread(target=task.run)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
       
    #Fonction chargée de dessiner le graphe 
    def dessin_graphe(self):
        G = nx.DiGraph()  # Utiliser un graphe orienté
        for task in self.taches:
            G.add_node(task.name)  # Ajouter les noms des tâches comme nœud
            for dep in self.parent[task.name]:
                G.add_edge(dep, task.name)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="grey", font_size=10, font_weight="bold", node_size=1500)
        plt.show()
    
    def detTestRnd(self):
        self.X = random.randint(1, 10)  # Corrigé: utilisation de la fonction randint pour générer un entier aléatoire
        self.Y = random.randint(1, 10)  # Corrigé: utilisation de la fonction randint pour générer un entier aléatoire

        self.run()

        res1 = self.Z

        self.X = random.randint(1, 10)  # Corrigé: utilisation de la fonction randint pour générer un entier aléatoire
        self.Y = random.randint(1, 10)  # Corrigé: utilisation de la fonction randint pour générer un entier aléatoire

        self.run()

        res2 = self.Z

        if res1 != res2:
            print("Le test n'est pas déterministe")
        else:
            print("Le test est déterministe")


    def parCost(self, n_executions=100):
        temps_executions_seq = []
        temps_executions_par = []

        for _ in range(n_executions):

            t0 = time.time()
            self.runSeq()
            t1 = time.time()
            temps_executions_seq.append(t1 - t0)

            t2 = time.time()
            self.run()
            t3 = time.time()
            temps_executions_par.append(t3 - t2)

        # Suppr les 2 premières exécutions pour éliminer l'effet du cache
        del temps_executions_seq[0:2]
        del temps_executions_par[0:2]

        temps_moyen_seq = sum(temps_executions_seq) / len(temps_executions_seq)
        temps_moyen_par = sum(temps_executions_par) / len(temps_executions_par)

        print("Temps d'exécution séquentiel moyen:", temps_moyen_seq)
        print("Temps d'exécution parallèle moyen:", temps_moyen_par)

#Question 3: variables globales -> on met dans les classes pour éviter des bugs => blabla à l'oral                    
        
    def runT1(self):
        self.X = 1

    def runT2(self):
        self.Y = 2

    def runTsomme(self):
        self.Z = self.Y + self.X