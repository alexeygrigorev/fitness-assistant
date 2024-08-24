import pandas as pd

import requests

df = pd.read_csv("./data/ground-truth-retrieval.csv")
question = df.sample(n=1).iloc[0]['question']

print("question: ", question)

url = "http://localhost:5000/question"


data = {"question": question}

response = requests.post(url, json=data)
# print(response.content)

print(response.json())