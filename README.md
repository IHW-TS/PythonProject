
# Projet en Python 
Plusieurs projets universitaire mettant en pratique la stratégie de recherche _A*_ pour
résoudre des taquins.
Développé en Python 3.6.0

## Projet en IA

#### Projet d'échauffement "Missionnaire et Cannibale" 

- Ennoncé du Sujet
- Rechercher en profondeur => Problème : Affiche le premier chemin trouvé et non le plus court, le reste est correct. 
- Compte rendu en LateX + étude expérimentale pas assez approfondie ( pas eu le temps), je recommande de faire un graphique et avec au moins 100 exécutions avec des valeurs différentes pour comparer le temps d'exécution du programme CPU etc... 
- **25%** de la Note Finale
- Note obtenue : **17/20**.

#### Projet "Taquin"

- Ennoncé du Sujet
- Le programme Python est correct et fonctionne bien, comme indiqué précédemment. Il s'agit du même programme que celui présenté dans le lien ci-dessous.
- **50%** de la Note Finale.
- La version Web en Bootstrap et un brouillon, il ne fonctionne pas mais ca peut donner une idée de présentation.
- **Pour avoir la version finale du projet (pour la version Web), il est disponible sur ce lien (contient le diaporama et le Rapport en Latex :** *https://github.com/IHW-TS/Taquin_Game_IA*
- La Version Web contient également un graphique qui réalise une moyenne du temps d'exécution, du temps CPU et du temps d'exécution pour différentes heuristiques et tailles de Taquin. Ceci permet d'analyser les performances des différentes approches et de déterminer la meilleure heuristique pour résoudre le problème du Taquin.
- Note obtenue : **17/20**.

## Projet en SE

#### Projet "Implémentation d'un système de gestion de tâches parallélisées"

- Ennoncé du Sujet
- Réalisation d'un programme en python => Implémenté un système de gestion de tâches parallélisées qui optimise les performances en exploitant les ressources de calcul disponibles.  
- Réalisation d'une structure de base pour mieux comprendre l'intérêt du projet => Très utile si vous ne comprenez rien au projet 
- On peut remarquer 2 versions du programme : 
```python
- Projet_SE_V1 : Fonctionne dans l'ensemble mais contient quelque bug.
                 Fonction Test randomisé de déterminisme n'a pas été réalisé. 
                 Il existe aussi un version avec deux fichiers qui imposé par le sujet.
- Projet_SE_V2 : Tout fonction correctement 
```
- Diaporama : Ne pas mettre des screens de votre code (vous perdrez des points), mais plutôt une explipcation de vos fonctions en génrale (cf diapo).
- **50%** de la note final voir plus (varie en fonction des années).
- Note obtenue : **16.5/20** (la partie question/réponse à l'oral, en fonction de la qualité de votre réponse, vous fera gagner ou perdre des points).

# Installation
### Windows
- Télécharger les dossiers pour les différents 
- Si besoin, installer la dernière version de Python 3 sur 
[le site officiel](https://www.python.org/downloads/windows/)
- Lancer l'interpréteur : `Démarrer > Programmes > Python 3.6 > IDLE Python GUI`
- Indiquer à Python dans quel répertoire se trouve les fichiers :
```python
>>> import sys
>>> sys.path.append('C:\Users\utilisateur\Documents\dossierContenanttaquinpy') #exemple
```

### Linux
- Idem
- Ouvrir un terminal, aller dans le répertoire contenant `taquin.py` et lancer
la commande `python`

