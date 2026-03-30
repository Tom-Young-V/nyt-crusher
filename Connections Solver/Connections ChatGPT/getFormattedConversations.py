import json
from connectionsArchive import allPuzzles  # wont work
from random import shuffle

def getCards(puzzle, randomize = True):
	cards = [value for category in puzzle for values in category.values() for value in values]
	if randomize:
		shuffle(cards)
	return cards

formattedConversations = []

for puzzle in allPuzzles:
	data = {"messages": [{"role": "system", "content": "You are a puzzle solving chatbot that solves a sorting game, of putting 16 different words into 4 categories of 4 words with some common relevance"}, 
		{"role": "user", "content": f"{getCards(puzzle)}"}, {"role": "assistant", "content": f"{puzzle}"}]}

	jsonData = json.dumps(data, default=str)
	formattedConversations.append(jsonData)

for line in formattedConversations:
	print(line)
