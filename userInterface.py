"""
Gère ce qui touche à l'interface graphique:
	- Création de la grille
	- Positionnement des lettres
	- Déplacements
	- etc.
"""

import math
from words import *

def grid():
	"""
	Crée la grille, les boutons et place les lettres
	"""

	window.title("TypeShift")
	window.configure(bg = windowColor)
	
	canvas = Canvas(window, width = gridContainerSize, height = gridContainerSize)
	canvas.configure(bg = gridContainerColor)
	canvas.pack()

	#Le background de la ligne du centre
	canvas.create_rectangle(
		centerLinePosX,
		centerLinePosY,
		gridContainerSize,
		(centerLinePosY + letterBlockSize),
		fill = centerLineColor,
		outline = ""
	)

	#Là ou on commence à dessiner la grille (C'est pour permettre de centrer la grille)
	startX = (gridContainerSize // 2) - ((level * letterBlockSize) // 2)
	startY = centerLinePosY - (letterBlockSize * (expectedWords // 2))

	for i in range(level):

		notAvailablePositions = []
		alreadyPositionedLetters = []
		letterPositions = []
		
		for x in range(expectedWords): letterPositions.append(x)

		columns["column"+str(i)] = {}

		for j in range(expectedWords):
			wordToChoosePosition = choice([k for k in range(expectedWords) if k not in notAvailablePositions])
			notAvailablePositions.append(wordToChoosePosition)

			if (words[wordToChoosePosition][i] not in alreadyPositionedLetters) :
				positionY = letterPositions.pop(math.floor(len(letterPositions)//2))
				
				letter = words[wordToChoosePosition][i]

				alreadyPositionedLetters.append(letter)

				columns["column"+str(i)]["letter"+str(positionY)] = {
					"letter": letter,
					"posX": i,
					"posY": positionY,
					"found": False,
					"rectAndText": textWidget(
										startX + (i * letterBlockSize),
										startY + ((positionY * letterBlockSize)),
										letter.upper(),
										canvas,
										getBlockColor(positionY, False, startX, startY)
									)
				}
		
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame.pack(side = LEFT)

def checkWord():
	pass

def moveColumn():
	pass

def textWidget(x, y, text, canvas, fill = letterBlockColor):
	"""Permet de créer un carré avec un texte à l'interieur"""
	
	rect = canvas.create_rectangle(x, y, (x + letterBlockSize), (y + letterBlockSize), fill = fill, outline = windowColor)
	text = canvas.create_text(
		x + (letterBlockSize // 2),
		y + (letterBlockSize // 2),
		text = text,
		font = ("Arial", letterBlockSize - (letterBlockSize // 6)),
		fill = "#fff"
	)
	return rect, text

def getBlockColor(posY, found, startX, startY):
	if found:
		return onCenterLineFoundLetterBlockColor if (startY + (posY * letterBlockSize) == centerLinePosY and startY + (posY * letterBlockSize) + letterBlockSize == (centerLinePosY + letterBlockSize)) else foundLetterBlockColor
	else:
		return onCenterLineLetterBlockColor if (startY + (posY * letterBlockSize) == centerLinePosY and startY + (posY * letterBlockSize) + letterBlockSize == (centerLinePosY + letterBlockSize)) else letterBlockColor


def quitGame():
	window.destroy()