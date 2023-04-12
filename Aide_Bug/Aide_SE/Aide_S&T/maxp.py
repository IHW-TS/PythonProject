from maxpar import *
import threading

class Task:
    name = ""
    reads = []
    writes = []
    run = None

class TaskSystem:
    def __init__(self, listeTaches, precedences):
        self.listeTaches = listeTaches
        self.precedences = precedences

    def getDependencies(self, nomTache):
        listeDep = self.precedences.get(nomTache)
        return listeDep
   
    def runSec(self):
        tacheExecutees = [] # Initialisation d'une liste vide pour stocker les tâches exécutées.
        
        while len(tacheExecutees) < len(self.precedences): # tant que le nombre de tâches exécutées est inférieur au nombre total de tâches à exécuter
            for cle, valeur in self.precedences.items():
                if cle not in tacheExecutees and set(valeur).issubset(tacheExecutees): # Si la tâche n'a pas encore été exécutée et que toutes ses dépendances ont été exécutées (c'est-à-dire si l'ensemble des dépendances est inclus dans l'ensemble des tâches exécutées)
                    for t in self.listeTaches:
                        if t.name == cle:
                            t.run()
                            tacheExecutees.append(cle)
                            break                      


    def run(self):
        tacheExecutees = [] # Initialisation d'une liste vide pour stocker les tâches exécutées.
        threads = []
        while len(tacheExecutees) < len(self.precedences): # tant que le nombre de tâches exécutées est inférieur au nombre total de tâches à exécuter
            for cle, valeur in self.precedences.items():
                if cle not in tacheExecutees and set(valeur).issubset(tacheExecutees): # Si la tâche n'a pas encore été exécutée et que toutes ses dépendances ont été exécutées (c'est-à-dire si l'ensemble des dépendances est inclus dans l'ensemble des tâches exécutées)
                    for tache in self.listeTaches:
                        if tache.name == cle:
                            thread = threading.Thread(target=tache.run)
                            thread.start()
                            threads.append(thread)
                            tacheExecutees.append(cle)
                            break
        for thread in threads:
            thread.join()



