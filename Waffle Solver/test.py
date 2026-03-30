import re
from words import deluxeWords, words, weird


# words = open("test.txt", encoding="UTF-8").read()
# words = words.split("\n")

# all7LetterWords = [word.lower() for word in words if len(word) == 7 and word.isalpha() and word.lower() not in deluxeWords]

# # print(sorted(all7LetterWords))

# deluxeWords.extend(all7LetterWords)

# print(sorted(deluxeWords))

# with open("allDeluxeWords.txt", 'w') as file:
#     # Write each word followed by a newline character
#     for word in deluxeWords:
#         file.write(word + '\n')

text = open("allWords.txt", encoding="UTF-8").read()
lines = text.split("\n")


for word in lines:
	if "b" in word and "i" in word and "a" in word and "e" in word and word[0] == "b":
		print(word)