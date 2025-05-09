from Publication import Publication
from FilePublication import FilePublication
from TextDivider import TextDivider
import os
from string_object import sentence_correction
from PublicationClassifier import PublicationClassifier
from DbManager import DbManager


class TxtFilePublication(FilePublication):
    def __init__(self, num_of_publ, direction, path=r'ex1.txt'):
        super().__init__(num_of_publ, direction, path)

        self.blocks_number = len(TextDivider('\n\n\n').split_file(self.path))

    @staticmethod
    def input_num_of_publ_with_validation(message, path):
        num = input(message)
        while not num.isdigit() or int(num) > len(TextDivider('\n\n\n').split_file(path)):
            num = input("There are not that many number of publications in this file or you entered not a number. Enter another number: ")
        return num

    @staticmethod
    def initialize_from_user_input():
        is_custom_path = input('Do you want to use a custom path? (y/n): ')
        if is_custom_path == 'y':
            path = input('Enter the path to the file: ')
            path = Publication.input_file_path_with_validation(path)
        else:
            path = r'ex1.txt'

        num_of_publ = int(TxtFilePublication.input_num_of_publ_with_validation(f'Enter number of publications you want to publish from the file: ', path))
        direction = FilePublication.input_direction_with_validation('Specify from what end you want to take publications: \n 1 - from the beginning \n 2 - from the end ')
        return TxtFilePublication(num_of_publ, direction, path)

    def add_post_to_feed(self):
        file_path = 'news_feed.txt'

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        with open(file_path, 'a') as f:
            list_of_blocks = TextDivider('\n\n\n').split_file(self.path)
            if self.direction == '1':
                for num in range(self.num_of_publ):
                    block = list_of_blocks[num]
                    block_type = (PublicationClassifier.classify(block)).capitalize()
                    f.write(f'----------{block_type}----------\n{sentence_correction(block)}\n\n\n\n')
                text_left = list_of_blocks[self.num_of_publ:]
            else:
                for num in range(self.num_of_publ):
                    block = list_of_blocks[-num - 1]
                    block_type = (PublicationClassifier.classify(block)).capitalize()
                    f.write(f'----------{block_type}----------\n{sentence_correction(block)}\n\n\n\n')
                text_left = list_of_blocks[:-self.num_of_publ]
            with open(self.path, 'w') as f:
                f.write('\n\n\n'.join(text_left))

    def insert_data(self):
        db = DbManager()
        list_of_blocks = TextDivider('\n\n\n').split_file(self.path)

        if self.direction == '1':
            selected_blocks = list_of_blocks[:self.num_of_publ]
        else:
            selected_blocks = list_of_blocks[-self.num_of_publ:]

        for block in selected_blocks:
            corrected_text = sentence_correction(block)
            block_type = PublicationClassifier.classify(block)

            result = db.duplication_validation(corrected_text, block_type)
            if result[0][0] > 0:
                print(f"Duplicate detected. {block_type} with text:\n'{corrected_text}' already exists in the database.\n")
                continue
            else:
                db.insert_from_txt_block(block_type, corrected_text)

    def remove_empty_file(self):
        if os.path.exists(self.path) and os.path.getsize(self.path) == 0:
            os.remove(self.path)
