from openai import OpenAI

# Data should be: 60-80% training data, 10-20% validation data, and 10-20% test data

def getGPTSuggestions(puzzle, amountGuesses):
	completion = client.chat.completions.create(
		model="gpt-4-0613",  # gpt-4-0125-preview
		messages=[
			{"role": "system", "content": 
"""
You are a puzze-solving bot. The puzzle at hand is a game called Connections, where you are given 16, 12, 8, or 4 words, and you have to group the
words into 4 groups of 4. Each group has some sort of common relevance. Here are some category examples:
FISH: Bass, Flounder, Salmon, Trout
FIRE ___: Ant, Drill, Island, Opal
Categories will always be more specific than "5-LETTER-WORDS," "NAMES" or "VERBS."
The categories can become very out of the box, so be very creative.
"""
			},
			{"role": "user", "content": 
f"""
Here are todays words: {puzzle}. I want you to make {amountGuesses} guesses of possible categories.
ONLY RESPOND with only a brief category name (i.e: FISH, or FIRE ___ in the given example), the 4 words that align with the category, 
and a percent value of your confidence that the category is correct. The categories can overlap words as much or as little as necessary.
Do not respond with anything more. Here is what each category suggestion should look like:
Category Description - [Word1, ...] - Percent confidence value
"""
			}
		]
	)
	return completion.choices[0].message.content





