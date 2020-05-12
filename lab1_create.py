import string
import random


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


N = 6

kolekcja = {}

while len(kolekcja) < (10 ** N):
    kolekcja[id_generator()] = 1

items = []
for elem in kolekcja:
    items.append((elem,))

# for elem in items:
#     print(elem)

print(len(kolekcja))
