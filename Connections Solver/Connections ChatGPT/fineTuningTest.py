from openai import OpenAI
import os

filePath = os.path.join("Fine Tuning Data Sets", "superSmallDataSet.jsonl")
client.files.create(
	file=open(filePath, "rb"),
	purpose="fine-tune"
	)

# client.fine_tuning.jobs.create(
#   training_file="superSmallDataSet.jsonl", 
#   model="gpt-3.5-turbo"
# )




