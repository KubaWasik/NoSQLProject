from pymongo import MongoClient
from time import perf_counter
import math


print("timer start")
start = perf_counter()

client1 = MongoClient("10.100.100.1")
mydbMongo1 = client1['mydb1']

client2 = MongoClient("10.100.100.2")
mydbMongo2 = client2['mydb2']

print("Started fetching data from MongoDb 1")
fetchStart = perf_counter()
stringsMongo1 = mydbMongo1.strings

stringsMongo2 = mydbMongo2.strings
stringsMongo2.drop()
print("Collection droped - it's empyty")

result1 = stringsMongo1.find()
fetchEnd = perf_counter()
print("Ended fetching data, time elapsed: " + str(fetchEnd - fetchStart) + " s")
print("Creating list and inserting data to MongoDb 2")

stringList = [{"id": string["id"], "name": string["name"]} for string in result1]

count = len(stringList)
N = math.log10(count)

insertSum = 0

if N > 5:
    step = int(10 ** (N - 5))
    for i in range(step):
        startSlice = (10 ** 5) * i
        stopSlice = (10 ** 5) * (i + 1)
        result = stringsMongo2.insert_many(stringList[startSlice:stopSlice])
        print("step " + str(i + 1) + " done")
        insertSum += len(result.inserted_ids)
else:
  result = stringsMongo2.insert_many(stringList)
  insertSum += len(result.inserted_ids)

insertEnd = perf_counter()
print(str(insertSum) + " records inserted, elapsed time: " + str(insertEnd - fetchEnd) + " s")

stop = perf_counter()
print("timer stop")
print("Python execution time: " + str(stop - start) + " s")