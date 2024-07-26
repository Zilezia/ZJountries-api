from flask import jsonify, request
from flask_restful import Resource
import json

# with open("./data/dataset/natn.json") as file: # test file
# with open("./data/dataset/data2.json") as file:
with open("./data/dataset/td.json") as file:
    data = json.load(file)

def get_fields(fields, data_subset=None):
    field_list = fields.split(',')
    fields_data = []

    if data_subset is None:
        data_subset = data

    for record in data_subset:
        record_data = {}
        for field in field_list:
            if field in record:
                record_data[field] = record[field]

        fields_data.append(record_data)
    
    if fields_data:
            return fields_data
    else:
        return jsonify({"error": "Fields not found."}), 404