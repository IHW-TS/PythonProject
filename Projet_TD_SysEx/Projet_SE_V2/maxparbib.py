import maxpar
import matplotlib.pyplot as plt

def test_maxpar():
    # Création des tâches avec leurs dépendances et leurs fonctions de mise à jour
    t1 = maxpar.Task("T1", [], ["X"], lambda: maxpar.runT1(s1))
    t2 = maxpar.Task("T2", [], ["Y"], lambda: maxpar.runT2(s1))
    tSomme = maxpar.Task("somme", ["X", "Y"], ["Z"], lambda: maxpar.runTsomme(s1))

    # Création du système de tâches avec la liste des tâches et leurs relations de précédence
    s1 = maxpar.TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
    
    # Exécution séquentielle des tâches
    s1.runSeq()
    print(s1.X, s1.Y, s1.Z)

    # Exécution parallèle des tâches
    s1.run()
    print(s1.X, s1.Y, s1.Z)

    # Affichage du graphe de précédence
    s1.draw()

    # Test de déterminisme avec des exécutions randomisées
    s1.detTestRnd()

    # Comparaison des temps d'exécution séquentielle et parallèle
    s1.parCost()

# Appel de la fonction de test lors de l'exécution du fichier
if __name__ == "__main__":
    test_maxpar()
