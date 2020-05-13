import mysql.connector
from random import choice
from time import perf_counter
from string import ascii_uppercase, digits


def id_generator(size=20, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

N = int(input("Enter N value: "))

print("timer start")
start = perf_counter()

try:
    mydb = mysql.connector.connect(
      host="10.100.100.2",
      user="root",
      passwd="root",
      database="mydb"
    )

    print("Database already exsists")
except:
    mydb = mysql.connector.connect(
      host="10.100.100.2",
      user="root",
      passwd="root"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE mydb")
    mydb.commit()
    mydb = mysql.connector.connect(
      host="10.100.100.2",
      user="root",
      passwd="root",
      database="mydb"
    )
    print("Database 'mydb' created")

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE TABLE strings (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY(id))")
    print("Table 'strings' created")
except:
    print("Table already exists")
    mycursor.execute("DROP TABLE strings")
    print("Table droped")
    mycursor.execute("CREATE TABLE strings (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY(id))")
    print("Table 'strings' recreated")

mydb.commit()

sql = "INSERT INTO strings (name) VALUES (%s)"

randomDict = {}

while len(randomDict) < (10 ** N):
    randomDict[id_generator()] = 1

print("Strings generated")

items = []
for elem in randomDict:
    items.append((elem,))

print("List created")

insertSum = 0

if N > 5:
    step = 10 ** (N - 5)
    for i in range(step):
        startSlice = (10 ** 5) * i
        stopSlice = (10 ** 5) * (i + 1)
        mycursor.executemany(sql, items[startSlice:stopSlice])
        mydb.commit()
        print("step " + str(i) + " done")
        insertSum += mycursor.rowcount
else:
    mycursor.executemany(sql, items)
    mydb.commit()
    insertSum += mycursor.rowcount

stop = perf_counter()
print("timer stop")

print(str(insertSum) + " records inserted.")
print("Python execution time: " + str(stop - start) + " s")