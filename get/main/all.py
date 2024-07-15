from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

from get.main.fields import get_fields

# data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')
data = pd.read_json("./data/dataset/data2.json").to_dict(orient='records')

class All(Resource):
    def get(self):
        fields_param = request.args.get("fields", None)
        
        countries = data
        
        if fields_param:
            countries = get_fields(fields_param, countries)

        return jsonify(countries)
        