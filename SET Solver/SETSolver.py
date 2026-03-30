from itertools import combinations

# solver for SET

# order: color, number, shape, fill
# colors: red (r), green (g), purple (p)
# numbers: 1, 2, 3
# shapes: diamond (d), oval (o), squiggly (s)
# fills: filled (f), lines (l), clear (c)


class Solver:
	def __init__(self, grid):
		self.grid = grid
		self.solutions = []


	def solve(self):
		if self.solutions:
			print("Already solved")
			return

		possibilities = combinations(grid, 3)

		for comb in possibilities:
			# print(comb)

			for i, j, k in zip(*comb):
				if not i == j == k and not len(set([i, j, k])) == 3:
					break

			else:
				self.solutions.append(comb)

		return self.solutions


	def getIndexes(self):
		readable = ""
		for comb in self.solutions:
			readable += ", ".join([f"row {grid.index(card) // 3 + 1} item {grid.index(card) % 3 + 1}" for card in comb]) + "\n"

		return readable


# order: color, number, shape, fill

grid = ["r2dl", "g1ol", "r1dl", "g2df", "r3of", "g3sl", "g2dl", "p3sl", "p1df", "g2ol", "r3sl", "g3dc"]
solver = Solver(grid)
print(solver.solve())
print(solver.getIndexes())





