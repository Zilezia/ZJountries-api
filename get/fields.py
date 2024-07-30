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

from flask import jsonify, request
from flask_restful import Resource
import json

data_path = "./data/dataset/data.json"

with open(data_path) as file:
    data = json.load(file)

def get_fields(fields, data_subset=None):
    field_list = fields.split(',')
    fields_data = []

    if data_subset is None:
        data_subset = data

    for record in data_subset:
        record_data = {}
        for field in field_list:
            if field in record:
                record_data[field] = record[field]

        fields_data.append(record_data)
    
    if fields_data:
            return fields_data
    else:
        return jsonify({"error": "Fields not found."}), 404 # barely shows this but typical flask error