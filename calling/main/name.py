from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

from calling.fields.fields_helper import get_fields

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class CountryName(Resource):
    def get(self, names):
        names_list = names.split(',')
        matching_countries = []
        
        fields_param = request.args.get("fields", None)
        full_text_call = request.args.get('fulltext', '').lower() == 'true'
        
        for name in names_list:
            name_lower = name.lower()
            if full_text_call:
                matches = [country for country in data if name_lower == country['name']['common'].lower()]
            else:
                matches = [country for country in data if name_lower in country['name']['common'].lower()]
            matching_countries.extend(matches)
            
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
