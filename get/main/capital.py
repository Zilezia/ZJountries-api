from get.fields import *

class CapitalName(Resource):
    def get(self, capitals):
        capital_list = capitals.split(',')
        matching_countries = []
        
        fields_param = request.args.get("fields", None)
        full_text_call = request.args.get('fulltext', '').lower() == 'true'
        
        for capital in capital_list:
            capital_lower = capital.lower()
            if full_text_call:
                matches = [country for country in data if capital_lower == country['capital']['name']['common'].lower()]
            else:
                matches = [country for country in data if capital_lower in country['capital']['name']['common'].lower()]
            matching_countries.extend(matches)
            
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
