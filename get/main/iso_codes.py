# ZJountries-api is a RESTful program indented for quick access to world places data
# Copyright (C) 2024  Zilezia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from get.fields import *

class ISO2Code(Resource):
    def get(self, alpha2s):
        alpha2_list = alpha2s.split(',')
        fields_param = request.args.get("fields", None)
        matching_countries = []
        for alpha2 in alpha2_list:
            alpha2_lower = alpha2.lower()
            matching_countries.extend(
                [country for country in data if alpha2_lower == country['code']['alpha-2'].lower()]
            )
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
        
class ISO3Code(Resource):
    def get(self, alpha3s):
        alpha3_list = alpha3s.split(',')
        fields_param = request.args.get("fields", None)
        matching_countries = []
        for alpha3 in alpha3_list:
            alpha3_lower = alpha3.lower()
            matching_countries.extend(
                [country for country in data if alpha3_lower == country['code']['alpha-3'].lower()]
            )
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
        
class ISONumCode(Resource):
    def get(self, numerics):
        numeric_list = numerics.split(',')
        fields_param = request.args.get("fields", None)
        matching_countries = []
        for numeric in numeric_list:
            matching_countries.extend(
                [country for country in data if numeric == country['code']['numeric']]
            )
        
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)