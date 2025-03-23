from FilePublication import FilePublication
import json
from Publication import Publication
import os


class JsonFilePublication(FilePublication):
    def __init__(self, num_of_publ, direction, path = r'ex1.json'):
        super().__init__(num_of_publ, direction, path)

        blocks_number = len(json.load(open(self.path)))

    @staticmethod
    def input_num_of_publ_with_validation(message, path):
        num = input(message)
        while not num.isdigit() or int(num) > len(json.load(open(path))):
            num = input("There are not that many number of publications in this file or you entered not a number. Enter another number: ")
        return num
    

    @staticmethod
    def initialize_from_user_input():
        is_custom_path = input('Do you want to use a custom path? (y/n): ')
        if is_custom_path == 'y':
            path = Publication.input_file_path_with_validation('Enter the path to the file: ')
        else:
            path = r'ex1.json'

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
    
    

    def remove_empty_file():
        pass

pub = JsonFilePublication.initialize_from_user_input()
pub.add_post_to_feed()