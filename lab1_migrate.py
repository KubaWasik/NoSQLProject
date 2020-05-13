import mysql.connector
from pymongo import MongoClient
from time import perf_counter
import math


print("timer start")
start = perf_counter()

mydbMariaDb = mysql.connector.connect(
  host="10.100.100.2",
  user="root",
  passwd="root",
  database="mydb"
)

mycursor = mydbMariaDb.cursor()
mycursor.execute("SELECT * FROM strings")

print("Started fetching data from MariaDb")
fetchStart = perf_counter()
stringsMariaDb = mycursor.fetchall()
fetchEnd = perf_counter()

print("Ended fetching data, time elapsed: " + str(fetchEnd - fetchStart) + " s")
print("Creating list and inserting data to MongoDb")

client = MongoClient("10.100.100.1")
mydbMongo = client['mydb']
stringsMongoDb = mydbMongo.strings
stringsMongoDb.drop()
print("Collection droped - it's empyty")

stringList = [{"id": string[0], "name": string[1]} for string in stringsMariaDb]

count = len(stringList)
N = math.log10(count)

insertSum = 0

if N > 5:
    step = int(10 ** (N - 5))
    for i in range(step):
        startSlice = (10 ** 5) * i
        stopSlice = (10 ** 5) * (i + 1)
        result = stringsMongoDb.insert_many(stringList[startSlice:stopSlice])
        print("step " + str(i + 1) + " done")
        insertSum += len(result.inserted_ids)
else:
  result = stringsMongoDb.insert_many(stringList)
  insertSum += len(result.inserted_ids)

insertEnd = perf_counter()
print(str(insertSum) + " records inserted, elapsed time: " + str(insertEnd - fetchEnd) + " s")

stop = perf_counter()
print("timer stop")
print("Python execution time: " + str(stop - start) + " s")