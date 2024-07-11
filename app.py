from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
import pandas as pd

from config import Config
from calling import *

app = Flask(__name__)
app.json.sort_keys = False
app.config.from_object(Config)

api = Api(app)
api_ver = 'v'+app.config['API_VERSION']

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

@app.context_processor
def inject_config(): # 2nd version bc icba removing or adding "v"'s
    return dict(api_ver=api_ver,api_version=app.config['API_VERSION'],domain=app.config['DOMAIN'])

@app.route("/")
def home():
    return render_template("index.html")

# all
api.add_resource(All, f"/{api_ver}/all")
# geo
api.add_resource(CountryName, f"/{api_ver}/name=<string:names>")
api.add_resource(Continent, f"/{api_ver}/continent=<string:continents>")
# iso
api.add_resource(ISO2Code, f"/{api_ver}/iso2=<string:alpha2s>")
api.add_resource(ISO3Code, f"/{api_ver}/iso3=<string:alpha3s>")
api.add_resource(ISONumCode, f"/{api_ver}/isoN=<string:numerics>")
# langs
api.add_resource(Language, f"/{api_ver}/language=<string:languages>")

# api.add_resource(Field, f"/{api_ver}/field=<string:fields>") # kinda unnecessary, works same as /all?field={fields}

if __name__ == '__main__':
    app.run(debug=True)