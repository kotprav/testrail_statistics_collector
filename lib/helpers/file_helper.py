import json


def read_list_of_dicts_from_file(file_path: str) -> list[dict]:  # pragma: no cover
    try:
        with open(file_path, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            print(f"---Cache: {file_path} is successfully loaded")
            return data
    except:
        pass

    return []


def write_list_of_dicts_to_file(file_path: str, list_of_dicts: list):  # pragma: no cover
    with open(file_path, 'w') as file:
        json.dump(list_of_dicts, file)


def write_list_to_file(file_path: str, list_to_write: list):  # pragma: no cover
    with open(file_path, 'w') as filehandle:
        for list_item in list_to_write:
            filehandle.write(f'{list_item}\n')


def read_list_from_file(file_path: str) -> list:  # pragma: no cover
    result_list = []
    try:
        with open(file_path, 'r') as filehandle:
            for line in filehandle:
                # Remove linebreak which is the last character of the string
                curr_place = line[:-1]
                # Add item to the list
                result_list.append(curr_place)
                print(f"---Cache: {file_path} is successfully loaded")
    except:
        pass

    return result_list
