import sys
sys.path.append("./Connections Web Scraping")
from connectionsDailyScraping import getDailyPuzzle
sys.path.append("./Connections ChatGPT")
from chatGPTRequests import getGPTSuggestions

todaysPuzzle = getDailyPuzzle()
print(todaysPuzzle)

class ConnectionsSolver():
	def __init__(self, puzzle):
		self.puzzle = puzzle

print(getGPTSuggestions(todaysPuzzle, 10))








