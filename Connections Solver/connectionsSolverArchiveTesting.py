import sys
sys.path.append('./Connections Web Scraping')
from connectionsArchive import allPuzzles

def getCards(puzzle, randomize = True):
	cards = [value for category in puzzle for values in category.values() for value in values]
	if randomize:
		shuffle(cards)
	return cards








