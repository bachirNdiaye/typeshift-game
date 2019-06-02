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
			return str(i)

def rightClick(event):
	global actualScore

	if ( (event.x >= startX and event.x <= startX+(level*letterBlockSize)) ):
		moveColumn(whosClicked(event.x - startX), "down")

def leftClick(event):
	global actualScore

	if ( (event.x >= startX and event.x <= startX+(level*letterBlockSize)) ):
		moveColumn(whosClicked(event.x - startX), "up")

def grid():
	"""
	Crée la grille, les boutons et place les lettres
	"""
	global maxScore

	window.title("TypeShift")
	window.configure(bg = windowColor)
	
	canvas.configure(bg = gridContainerColor)
	canvas.pack()
	canvas.bind("<Button-1>", leftClick)
	#Button-2 and Button-3 for right and middle click, il also allows to use right click on mac and windows because 2 works on mac
	#but not on windows and 3 works on windows but not on mac
	canvas.bind("<Button-2>", rightClick)
	canvas.bind("<Button-3>", rightClick)

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
	
	print("Solveur")
	print(solveur())
	
	#scoreWidget = canvas.create_text(windowSize - 50, 0, text="0/"+str(maxScore), fill="#fff")
	scoreWidgetText.set("Score: "+ str(actualScore) +" / "+str(maxScore))
	scoreWidget = Label(window, textvariable = scoreWidgetText)
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	
	btnQuitGame.pack(side = RIGHT)
	scoreWidget.pack(side = LEFT)

def actualWord(node):
	if node["next"]:
		return node["letter"]["letter"]+actualWord(node["next"])
	else:
		return node["letter"]["letter"]

def colorizeFoundLetters(node):
	global actualScore

	alreadyFound = node["letter"]["found"]
	
	if not alreadyFound:
		rect = node["letter"]["rectAndText"][0]
		node["letter"]["found"] = True
		actualScore+=1
		scoreWidgetText.set("Score: "+ str(actualScore) +" / "+str(maxScore))
		canvas.itemconfigure(rect, fill=onCenterLineFoundLetterBlockColor)
	
	if node["next"] is not None:
		colorizeFoundLetters(node["next"])

def end():
	canvas.destroy()
	winMessage = Label(window, text = "Puzzle Trouvé !", fg="#fff", bg=windowColor, font=("Arial", 50))
	winMessage.pack(side = TOP, padx = gridContainerSize // 2)

	expectedWordsMessage = Label(window, text = "Mots Prévus: "+", ".join(words), fg="#fff", bg=windowColor, font=("Arial", 14))
	foundWordsMessage = Label(window, text = "Mots trouvés: "+", ".join(foundWords), fg="yellow", bg=windowColor, font=("Arial", 14))
	additionalFoundWordsMessage = Label(window, text = "Mots additionnels: "+", ".join(additionalFoundWords), fg="yellow", bg=windowColor, font=("Arial", 14))

	expectedWordsMessage.pack(side = TOP)
	foundWordsMessage.pack(side = TOP)
	additionalFoundWordsMessage.pack(side = TOP)

def checkWord():
	global actualScore
	
	word = actualWord(centerLineList["head"])

	if (word in words) and (word not in foundWords):
		foundWords.append(word)
		colorizeFoundLetters(centerLineList["head"])
	elif (word in allWordsOfThisLevel) and (word not in additionalFoundWords):
		additionalFoundWords.append(word)
		colorizeFoundLetters(centerLineList["head"])

	if (actualScore == maxScore): end()

#La colonne cliquée correspond au nombre d'iterations à faire avant d'arrêter la fonction récursive
def updateCenterLineList(nodeToInsert, iterations, actualNode):
	if iterations == 0:
		actualNode["letter"] = nodeToInsert
	else:
		updateCenterLineList(nodeToInsert, iterations-1, actualNode["next"])

def moveColumn(cliquedColumn, direction):
	# On met la valeur à soustraire pour le déplacement dans le tableau afin de le recuperer via les clés (correspondant à direction passé en paramètre ) au lieu de faire un if..else et de répéter deux fois le même code
	columnLength = len(columns["column"+cliquedColumn])

	sortedColumnKeys = list(columns["column"+cliquedColumn].keys())
	sortedColumnKeys.sort()

	centerLinePos = expectedWords // 2
	lastKey = sortedColumnKeys[len(sortedColumnKeys) - 1]
	
	if ((columns["column"+cliquedColumn][sortedColumnKeys[0]]["posY"] != centerLinePos) and (direction == "down")) or ((columns["column"+cliquedColumn][lastKey]["posY"] != centerLinePos) and (direction == "up")):
		d = {"up": letterBlockSize, "down": -letterBlockSize}
		newPosY = 0

		#letterPositions = []
		for key in columns["column"+cliquedColumn]:
			#letterPositions.append(int(key[len(key)-1]))
			rect = columns["column"+cliquedColumn][key]["rectAndText"][0]
			rectCoords = canvas.coords(rect)

			text = columns["column"+cliquedColumn][key]["rectAndText"][1]
			textCoords = canvas.coords(text)

			canvas.coords(rect, rectCoords[0], rectCoords[1] - d[direction], rectCoords[2], rectCoords[3] - d[direction])
			canvas.coords(text, textCoords[0], textCoords[1] - d[direction])

			newPosY = columns["column"+cliquedColumn][key]["posY"] - 1 if direction == "up" else columns["column"+cliquedColumn][key]["posY"] + 1

			columns["column"+cliquedColumn][key]["posY"] = newPosY

			if not columns["column"+cliquedColumn][key]["found"]:
				canvas.itemconfigure(rect, fill=letterBlockColor)

				if newPosY == centerLinePos:
					canvas.itemconfigure(rect, fill=onCenterLineLetterBlockColor)
					updateCenterLineList(columns["column"+cliquedColumn][key], int(cliquedColumn), centerLineList["head"])
			else:
				canvas.itemconfigure(rect, fill=foundLetterBlockColor)

				if newPosY == centerLinePos:
					canvas.itemconfigure(rect, fill=onCenterLineFoundLetterBlockColor)
					updateCenterLineList(columns["column"+cliquedColumn][key], int(cliquedColumn), centerLineList["head"])
	checkWord()

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

def solveur():
	"""
	On cree le cas fixe 5 mots de 4 lettres
	Les memes variables precedé pas le S de solveur pour les differencier
	"""

	SWords = ['pers', 'dito', 'soja', 'rapt', 'alle']
	SAllWordsOfThisLevel = ["jale", "teta", "fila", "paya", "itou", "beer", "mail", "peau", "fera", "aide", "neon", "fane", "pref", "jars","elfe"]

	SColumns = {
		'column0': {
			'letter2': {
				'letter': 's',
				'posX': 0,
				'posY': 2,
				'found': False,
				'rectAndText': (2, 3)
			},
			'letter3': {
				'letter': 'd',
				'posX': 0,
				'posY': 3,
				'found': False,
				'rectAndText': (4, 5)
			},
			'letter1': {
				'letter': 'a',
				'posX': 0,
				'posY': 1,
				'found': False,
				'rectAndText': (6, 7)
			},
			'letter4': {
				'letter': 'r',
				'posX': 0,
				'posY': 4,
				'found': False,
				'rectAndText': (8, 9)
			},
			'letter0': {
				'letter': 'p',
				'posX': 0,
				'posY': 0,
				'found': False,
				'rectAndText': (10, 11)
			}
		},
		'column1': {
			'letter2': {
				'letter': 'a',
				'posX': 1,
				'posY': 2,
				'found': False,
				'rectAndText': (12, 13)
			},
			'letter3': {
				'letter': 'l',
				'posX': 1,
				'posY': 3,
				'found': False,
				'rectAndText': (14, 15)
			},
			'letter1': {
				'letter': 'i',
				'posX': 1,
				'posY': 1,
				'found': False,
				'rectAndText': (16, 17)
			},
			'letter4': {
				'letter': 'o',
				'posX': 1,
				'posY': 4,
				'found': False,
				'rectAndText': (18, 19)
			},
			'letter0': {
				'letter': 'e',
				'posX': 1,
				'posY': 0,
				'found': False,
				'rectAndText': (20, 21)
			}
		},
		'column2': {
			'letter2': {
				'letter': 'r',
				'posX': 2,
				'posY': 2,
				'found': False,
				'rectAndText': (22, 23)
			},
			'letter3': {
				'letter': 'p',
				'posX': 2,
				'posY': 3,
				'found': False,
				'rectAndText': (24, 25)
			},
			'letter1': {
				'letter': 'j',
				'posX': 2,
				'posY': 1,
				'found': False,
				'rectAndText': (26, 27)
			},
			'letter4': {
				'letter': 'l',
				'posX': 2,
				'posY': 4,
				'found': False,
				'rectAndText': (28, 29)
			},
			'letter0': {
				'letter': 't',
				'posX': 2,
				'posY': 0,
				'found': False,
				'rectAndText': (30, 31)
			}
		},
		'column3': {
			'letter2': {
				'letter': 't',
				'posX': 3,
				'posY': 2,
				'found': False,
				'rectAndText': (32, 33)
			},
			'letter3': {
				'letter': 's',
				'posX': 3,
				'posY': 3,
				'found': False,
				'rectAndText': (34, 35)
			},
			'letter1': {
				'letter': 'e',
				'posX': 3,
				'posY': 1,
				'found': False,
				'rectAndText': (36, 37)
			},
			'letter4': {
				'letter': 'a',
				'posX': 3,
				'posY': 4,
				'found': False,
				'rectAndText': (38, 39)
			},
			'letter0': {
				'letter': 'o',
				'posX': 3,
				'posY': 0,
				'found': False,
				'rectAndText': (40, 41)
			}
		}
	}
	SLevel = 4
	SExpectedWords = 5
	#start = ""
	end = ""
	wordToCheck = ""

	allWordsOfThisLevelWithExpectedWords = SWords + SAllWordsOfThisLevel

	foundWords = [] #Les mots trouvés par le solveur

	for i in range(SLevel):
		end+=str(len(SColumns["column"+str(i)]))

	tabIterations = list(map(int, list(end)))

	for i1 in range(0, tabIterations[0]):
		for i2 in range(0, tabIterations[1]):
			for i3 in range(0, tabIterations[2]):
				for i4 in range(0, tabIterations[3]):
					wordToCheck = SColumns["column0"]["letter"+str(i1)]["letter"] + SColumns["column1"]["letter"+str(i2)]["letter"] + SColumns["column2"]["letter"+str(i3)]["letter"] + SColumns["column3"]["letter"+str(i4)]["letter"]

					if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
						foundWords.append(wordToCheck)
						allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	print("End: "+ end)
	print("tabIterations: ")
	print(tabIterations)
	print("Found Words (Solveur): ")
	print(foundWords)

def quitGame():
	window.destroy()