from flask import jsonify, request
from flask_restful import Resource
import pandas as pd

from calling.fields.fields_helper import get_fields

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Language(Resource):
    def get(self, languages):
        language_list = languages.split(',')
        matching_countries = []
        
        fields_param = request.args.get("fields", None)
        official_lang_call = 'official' in request.args
        spoken_lang_call = 'spoken' in request.args
        
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
        
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
