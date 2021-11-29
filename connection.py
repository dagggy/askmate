'''This layer contains common functions to read, write,
or append CSV files without feature-specific knowledge.
Only this layer can access long term data storage.
In this case, CSV files are used as storage, later this will switch to SQL databases.
'''
import csv
import os

def get_path(filename:str):
    return os.path.join(os.path.dirname(__file__), filename)


def read_file(filename:str):
    file_data = []
    first_row = []
    file = get_path(filename)
    with open(file, mode='r') as inp:
        reader = csv.reader(inp)
        for row in reader:
            if first_row == []:
                first_row = row
            else:
                row_dict = {}
                for value in range(len(first_row)):
                    current_item = first_row[value]
                    row_dict[current_item] = row[value]
                file_data.append(row_dict)
    return file_data

def save_file(data_list:list, filename:str):
    file = get_path(filename)
    prepared_data = prepare_data(data_list)
    writer = csv.writer(open(file, 'w', newline=''))
    writer.writerows(prepared_data)

def prepare_data(data_list:list):
    prepared_data = []
    try:
        prepared_data = [list(data_list[0].keys())]
        for i in range(len(data_list)):
            prepared_data.append(list(data_list[i].values()))
            print('prepared record ' + str(i+1))
    except:
        pass
    return prepared_data
