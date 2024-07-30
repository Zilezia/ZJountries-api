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
