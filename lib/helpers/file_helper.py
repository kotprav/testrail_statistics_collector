import json


def read_list_of_dicts_from_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            print(f"{file_path} is successfully loaded")
            return data
    except:
        pass

    return []


def write_list_of_dicts_to_file(file_path, list_of_dicts):
    with open(file_path, 'w') as f:
        json.dump(list_of_dicts, f)


def write_list_to_file(file_path, list):
    with open(file_path, 'w') as filehandle:
        for list_item in list:
            filehandle.write(f'{list_item}\n')


def read_list_from_file(file_path):
    result_list = []
    try:
        with open(file_path, 'r') as filehandle:
            for line in filehandle:
                # Remove linebreak which is the last character of the string
                curr_place = line[:-1]
                # Add item to the list
                result_list.append(curr_place)
                print(f"{file_path} is successfully loaded")
    except:
        pass

    return result_list
