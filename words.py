"""
Contient la fonction qui charge mots qui seront sur la grille
"""
from globals import *

def loadWords():
	"""
	Charge les mots depuis le fichier dictionary.json
	en fonction du niveau du jeu
	(Niveau 3 = 3lettres, Niveau 4 = 4 lettres etc.)
	"""
	global level, words, allWordsOfThisLevel, expectedWords, gridSize

	print(level.get())

	with open('dictionary.json') as dictionaryFile:
		allWordsOfThisLevel = json.load(dictionaryFile)[level.get()]

		for i in range(expectedWords):
			words.append(allWordsOfThisLevel.pop(randint(0, len(allWordsOfThisLevel)-1)))
	print(words)