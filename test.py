import requests

url = "http://localhost:5000/question"

question = (
    "Is the Lat Pulldown considered a strength training activity, and if so, why?"
)
data = {"question": question}

response = requests.post(url, json=data)
# print(response.content)

print(response.json())