"""
Gère ce qui touche à l'interface graphique:
	- Création de la grille
	- Positionnement des lettres
	- Déplacements
	- etc.
"""

from words import *

def grid():
	"""
	Crée la grille, les boutons et place les lettres
	"""
	global window

	window.title("TypeShift")
	canvas = Canvas(window, width = windowSize, height = windowSize)

	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame.pack(side = LEFT)
	pass

def checkWord():
	pass

def moveColumn():
	pass

def quitGame():
	window.destroy()