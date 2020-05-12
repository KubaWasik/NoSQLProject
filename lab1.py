import mysql.connector
from pymongo import MongoClient
from time import perf_counter


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

stringList = [{"id": string[0], "name": string[1]} for string in stringsMariaDb]
result = stringsMongoDb.insert_many(stringList)

insertEnd = perf_counter()
print(str(len(result.inserted_ids)) + " records inserted, elapsed time: " + str(insertEnd - fetchEnd) + " s")

stop = perf_counter()
print("timer stop")
print("Python execution time: " + str(stop - start) + " s")