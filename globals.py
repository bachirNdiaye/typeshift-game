"""
Ce fichier contient les variables globales qui seront utilisés dans le jeu
"""
from random import randint
import json

level = randint(3, 10)
expectedWords = 3 if randint(0,1) else 5 #Le nombre prévu à trouver (correspond aussi au nombre de lignes), mais le joueur peut quand meme en trouver d'autres (Ils seront dans les mots additionels trouvés). Ici on choisi aléatoirement 3 ou 5 lignes et mots prévus
allWordsOfThisLevel = []
words = []
maxScore = level*expectedWords #Le nombre de points total à avoir
additionalFoundWords = [] #Si le joueur trouve des mots en plus de ceux qui avaient étés prévus, ils seront ici

with open("config.json") as configFile:
	config = json.load(configFile)
	gridContainerSize = config["gridContainerSize"]