import pandas as pd

data = pd.read_json("./data/dataset/data.json").to_dict(orient='records')

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
    
    return fields_data
