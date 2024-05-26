"""
This module is used to convert the data from a CSV file to a JSON file.
"""
import csv
import json

csv_file_path = 'data.csv'
json_file_path = 'data.json'

data = []
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

with open(json_file_path, mode='w') as json_file:
    json.dump(data, json_file, indent=4)