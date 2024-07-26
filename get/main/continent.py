from get.fields import *

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
        
        fields_param = request.args.get('fields', None)
        
        matching_countries = []
        for continent in continents_list:
            actual_continent = continent_alias.get(continent.lower(), continent)
            matches = [country for country in data if actual_continent in country['continents']] # continent/s
            matching_countries.extend(matches)
        
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)