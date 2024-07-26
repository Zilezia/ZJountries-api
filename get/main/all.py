from get.fields import *

class All(Resource):
    def get(self):
        fields_param = request.args.get("fields", None)
        
        countries = data
        
        if fields_param:
            countries = get_fields(fields_param, countries)

        return jsonify(countries)
        