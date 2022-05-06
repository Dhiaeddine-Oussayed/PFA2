from time import time
from nltk import word_tokenize, pos_tag
from itertools import chain

start = time()

a = list(chain(*pos_tag(word_tokenize("i want a timer please"))))
if 'CD' not in a:
    print(False)
else:
    print(True)
end = time()

starting = time()

print(any(value.isdigit() for value in "i want a timer please".split()))

ending = time()

print(end - start)
print(ending- starting)