"""
Ce fichier contient les variables globales qui seront utilisés dans le jeu
"""

from tkinter import *
from random import randint, choice
import json

level = randint(3, 10)
expectedWords = 3 if randint(0,1) else 5 #Le nombre prévu à trouver (correspond aussi au nombre de lignes), mais le joueur peut quand meme en trouver d'autres (Ils seront dans les mots additionels trouvés). Ici on choisi aléatoirement 3 ou 5 lignes et mots prévus
allWordsOfThisLevel = []
words = []
maxScore = 0 #On le modifiera plus tard
additionalFoundWords = [] #Si le joueur trouve des mots en plus de ceux qui avaient étés prévus, ils seront ici
columns = {} #Correspond aux colonnes du jeu
centerLineList = { #Une liste chainée correspondant à la ligne du centre, un mot est trouvé si tous les noeuds de la liste forment un mot
	"head": None
}
window = Tk()

with open("config.json") as configFile:
	config = json.load(configFile)

	gridContainerSize					= config["gridContainerSize"]
	windowSize							= config["windowSize"]
	letterBlockSize						= config["letterBlockSize"]
	windowColor							= config["windowColor"]
	gridContainerColor					= config["gridContainerColor"]
	centerLineColor						= config["centerLineColor"]
	letterBlockColor					= config["letterBlockColor"]
	foundLetterBlockColor				= config["foundLetterBlockColor"]
	onCenterLineFoundLetterBlockColor	= config["onCenterLineFoundLetterBlockColor"]
	onCenterLineLetterBlockColor		= config["onCenterLineLetterBlockColor"]

centerLinePosX = 0
centerLinePosY = (gridContainerSize // 2 - letterBlockSize // 2)