import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "top gun", "views": 500, "likes": 10},
    {"name": "rest api", "views": 80000, "likes": 444},
    {"name": "machine learning", "views": 777, "likes": 10000},
]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())
# input()

# for i in range(0, 3, 1):
#     response = requests.get(BASE + "video/" + str(i))
#     print(response.json())

response = requests.delete(BASE + "video/0")
print(response)
input()

# response = requests.get(BASE + "video/6")
# print(response.json())

response = requests.patch(BASE + "video/2", {"views": 99})
print(response.json())