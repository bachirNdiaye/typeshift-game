"""
Ce fichier contient les variables globales qui seront utilisés dans le jeu
"""
from random import randint

level = randint(3, 10)
expectedWords = randint(3, 5) #Le nombre prévu à trouver (correspond aussi au nombre de lignes), mais le joueur peut quand meme en trouver d'autres (Ils seront dans les mots additionels trouvés)
allWordsOfThisLevel = []
words = []
maxScore = level*expectedWords #Le nombre de points total à avoir
additionalFoundWords = [] #Si le joueur trouve des mots en plus de ceux qui avaient étés prévus, ils seront ici