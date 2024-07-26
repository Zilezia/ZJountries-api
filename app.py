from flask import Flask, render_template
from flask_restful import Api

from config import Config
from get import *

app = Flask(__name__)
app.json.sort_keys = False
app.config.from_object(Config)

api = Api(app)
api_ver = 'v'+app.config['API_VERSION']

@app.context_processor
def inject_config():
    return dict(
        api_ver=api_ver,
        api_version=app.config['API_VERSION'],  # 2nd version bc icba removing or adding "v"'s
        domain=app.config['DOMAIN']
    )

@app.route("/")
def home():
    # thinking either to have this way to load the sections or if it too much
    components = [
        'about', 'all', 
        'name', 'continent', 
        'iso', 'lang', 
        'fields', 'mult', 
    'github']
    return render_template("doc.html", components=components)

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

if __name__ == "__main__":
    app.run(debug=True, port=2137)