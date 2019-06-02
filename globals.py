"""
Ce fichier contient les variables globales qui seront utilisés dans le jeu
"""

from tkinter import *
from random import randint, choice
import json

expectedWords = randint(3,5) #Le nombre prévu à trouver (correspond aussi au nombre de lignes), mais le joueur peut quand meme en trouver d'autres (Ils seront dans les mots additionels trouvés). Ici on choisi aléatoirement entre 3 et 5 lignes et mots prévus
allWordsOfThisLevel = []
words = []
actualScore = 0
maxScore = 0 #On le modifiera plus tard
foundWords = []
additionalFoundWords = [] #Si le joueur trouve des mots en plus de ceux qui avaient étés prévus, ils seront ici
columns = {} #Correspond aux colonnes du jeu
centerLineList = { #Une liste chainée correspondant à la ligne du centre, un mot est trouvé si tous les noeuds de la liste forment un mot
	"head": None
}
window = Tk()
window.title("TypeShift")

level = IntVar()
scoreWidgetText = StringVar()
startX = IntVar()
startY = IntVar()

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
	maxLetters 							= config["maxLetters"] #Le nombre de lettres maximum par mot du dictionnaire (A changer dans le fichier config.json)
	minLetters 							= config["minLetters"] #Le nombre de lettres minimum par mot du dictionnaire (A changer dans le fichier config.json)

window.configure(bg = windowColor)
canvas = Canvas(window, width = gridContainerSize, height = gridContainerSize)
canvas.configure(bg = gridContainerColor)
canvas.pack()

centerLinePosX = 0
centerLinePosY = (gridContainerSize // 2 - letterBlockSize // 2)

levelsWidget = [] #contient les widgets pour le choix du niveau