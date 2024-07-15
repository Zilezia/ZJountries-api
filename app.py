from flask import Flask, render_template
from flask_restful import Api
import pandas as pd

from config import Config
from get import *

app = Flask(__name__)
app.json.sort_keys = False
app.config.from_object(Config)

api = Api(app)
api_ver = 'v'+app.config['API_VERSION']

@app.context_processor
def inject_config(): # 2nd version bc icba removing or adding "v"'s
    return dict(
        api_ver=api_ver,
        api_version=app.config['API_VERSION'],
        domain=app.config['DOMAIN']
    )

@app.route("/")
def home():
    return render_template("index.html")
# been a slight pause wanted to try to replace ^ this with vite react 
# but the only annoying part would be updating the version in like 3
# seperate locations so im just gonna keep this

# oh yeah right i can do the same thing i wished on doing in vite
# i forgot that it uses jinji so that might actually be better to do
# i really disliked how big and confusing the file became with all 
# the sections thats it tbh, all the struggle to have the same 
# outcome + functionality

# all
api.add_resource(All, f"/{api_ver}/all")
# geo
api.add_resource(CountryName, f"/{api_ver}/name=<string:names>")
api.add_resource(Continent,   f"/{api_ver}/continent=<string:continents>")
api.add_resource(CapitalName, f"/{api_ver}/capital=<string:capitals>")
# iso
api.add_resource(ISO2Code,   f"/{api_ver}/iso2=<string:alpha2s>")
api.add_resource(ISO3Code,   f"/{api_ver}/iso3=<string:alpha3s>")
api.add_resource(ISONumCode, f"/{api_ver}/isoN=<string:numerics>")
# langs
api.add_resource(Language, f"/{api_ver}/language=<string:languages>")

# api.add_resource(Field, f"/{api_ver}/field=<string:fields>") # kinda unnecessary, works same as /all?field={fields}
