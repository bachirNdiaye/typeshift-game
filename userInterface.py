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
	#global window

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

	startX = (gridContainerSize // 2) - ((level * letterBlockSize) // 2)
	startY = centerLinePosY - (letterBlockSize * (expectedWords // 2))

	#canvas.create_text(10, centerLinePosY, text = "A", justify = "center", fill = "#fff", width = letterBlockSize, stipple="gray25")

	#a = textWidget(centerLinePosX, centerLinePosY, "A", canvas)
	#print(a[0])
	#print(a[1])

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
				positionY = letterPositions.pop(math.floor(len(letterPositions)//2))#choice([k for k in range(expectedWords) if k not in notAvailablePositions])
				
				letter = words[wordToChoosePosition][i]

				alreadyPositionedLetters.append(letter)

				columns["column"+str(i)]["letter"+str(positionY)] = {
					"letter": letter,
					"posX": i,
					"posY": positionY,
					"found": False,
					"rectAndText": textWidget(
										startX + (i * letterBlockSize),
										startY + ((positionY * letterBlockSize)),# - (letterBlockSize // 2),
										letter.upper(),
										canvas
									)
					#"next": None
				}
		
		#print(notAvailablePositions)
		
	#print(columns)
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame.pack(side = LEFT)

def checkWord():
	pass

def moveColumn():
	pass

def textWidget(x, y, text, canvas):
	"""Permet de créer un carré avec un texte à l'interieur"""
	
	rect = canvas.create_rectangle(x, y, (x + letterBlockSize), (y + letterBlockSize), fill = letterBlockColor, outline = windowColor)
	text = canvas.create_text(
		x + (letterBlockSize // 2),
		y + (letterBlockSize // 2),
		text = text,
		font = ("Arial", letterBlockSize - (letterBlockSize // 6)),
		fill = "#fff"
	)
	return rect, text



def quitGame():
	window.destroy()