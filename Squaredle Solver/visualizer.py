from grid import Grid

# grid = Grid("lnsahbuhdsruawtetdrionoei", 6)
# grid.findAllWords()
# print(grid.words)
# print()

grid = Grid("noozetitdhusbreh")
print(len(grid.letters), grid.gridSize)
print(grid.findAllWords())
print()


def prettyPrint(wordStrand):
	print(wordStrand.word)
	print()
	for row in range(grid.gridSize):
		rowstr = ""
		included = False
		for index in range(row * grid.gridSize, (row + 1) * grid.gridSize):
			if index in wordStrand.indexes:
				rowstr += f"{grid.letters[index]} "
				included = True
			else:
				rowstr += "  "
		if included:
			print(rowstr)
	print()


for word in grid.words:
	prettyPrint(word)