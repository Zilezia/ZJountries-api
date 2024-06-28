from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
app.json.sort_keys = False
api = Api(app)

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Countries(Resource):
    def get(self):
        return jsonify(data)
    
class CountryName(Resource):
    def get(self, names):
        names_list = names.split('&')
        matching_countries = []
        for name in names_list:
            name_lower = name.lower()
            matching_countries.extend(
                [country for country in data if name_lower in country['name']['common'].lower()]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404

class AlphaTwoCode(Resource):
    def get(self, alpha2s):
        alpha2_list = alpha2s.split('&')
        matching_countries = []
        for alpha2 in alpha2_list:
            alpha2_lower = alpha2.lower()
            matching_countries.extend(
                [country for country in data if alpha2_lower in country['code']['alpha-2'].lower()]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404
        
class AlphaThreeCode(Resource):
    def get(self, alpha3s):
        alpha3_list = alpha3s.split('&')
        matching_countries = []
        for alpha3 in alpha3_list:
            alpha3_lower = alpha3.lower()
            matching_countries.extend(
                [country for country in data if alpha3_lower in country['code']['alpha-3'].lower()]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404
        
class NumericCode(Resource):
    def get(self, numerics):
        numeric_list = numerics.split('&')
        matching_countries = []
        for numeric in numeric_list:
            matching_countries.extend(
                [country for country in data if numeric in country['code']['numeric']]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404

@app.route("/")
def home():
    return render_template("index.html")

api.add_resource(Countries, '/all')
api.add_resource(CountryName, "/name/<string:names>")
api.add_resource(AlphaTwoCode, "/alpha-2/<string:alpha2s>")
api.add_resource(AlphaThreeCode, "/alpha-3/<string:alpha3s>")
api.add_resource(NumericCode, "/numeric/<string:numerics>")


if __name__ == '__main__':
    app.run(debug=True)