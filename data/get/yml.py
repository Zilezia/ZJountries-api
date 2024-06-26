import yaml

with open('impo.yaml', 'r') as file:
    data = yaml.safe_load(file)
    
for item in data['place']:
    print(item)