from pymongo import MongoClient
from random import choice
from time import perf_counter


print("timer start")
start = perf_counter()

client = MongoClient("10.100.100.1")
mydbMongo = client['mydb1']
stringsMongo = mydbMongo.strings

stringsCopy = mydbMongo.stringsCopy
stringsCopy.drop()
print("Collection droped - it's empyty")

print("Started fetching data from MongoDb 1")
fetchStart = perf_counter()
result1 = stringsMongo.find()
fetchEnd = perf_counter()
print("Ended fetching data, time elapsed: " + str(fetchEnd - fetchStart) + " s")
print("Creating list and inserting data to MongoDb 2")

i = 0
count = stringsMongo.count_documents({})
resultList = [item for item in result1]

print("List created")

while i < count:
    randomString = choice(resultList)
    result = stringsCopy.find_one({'name': randomString['name']})
    if type(result) == type(None):
        stringsCopy.insert_one({'id': randomString['id'], 'name': randomString['name']})
        i += 1

stop = perf_counter()
print("timer stop")

print("Python execution time: " + str(stop - start) + " s")