from fa import *

def lancementProg():
    s1 = TaskSysteme([], {})

    t1 = Task("T1", [], ["X"], s1.runT1)
    t2 = Task("T2", [], ["Y"], s1.runT2)

    tSomme = Task("somme", ["X", "Y"], ["Z"], s1.runTsomme)

    s1.taches = [t1, t2, tSomme]
    s1.parent = {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]}

    s1.runSeq()
    print(s1.X, s1.Y, s1.Z) 

    s1.run()
    print(s1.X, s1.Y, s1.Z) 

   # s1.dessin_graphe()

    s1.detTestRnd() 

    s1.parCost()

if __name__ == "__main__":
    lancementProg()
