from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
import pandas as pd

from config import Config

app = Flask(__name__)
app.json.sort_keys = False
app.config.from_object(Config)

api = Api(app)
api_ver = app.config['API_VERSION']

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Countries(Resource):
    def get(self):
        return jsonify(data)
    
class CountryName(Resource):
    def get(self, names):
        names_list = names.split(',')
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
        alpha2_list = alpha2s.split(',')
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
        alpha3_list = alpha3s.split(',')
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
        numeric_list = numerics.split(',')
        matching_countries = []
        for numeric in numeric_list:
            matching_countries.extend(
                [country for country in data if numeric in country['code']['numeric']]
            )
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404

@app.context_processor
def inject_version():
    return dict(api_version=app.config['API_VERSION'])

@app.route("/")
def home():
    return render_template("index.html")

api.add_resource(Countries,     f"/{api_ver}/all")
api.add_resource(CountryName,   f"/{api_ver}/name=<string:names>")
api.add_resource(AlphaTwoCode,  f"/{api_ver}/iso2=<string:alpha2s>")
api.add_resource(AlphaThreeCode,f"/{api_ver}/iso3=<string:alpha3s>")
api.add_resource(NumericCode,   f"/{api_ver}/isoN=<string:numerics>")


if __name__ == '__main__':
    app.run(debug=True)