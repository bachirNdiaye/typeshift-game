"""
Contient la fonction qui appele les fonctions qui permettent de jouer au jeu
"""
from userInterface import *

def game():
	"""
	Appele dans l'ordre toutes les fonctions
	permettant de jouer au jeu
	"""
	chooseLevel()
	window.mainloop()