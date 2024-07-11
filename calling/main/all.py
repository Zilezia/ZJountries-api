from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

from calling.fields.fields import Fields

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class All(Resource):
    def get(self):
        fields_param = request.args.get("fields", None)
        
        if fields_param:
            return Fields().get(fields_param)
        else:
            return jsonify(data)