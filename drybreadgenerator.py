import json
from random import choice
from sys import stderr

with open('resources/tmp_database.txt', 'r', encoding='utf-8') as dbbasefile:
    data = dbbasefile.read()

drybread_data = json.loads(data)
NUM_DB = len(drybread_data['suchary'])
print("Loaded", NUM_DB, "dry breads.", file=stderr)

def get_random_drybread():
    return choice(drybread_data['suchary'])

def get_random_drybread_index():
    return choice(range(len(drybread_data['suchary'])))

def get_drybread_at_index(index):
       return drybread_data['suchary'][index]