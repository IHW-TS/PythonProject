#!/bin/python
#-*-coding:utf-8-*-
 
import copy
 
# donnees des noeuds
F, G, H, JEU, PAPA = 0, 1, 2, 3, 4
 
class Solveur :
    '''
    Le solveur de taquin
    '''
 
    def __init__(self, taquin) :
        self.openList = []
        self.closedList = []
 
        self.taquinInitial = taquin
        self.numeroCaseVide = taquin.numeroCaseVide
        self.taille = len(taquin.jeu)
 
        # on met l'etat initial
        self.openList.append([0, 0, 0, taquin.jeu, None])
 
 
    def resoudre(self) :
        print "Recherche de la solution..."
        while len(self.openList) > 0 :
 
            noeudCourant = self.openList.pop(0)
            taquin = noeudCourant[JEU]
 
            #self.closedList.append()
 
            if noeudCourant[JEU] == self.taquinInitial.jeuTrie :
                return noeudCourant
 
            # ajout des possibilites ...
            for ligne in range(0, self.taille) :
                for colonne in range(0, self.taille) :
 
                    if colonne > 0 and taquin[ligne][colonne-1] == self.numeroCaseVide :
                        tq = copy.deepcopy(taquin)
                        tq[ligne][colonne], tq[ligne][colonne-1] = tq[ligne][colonne-1], tq[ligne][colonne]
                        g = noeudCourant<strong>+1
                        h = self.heuristique(tq)
                        if not tq in self.closedList :
                            i = self.indiceDansListeOuverte(tq)
                            if i == -1 :
                                self.openList.append([g+h, g, h, tq, noeudCourant])
                            elif g+h < self.openList<em>[F] :
                                self.openList[i] = [g+h, g, h, tq, noeudCourant]
 
                    if colonne < self.taille - 1 and taquin[ligne][colonne+1] == self.numeroCaseVide :
                        tq = copy.deepcopy(taquin)
                        tq[ligne][colonne], tq[ligne][colonne+1] = tq[ligne][colonne+1], tq[ligne][colonne]
                        g = noeudCourant[G]+1
                        h = self.heuristique(tq)
                        if not tq in self.closedList :
                            i = self.indiceDansListeOuverte(tq)
                            if i == -1 :
                                self.openList.append([g+h, g, h, tq, noeudCourant])
                            elif g+h < self.openList[i][F] :
                                self.openList[i] = [g+h, g, h, tq, noeudCourant]
 
                    if ligne > 0 and taquin[ligne-1][colonne] == self.numeroCaseVide :
                        tq = copy.deepcopy(taquin)
                        tq[ligne][colonne], tq[ligne-1][colonne] = tq[ligne-1][colonne], tq[ligne][colonne]
                        g = noeudCourant[G]+1
                        h = self.heuristique(tq)
                        if not tq in self.closedList :
                            i = self.indiceDansListeOuverte(tq)
                            if i == -1 :
                                self.openList.append([g+h, g, h, tq, noeudCourant])
                            elif g+h < self.openList[i][F] :
                                self.openList[i] = [g+h, g, h, tq, noeudCourant]
 
                    if ligne < self.taille - 1 and taquin[ligne+1][colonne] == self.numeroCaseVide :
                        tq = copy.deepcopy(taquin)
                        tq[ligne][colonne], tq[ligne+1][colonne] = tq[ligne+1][colonne], tq[ligne][colonne]
                        g = noeudCourant[G]+1
                        h = self.heuristique(tq)
                        if not tq in self.closedList :
                            i = self.indiceDansListeOuverte(tq)
                            if i == -1 :
                                self.openList.append([g+h, g, h, tq, noeudCourant])
                            elif g+h < self.openList[i][F] :
                                self.openList[i] = [g+h, g, h, tq, noeudCourant]
 
            self.openList.sort()
 
        print None
 
 
    def indiceDansListeOuverte(self, jeu) :
        for i in range(0, len(self.openList)) :
            if self.openList[i][3] == jeu :
                return i
        return -1
 
 
    def heuristique(self, taquin) :
        i = 0
        for ligne in range(0, self.taille) :
            for colonne in range(0, self.taille) :
                if taquin[ligne][colonne] != self.taquinInitial.jeuTrie[ligne][colonne] :
                    i += 1
        return i
 
 
class Taquin :
    '''
    Le jeu en lui meme
    '''
 
    def __init__(self, jeu = None) :
        if jeu != None :
            self.setJeu(jeu)
 
    def __repr__(self) :
        return 'n'.join( ''.join(str(i)) for i in self.jeu )
 
    def setJeu(self, jeu) :
        self.jeu = [ list(i) for i in jeu ]
        self.numeroCaseVide = len(self.jeu) - 1
 
        self.jeuTrie = [ [] for i in range(len(self.jeu)) ] # pour ne pas le recalculer a chaque fois
        for i in range(len(self.jeu)) :
            self.jeuTrie[i] = [ j for j in range(len(self.jeu)*i, len(self.jeu)*i + len(self.jeu)) ]
 
    def setNumeroCaseVide(self, i) :
        self.numeroCaseVide = i
 
    def printEtatFini(self) :
        print 'n' + 'n'.join( ''.join(str(i)) for i in self.jeuTrie )
 
    def termine(self) :
        return [ i for i in self.jeu ] == self.jeuTrie
 
    def resoudre(self) :
        solveur = Solveur(self)
        res = solveur.resoudre()
        if res == None :
            print "Pas de solution trouvee"
            return
        print "Solution trouvee"
 
        L = []
        while res[PAPA] != None :
            L.append(res[PAPA][JEU])
            res = res[PAPA]
        L.reverse()
 
        for elem in L :
            print 'n' + 'n'.join( ''.join(str(i)) for i in elem )
        self.printEtatFini()
 
'''
6 3 1
8 0 2
7 4 5
'''
 
if __name__ == "__main__" :
    tq = Taquin()
    tq.setJeu( [ [6, 3, 1], [8, 0, 2], [7, 4, 5] ] )
    tq.setNumeroCaseVide(2)
    tq.resoudre()