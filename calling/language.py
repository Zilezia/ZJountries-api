from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Language(Resource):
    def get(self, languages):
        language_list = languages.split(',')
        matching_countries = []
        
        official_lang_call = request.args.get('official', '').lower() == 'true'
        spoken_lang_call = request.args.get('spoken', '').lower() == 'true'
        
        for language in language_list:
            language_lower = language.lower()
            
            if official_lang_call:
                matches = [country for country in data if 
                    language_lower in [c.lower() for c in country['languages']['official']]
                ]
            elif spoken_lang_call:
                matches = [country for country in data if 
                    language_lower in [c.lower() for c in country['languages']['spoken']]
                ]
            else:
                matches = [country for country in data if 
                    (language_lower in [c.lower() for c in country['languages']['official']]) or
                    (language_lower in [c.lower() for c in country['languages']['spoken']])
                ]
            matching_countries.extend(matches)
        
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Countries not found."}), 404
