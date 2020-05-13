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

count = len(stringsList)
insertSum = 0

if N > 5:
    step = int(10 ** (N - 5))
    for i in range(step):
        startSlice = (10 ** 5) * i
        stopSlice = (10 ** 5) * (i + 1)
        result = stringsMongo.insert_many(stringsList[startSlice:stopSlice])
        print("step " + str(i + 1) + " done")
        insertSum += len(result.inserted_ids)
else:
  result = stringsMongo.insert_many(stringsList)
  insertSum += len(result.inserted_ids)

print("-------------------------")

stop = perf_counter()
print("timer stop")

print(str(insertSum) + " records inserted.")
print("Python execution time: " + str(stop - start) + " s")