from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class ISO2Code(Resource):
    def get(self, alpha2s):
        alpha2_list = alpha2s.split(',')
        matching_countries = []
        for alpha2 in alpha2_list:
            alpha2_lower = alpha2.lower()
            matching_countries.extend(
                [country for country in data if alpha2_lower == country['code']['alpha-2'].lower()]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404
        
class ISO3Code(Resource):
    def get(self, alpha3s):
        alpha3_list = alpha3s.split(',')
        matching_countries = []
        for alpha3 in alpha3_list:
            alpha3_lower = alpha3.lower()
            matching_countries.extend(
                [country for country in data if alpha3_lower == country['code']['alpha-3'].lower()]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404
        
class ISONumCode(Resource):
    def get(self, numerics):
        numeric_list = numerics.split(',')
        matching_countries = []
        for numeric in numeric_list:
            matching_countries.extend(
                [country for country in data if numeric == country['code']['numeric']]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404
