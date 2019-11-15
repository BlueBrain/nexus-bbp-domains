import json

def get_json(filename:str):
    """
    :return: The data loaded from filename (has to be a .json file).
    """
    with open(filename) as json_file:
        json_data = json.load(json_file)
        return json_data


def save_json(payload:dict):
    with open(filename, 'w') as filehandle:
        json.dump(payload, filehandle, sort_keys=True, indent=4)