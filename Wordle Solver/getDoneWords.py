

doneWords = open("doneWords.txt", encoding="UTF-8").read()
doneWords = doneWords.split(" ")
doneWords = [word.lower() for word in doneWords]

doneWords.append("sauna")

doneWords = sorted(list(set(doneWords)))


with open("doneWords.py", "w") as file:
	file.write(f"doneWords = {doneWords}\n")
