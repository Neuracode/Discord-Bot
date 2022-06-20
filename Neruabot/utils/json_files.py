import json

def write_json_data(data, path):
    json_object = json.dumps(data, indent=4)
    with open(path, "w") as outfile:
        outfile.write(json_object)

def read_json_data(path):
    with open(path, 'r') as openfile:
        data = json.load(openfile)
    return data