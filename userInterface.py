"""
Gère ce qui touche à l'interface graphique:
	- Création de la grille
	- Positionnement des lettres
	- Déplacements
	- etc.
"""

import math
from words import *

def whosClicked(x):
	for i in range(level):
		if x >= i*letterBlockSize and x <= (i+1)*letterBlockSize:
			return i+1

def rightClick(event):
	print("Clique droit")
	if ( (event.x >= startX and event.x <= startX+(level*letterBlockSize)) and (event.y >= startY and event.y <= startY+(expectedWords*letterBlockSize)) ):
		#print("La colonne cliquée est: "+str(whosClicked(event.x - startX)))
		moveColumn(whosClicked(event.x - startX))

def leftClick(event):
	print("Clique gauche")
	if ( (event.x >= startX and event.x <= startX+(level*letterBlockSize)) and (event.y >= startY and event.y <= startY+(expectedWords*letterBlockSize)) ):
		#print("La colonne cliquée est: "+str(whosClicked(event.x - startX)))
		moveColumn(whosClicked(event.x - startX))

def grid():
	"""
	Crée la grille, les boutons et place les lettres
	"""
	global maxScore

	window.title("TypeShift")
	window.configure(bg = windowColor)
	
	canvas = Canvas(window, width = gridContainerSize, height = gridContainerSize)
	canvas.configure(bg = gridContainerColor)
	canvas.pack()
	canvas.bind("<Button-1>", leftClick)
	canvas.bind("<Button-2>", rightClick)

	#Le background de la ligne du centre
	canvas.create_rectangle(
		centerLinePosX,
		centerLinePosY,
		gridContainerSize,
		(centerLinePosY + letterBlockSize),
		fill = centerLineColor,
		outline = ""
	)

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
				positionY = letterPositions.pop(len(letterPositions)//2)
				
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

				if positionY == expectedWords//2: #Si la lettre est dans la ligne du centre, on l'ajoute dans la liste chaînée centerLineList
					addToCenterLineList(i, positionY, centerLineList["head"])

		maxScore += len(alreadyPositionedLetters) #On charge le score maximum
	
	#A enlever
	print(maxScore, words, centerLineList)
	print("Actual word is")
	checkWord()
	
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame.pack(side = LEFT)

def actualWord(node):
	if node["next"]:
		return node["letter"]["letter"]+actualWord(node["next"])
	else:
		return node["letter"]["letter"]

def checkWord():
	word = actualWord(centerLineList["head"])
	print(word)

	if word in words:
		print("Mot trouvé")
	elif word in allWordsOfThisLevel:
		additionalFoundWords.append(word)
		print("Mot trouvé")
	else:
		print("Mot non trouvé")

def moveColumn(cliquedColumn):
	pass

def addToCenterLineList(columnIndice, letterYPosition, actualNode):
	""""""
	if not centerLineList["head"]: #S'il ne contient rien
		centerLineList["head"] = {
			"letter": columns["column"+str(columnIndice)]["letter"+str(letterYPosition)],
			"next": None
		}
	else:
		if not actualNode["next"]: #S'il ne contient rien
			actualNode["next"] = {
				"letter": columns["column"+str(columnIndice)]["letter"+str(letterYPosition)],
				"next": None
			}
		else:
			addToCenterLineList(columnIndice, letterYPosition, actualNode["next"])

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
		return onCenterLineFoundLetterBlockColor if posY == expectedWords//2 else foundLetterBlockColor
	else:
		return onCenterLineLetterBlockColor if posY == expectedWords//2 else letterBlockColor


def quitGame():
	window.destroy()