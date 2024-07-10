from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Continent(Resource):
    def get(self, continents):
        continent_alias = {
            'north_a': 'North America',
            'south_a': 'South America',
            'europe': 'Europe',
            'asia': 'Asia',
            'africa': 'Africa',
            'oceania': 'Oceania',
            'australia': 'Oceania',
            'antarctica': 'Antarctica',
        }
        continents_list = continents.split(',')
        matching_countries = []
        for continent in continents_list:
            actual_continent = continent_alias.get(continent.lower(), continent)
            # continent_lower = continent.lower()

            # matches = [country for country in data if continent_lower in [c.lower() for c in country['continent']]]
            # matches = [country for country in data if continent in country['continent']]
            matches = [country for country in data if actual_continent in country['continent']]
            matching_countries.extend(matches)
        
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Countries not found."}), 404
