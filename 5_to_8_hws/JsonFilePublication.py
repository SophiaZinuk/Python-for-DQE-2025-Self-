from FilePublication import FilePublication
import json
from Publication import Publication
import os


class JsonFilePublication(FilePublication):
    def __init__(self, num_of_publ, direction, path = r'ex1.json'):
        super().__init__(num_of_publ, direction, path)

        self.blocks_number = len(json.load(open(self.path)))

    @staticmethod
    def input_num_of_publ_with_validation(message, path):
        num = input(message)
        while not num.isdigit() or int(num) > len(json.load(open(path))):
            num = input("There are not that many number of publications in this file or you entered not a number. Enter another number: ")
        return num
    
    @staticmethod
    def is_json_valid(list_of_dicts):
        publication_type_keys_map = {'news': ['type', 'city', 'text', 'date'], 'privatad': ['type', 'text', 'date'], 'weatherforecast': ['type', 'text', 'date', 'city', 'temperature']}
        is_valid = True

        # print(list_of_dicts)

        for dict in list_of_dicts:
            publication_type_keys_map[dict['type']].sort()
            keys_list = list(dict.keys())
            keys_list.sort()
            # print(publication_type_keys_map[dict['type']])
            # print(keys_list)
            is_valid = is_valid & (publication_type_keys_map[dict['type']] == keys_list)
        print(is_valid)

        return is_valid
            

    
    @staticmethod
    def input_file_path_with_validation(path):
        data = json.load(open(path))
        # print(path)

        while not os.path.exists(path) or not JsonFilePublication.is_json_valid(data):
            path = input("Your file doesn't exist OR json is in invalid format. Enter another path: ")

        return path

    

    @staticmethod
    def initialize_from_user_input():
        is_custom_path = input('Do you want to use a custom path? (y/n): ')
        if is_custom_path == 'y':
            path = input('Enter the path to the file: ')
            path = JsonFilePublication.input_file_path_with_validation(path)
        else:
            # path = JsonFilePublication.input_file_path_with_validation(r'ex1.json') !!!!!!!!!!!!!!!!!!
            path = JsonFilePublication.input_file_path_with_validation(path)

        num_of_publ = int(JsonFilePublication.input_num_of_publ_with_validation(f'Enter number of publications you want to publish from the file: ', path))
        direction = input('Specify from what end you want to take publications: \n 1 - from the beginning \n 2 - from the end ')
        return JsonFilePublication(num_of_publ, direction, path)

    def add_post_to_feed(self):
        file_path = 'news_feed.txt'
        data = json.load(open(self.path))
        data_length = len(data)
        

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        with open(file_path, 'a') as f:
            if self.direction == '1':
                for block in data[:self.num_of_publ]:
                    f.write(f'----------{block["type"].capitalize()}----------\n')
                    for key, value in block.items():
                        if key != 'type':
                            f.write(f'{key.capitalize()}: {value.capitalize()}\n')
                    f.write('\n\n\n')

                data_left = data[self.num_of_publ:]
            elif self.direction == '2':
                for block in data[data_length - 1 : data_length - self.num_of_publ -1 : -1]:
                    f.write(f'----------{block["type"].capitalize()}----------\n')
                    for key, value in block.items():
                        if key != 'type':
                            f.write(f'{key.capitalize()}: {value.capitalize()}\n')
                    f.write('\n\n\n')
                data_left = data[:data_length-self.num_of_publ]
                
            with open(self.path, 'w') as f:
                json.dump(data_left, f, indent=4)
                self.blocks_number = self.blocks_number - self.num_of_publ
    
    

    def remove_empty_file(self):
        if os.path.exists(self.path) and self.blocks_number == 0:
            os.remove(self.path)

pub = JsonFilePublication.initialize_from_user_input()
# print(pub.input_file_path_with_validation)
# pub.add_post_to_feed()
# pub.remove_empty_file()



# add validation of direction
# create function for validation json format, maybe class 
# HOW TO call data ones????
# string 59 - problem if path is defauld