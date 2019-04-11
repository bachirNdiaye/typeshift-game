"""
Contient la fonction qui charge mots qui seront sur la grille
"""
from globals import *
import json

def loadWords():
	"""
	Charge les mots depuis le fichier dictionnary.json
	en fonction du niveau du jeu
	(Niveau 3 = 3lettres, Niveau 4 = 4 lettres etc.)
	"""
	global level, words, allWordsOfThisLevel, expectedWords

	with open('dictionnary.json') as dictionnaryFile:
		dictionnary = json.load(dictionnaryFile)
		allWordsOfThisLevel = dictionnary[level]

		for i in range(expectedWords):
			words.append(allWordsOfThisLevel.pop(randint(0, len(allWordsOfThisLevel)-1)))

	print("level")
	print(level)
	print("expectedWords")
	print(expectedWords)
	print("maxScore")
	print(maxScore)
	print("allWordsOfThisLevel")
	print(allWordsOfThisLevel)
	print("words")
	print(words)