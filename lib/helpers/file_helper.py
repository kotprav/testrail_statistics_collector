import json


def read_list_of_dicts_from_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            print(f"Information is successfully loaded from {file_path}")
            return data
    except:
        pass

    return []


def write_list_of_dicts_to_file(file_path, list_of_dicts):
    with open(file_path, 'w') as f:
        json.dump(list_of_dicts, f)
