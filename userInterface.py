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
	for i in range(level.get()):
		if x >= i*letterBlockSize and x <= (i+1)*letterBlockSize:
			return str(i)

def rightClick(event):
	global actualScore

	if ( (event.x >= startX.get() and event.x <= startX.get()+(level.get()*letterBlockSize)) ):
		moveColumn(whosClicked(event.x - startX.get()), "down")

def leftClick(event):
	global actualScore

	if ( (event.x >= startX.get() and event.x <= startX.get()+(level.get()*letterBlockSize)) ):
		moveColumn(whosClicked(event.x - startX.get()), "up")

def grid():
	"""
	Crée la grille, les boutons et place les lettres
	"""
	global maxScore

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

	#Là ou on commence à dessiner la grille (C'est pour permettre de centrer la grille)
	startX.set((gridContainerSize // 2) - ((level.get() * letterBlockSize) // 2))
	startY.set(centerLinePosY - (letterBlockSize * (expectedWords // 2)))

	for i in range(level.get()):

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
										startX.get() + (i * letterBlockSize),
										startY.get() + ((positionY * letterBlockSize)),
										letter.upper(),
										canvas,
										getBlockColor(positionY, False, startX.get(), startY.get())
									)
				}

				if positionY == expectedWords//2: #Si la lettre est dans la ligne du centre, on l'ajoute dans la liste chaînée centerLineList
					addToCenterLineList(i, positionY, centerLineList["head"])

		maxScore += len(alreadyPositionedLetters) #On charge le score maximum
	
	#scoreWidget = canvas.create_text(windowSize - 50, 0, text="0/"+str(maxScore), fill="#fff")
	scoreWidgetText.set("Score: "+ str(actualScore) +" / "+str(maxScore))
	scoreWidget = Label(window, textvariable = scoreWidgetText)
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnQuitGame = Button(window, text = "Quitter le jeu", command = quitGame)
	btnAfficheResultatSolveur = Button(window, text = "Solveur", command = printSolver)
	
	btnQuitGame.pack(side = RIGHT)
	scoreWidget.pack(side = LEFT)
	btnAfficheResultatSolveur.pack(side = BOTTOM, padx=gridContainerSize//2)

def getLevelAndLauchGame(event):
	for i in range(len(levelsWidget)):
		actualWidgetCoords = canvas.coords(levelsWidget[i])

		if event.x >= actualWidgetCoords[0] and event.x <= actualWidgetCoords[2]:
			level.set(i+minLetters)
			loadWords()
			canvas.delete(ALL)
			grid()
			break

def chooseLevel():
	canvas.create_text(
		gridContainerSize // 2,
		gridContainerSize // 3,
		text = "Choisissez un niveau",
		font = ("Arial", 40),
		fill = "#fff"
	)

	widgetRank = 0
	levelChoiceStartX = (gridContainerSize - (letterBlockSize * (maxLetters+1 - minLetters))) // 2

	y = gridContainerSize // 2 #Le y ne varie pas, pas besoin de le mettre dans la boucle et de recalculer à chaque fois
	for i in range(minLetters, maxLetters+1):
		x = levelChoiceStartX + (widgetRank*letterBlockSize)

		levelsWidget.append(textWidget(x, y, i, canvas, fill=onCenterLineFoundLetterBlockColor)[0])
		widgetRank += 1

	canvas.bind("<Button-1>", getLevelAndLauchGame)

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

	if (actualScore == maxScore):
		end()

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

def solver():
	"""
	Nous avons mis le solveur pour tous les niveaux au lieu du cas fixe, le solveur resout la partie en cours. Le cas varie en fonction du choix du niveau
	"""
	tmpsDeb = time.clock() #Pour mesurer le temps d'execution

	wordToCheck = "" #On y met une combinaison de lettre avant de verifier que c'est un mot

	allWordsOfThisLevelWithExpectedWords = words + allWordsOfThisLevel

	foundWords = [] #Les mots trouvés par le solveur
	
	tabIterations = list(list(map(int, list(k.replace("letter", "") for k in list(columns[column].keys())))) for column in columns)

	for t in tabIterations:
		t.sort()
	
	"""
	On met les boucles dans les if..else pour etre sur de faire qu'un seul test + le nombre d'iteration necessaire
	C'est mieux que de faire plusieus itérations et des tests (if..else) pour chaque itérations
	...
	On a préferé utiliser plusieurs if..else (correspondant aux niveaux possibles) au lieu d'une fonction récursive
	pour optimiser le temps, car la fonction récursive consommerai plus
	"""
	if level.get() == 3: #Solveur niveau 3
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"]

					if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
						foundWords.append(wordToCheck)
						allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)
	
	elif level.get() == 4: #Solveur niveau 4
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"]

						if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
							foundWords.append(wordToCheck)
							allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 5: #Solveur niveau 5
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"]

							if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
								foundWords.append(wordToCheck)
								allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 6: #Solveur niveau 6
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							for i6 in tabIterations[5]:
								wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"] + columns["column5"]["letter"+str(i6)]["letter"]

								if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
									foundWords.append(wordToCheck)
									allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 7: #Solveur niveau 7
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							for i6 in tabIterations[5]:
								for i7 in tabIterations[6]:
									wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"] + columns["column5"]["letter"+str(i6)]["letter"] + columns["column6"]["letter"+str(i7)]["letter"]

									if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
										foundWords.append(wordToCheck)
										allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 8: #Solveur niveau 8
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							for i6 in tabIterations[5]:
								for i7 in tabIterations[6]:
									for i8 in tabIterations[7]:
										wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"] + columns["column5"]["letter"+str(i6)]["letter"] + columns["column6"]["letter"+str(i7)]["letter"] + columns["column7"]["letter"+str(i8)]["letter"]

										if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
											foundWords.append(wordToCheck)
											allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 9: #Solveur niveau 9
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							for i6 in tabIterations[5]:
								for i7 in tabIterations[6]:
									for i8 in tabIterations[7]:
										for i9 in tabIterations[8]:
											wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"] + columns["column5"]["letter"+str(i6)]["letter"] + columns["column6"]["letter"+str(i7)]["letter"] + columns["column7"]["letter"+str(i8)]["letter"] + columns["column8"]["letter"+str(i9)]["letter"]

											if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
												foundWords.append(wordToCheck)
												allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	elif level.get() == 10: #Solveur niveau 10
		for i1 in tabIterations[0]:
			for i2 in tabIterations[1]:
				for i3 in tabIterations[2]:
					for i4 in tabIterations[3]:
						for i5 in tabIterations[4]:
							for i6 in tabIterations[5]:
								for i7 in tabIterations[6]:
									for i8 in tabIterations[7]:
										for i9 in tabIterations[8]:
											for i10 in tabIterations[9]:
												wordToCheck = columns["column0"]["letter"+str(i1)]["letter"] + columns["column1"]["letter"+str(i2)]["letter"] + columns["column2"]["letter"+str(i3)]["letter"] + columns["column3"]["letter"+str(i4)]["letter"] + columns["column4"]["letter"+str(i5)]["letter"] + columns["column5"]["letter"+str(i6)]["letter"] + columns["column6"]["letter"+str(i7)]["letter"] + columns["column7"]["letter"+str(i8)]["letter"] + columns["column8"]["letter"+str(i9)]["letter"] + columns["column9"]["letter"+str(i10)]["letter"]

												if (wordToCheck in allWordsOfThisLevelWithExpectedWords):
													foundWords.append(wordToCheck)
													allWordsOfThisLevelWithExpectedWords.remove(wordToCheck)

	#print("tabIterations: ")
	#print(tabIterations)
	#print("Found Words: ")
	tmpsFin = time.clock()

	return foundWords, tmpsFin - tmpsDeb

def printSolver():
	r = solver() #Le resultat du solveur
	rText = Label(window, text = "Solveur: \""+", ".join(r[0])+ "\" | Temps d'exec: "+str(r[1]), bg = windowColor, font=("Arial", 14), fg="#fff")

	rText.pack(side = BOTTOM)

def quitGame():
	window.destroy()