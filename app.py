from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api 
import pandas as pd

app = Flask(__name__)
app.json.sort_keys = False
api = Api(app)

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

class Countries(Resource):
    def get(self):
        return jsonify(data)
    
class CountryName(Resource):
    def get(self, name):
        name_lower = name.lower()
        matching_countries = [country for country in data if name_lower in country['name']['common'].lower()]
        if matching_countries:
            return jsonify(matching_countries)
        else:
            return jsonify({"error": "Country not found."}), 404

@app.route("/")
def home():
    return render_template("index.html")

api.add_resource(Countries, '/all')
api.add_resource(CountryName, "/name/<string:name>")


if __name__ == '__main__':
    app.run(debug=True)