from flask import jsonify
from flask_restful import Resource
import pandas as pd

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Fields(Resource):
    def get(self, fields):
        field_list = fields.split(',')
        
        fields_data = []
        for record in data:
            record_data = {}
            for field in field_list:
                if field in record:
                    record_data[field] = record[field]
            fields_data.append(record_data)
        
        if fields_data:
            return fields_data
        else:
            return jsonify({"error": "Fields not found."}), 404