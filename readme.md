# Typeshift
### Le projet est séparé en plusieurs fichiers
##### 1. Le fichier config.json
- Il correspond au fichier de configuration, il contient un paramétre pour l'instant, c'est la taille du conteneur
de la grille de jeu. Le reste sera calculé en fonction de cette taille variable
##### 2. Le fichier dictionnary.json
- Il simule un dictionnaire contenant l'ensemble des mots français de 3 à 10 lettres et est utilisé de sorte que
s'il contenait rééllement l'ensemble des mots français de 3 à 10 lettres, il fonctionnerait parfaitement avec le jeu.
- Il contient un tableau à double dimension, chaque indice du tableau contient 20 mots de taille indice
(tab[3] contient 20 mots de taille 3 lettres).
On suppose que ces 20 mots sont les seuls qui existe en français pour chaque indice
##### 3. Le fichier globals.py
- Il contient les variables globales qui seront utilisés dans le jeu
Ex: Le niveau, le nombre de mots prévus pour cette partie, etc.
- Ici, le programme choisit au hasard le niveau (Une taille entre 3 et 10) et dans les mots de ce niveau, il choisit de charger
au hasard 3 ou 5 mots pour la partie en cours. Il calcule ensuite le score maximal en fonction du nombre de mots et du
nombre de lettres et prend en compte le fait que le joueur peut trouver des mots qui n'ont pas été prévus dans les
3 ou 5 mots choisis. C'est ici que l'on charge aussi la taille du conteneur de la grille depuis le fichier config.json
##### 4. Le fichier words.py
- Il contient la fonction qui charge les mots en fonction du niveau choisi par le programme
- On y recupere aussi tous les mots du niveau en cours dans une variable afin de prévoir les mots additionnels qui
seront trouvés par le joueur. On accede à cette variable que si l'on ne trouve pas un mot trouvé dans la variable
contenant les mots prévus
- On y affiche en guise de test:
    - Le niveau choisi par le programme (level)
    - Le nombre de mots prévus (expectedWords)
    - Le score maximal à atteindre dans la partie en cours (maxScore)
    - Tous les mots de taille niveau sauf ceux présents sur la grille (allWordsOfThisLevel)
    - Tous les mots présents sur la grille (words)
    - La taille du conteneur de la grille paramétré dans le fichier config.json (gridContainerSize)
##### 5. Le fichier game.py
- Il appele dans l'ordre toutes les fonctions permettant de jouer au jeu
##### 6. Le fichier main.py
- Il lance le jeu en faisant appel à la fonction game du fichier game.py

# Logiciel de gestion de version utilisé: GIT
# Dépôt distant: BitBucket.org
# Membres du groupe:
- NDIAYE Deffa
- NDIAYE Mohameth El Bachir