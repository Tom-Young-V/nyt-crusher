import re



words = open("extensiveWords.txt", encoding="UTF-8").read()
words = words.split("\n")






for word in [word for word in words if re.search(r"a[a-z]{4}", word)]:
	print(word)