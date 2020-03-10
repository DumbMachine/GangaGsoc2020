import pprint
from pymongo import MongoClient

# Getting access to the Database
client = MongoClient('localhost', 27017)
db = client.ganga_eval

# Using document from the Database
example = db.json_example

# Placeholder/Example values
values = [
	{"color": "red", "value": "#f00"},
	{"color": "green", "value": "#0f0"},
	{"color": "blue", "value": "#00f"},
	{"color": "cyan", "value": "#0ff"},
	{"color": "magenta", "value": "#f0f"},
	{"color": "yellow", "value": "#ff0"},
	{"color": "black", "value": "#000"}
]

# inserting data, one-by-one, into the database
for value in values:
    example.insert_one(value)
print("We are inserted the following values: ")
pprint.pprint(values)

# Reading the same data
returned_values = [*example.find()]
print("We received the following values: ")
pprint.pprint(returned_values)

# Comparing, if they are the same values
assert values == returned_values
print("Asertion was successful")