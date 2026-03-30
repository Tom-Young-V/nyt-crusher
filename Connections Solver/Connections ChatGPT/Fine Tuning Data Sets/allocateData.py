import json
import random

dataFile = "formattedConversations.jsonl"

# Load the dataset
with open(dataFile, 'r', encoding='utf-8') as f:
	dataSet = [json.loads(line) for line in f]

smallDataSet = random.sample(dataSet, 100)

for conversation in smallDataSet:
	print(json.dumps(conversation, default=str))