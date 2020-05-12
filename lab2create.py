from pymongo import MongoClient
from random import choice
from time import perf_counter
from string import ascii_uppercase, digits


def id_generator(size=20, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

N = int(input("Enter N value: "))

print("timer start")
start = perf_counter()

client = MongoClient("10.100.100.1")
mydbMongo = client['mydb1']
stringsMongo = mydbMongo.strings

stringsMongo.drop()
print("Collection droped - it's empyty")

randomDict = {}

while len(randomDict) < (10 ** N):
    randomDict[id_generator()] = 1

print("Strings generated")

i = 0
items = []
for elem in randomDict:
    items.append((i, elem))
    i += 1

print("List created")

stringsList = [{"id": i[0], "name": i[1]} for i in items]

result = stringsMongo.insert_many(stringsList)

print("-------------------------")

stop = perf_counter()
print("timer stop")

print(str(len(result.inserted_ids)) + " records inserted.")
print("Python execution time: " + str(stop - start) + " s")