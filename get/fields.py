from flask import jsonify, request
from flask_restful import Resource
import json

data_path = "./data/dataset/data3.json" # previous
# data_path = "./data/dataset/td.json"

with open(data_path) as file:
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
        return jsonify({"error": "Fields not found."}), 404 # barely shows this but typical flask error