import pickle
from classes.Home import Home
from classes.Database import Database

test = Database('house')
try:
    test.root.save(Home('house','kitchen', 'living room', 'garage'))
except Exception as e:
    print(e)

with open('test.pickle', 'wb') as handle:
    pickle.dump(test, handle, protocol=pickle.HIGHEST_PROTOCOL)