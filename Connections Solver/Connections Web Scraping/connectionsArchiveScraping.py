Remove this to run the code

from urllib.request import urlopen
from bs4 import BeautifulSoup

defaultURL = "https://connections.swellgarfo.com/nyt/"

difficulty = {"🟨": 0, "🟩": 1, "🟦": 2, "🟪": 3}

allPuzzles = []

for day in range(256):
	if (day + 1) % 10 == 0:
		print(f"Puzzle {day + 1} / {256}")

	url = defaultURL + str(day + 1)
	page = urlopen(url)
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html, "html.parser")

	targetCode = soup.find("script", id="__NEXT_DATA__", type="application/json")
	targetCode = targetCode.string.replace("true", "True").replace("false", "False")
	targetDict = eval(targetCode)
	targetDict = targetDict["props"]["pageProps"]["answers"]
	puzzle = [{category["description"]: category["words"]} for category in targetDict]

	allPuzzles.append(puzzle)

with open("connectionsArchive.py", "w") as file:
    file.write(f"allPuzzles = {allPuzzles}")

