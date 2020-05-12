import mysql.connector
from pymongo import MongoClient
from time import perf_counter
import random


print("timer start")
start = perf_counter()

mydb = mysql.connector.connect(
  host="10.100.100.2",
  user="root",
  passwd="root",
  database="mydb"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM strings")

print("Started fetching data from MariaDb")
fetchStart = perf_counter()
stringsTable1 = mycursor.fetchall()
fetchEnd = perf_counter()

print("Ended fetching data, time elapsed: " + str(fetchEnd - fetchStart) + " s")

try:
    mycursor.execute("CREATE TABLE strings_copy (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY(id))")
    print("Table 'strings_copy' created")
except:
    print("Table already exists")
    mycursor.execute("DROP TABLE strings_copy")
    print("Table droped")
    mycursor.execute("CREATE TABLE strings_copy (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY(id))")
    print("Table 'strings_copy' recreated")

mydb.commit()

mycursor.execute("SELECT COUNT(*) FROM strings")
stringsCount = mycursor.fetchall()[0][0]

sql = "INSERT INTO strings (name) VALUES (%s)"

i = 0

while i < stringsCount:
    randomString = random.choice(stringsTable1)[1]
    mycursor.execute("SELECT * FROM strings_copy WHERE name = '" + randomString + "'")
    result = mycursor.fetchall()
    if len(result) == 0:
        mycursor.execute("INSERT INTO strings_copy (name) VALUES ('" + randomString + "')")
        mydb.commit()
        i += 1

stop = perf_counter()
print("timer stop")

print("Python execution time: " + str(stop - start) + " s")