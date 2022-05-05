from time import time
import json

x = json.load(open('languages.json'))


start = time()

if 'polish' in tuple(x.keys()):
    print(1)

end = time()

starting = time()

if 'polish' in list(x.keys()):
    print(1)
ending = time()

print(end - start)
print(ending- starting)