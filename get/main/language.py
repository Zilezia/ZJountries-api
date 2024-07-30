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

class Language(Resource):
    def get(self, languages):
        language_list = languages.split(',')
        matching_countries = []
        
        fields_param = request.args.get("fields", None)
        # official_lang_call = 'official' in request.args
        # spoken_lang_call = 'spoken' in request.args
        
        for language in language_list:
            language_lower = language.lower()
            
            # if official_lang_call:
            #     matches = [country for country in data if 
            #         language_lower in [c.lower() for c in country['languages']['official']]
            #     ]
            # elif spoken_lang_call:
            #     matches = [country for country in data if 
            #         language_lower in [c.lower() for c in country['languages']['spoken']]
            #     ]
            # else:
            matches = [country for country in data if 
                (language_lower in [c.lower() for c in country['official_lang']])
                # or
                # (language_lower in [c.lower() for c in country['languages']['spoken']])
            ]
            matching_countries.extend(matches)
        
        if not matching_countries:
            return jsonify({"error": "Country not found."}), 404

        if fields_param:
            matching_countries = get_fields(fields_param, matching_countries)

        return jsonify(matching_countries)
