from FilePublication import FilePublication
import xml.etree.ElementTree as ET
from DbManager import DbManager
import os


class XmlFilePublication(FilePublication):
    def __init__(self, num_of_publ, direction, path):
        super().__init__(num_of_publ, direction, path)

        xml_file = ET.parse(self.path)
        self.root = xml_file.getroot()

    @staticmethod
    def input_num_of_publ_with_validation(message, path):
        num = input(message)
        xml_file = ET.parse(path)
        root = xml_file.getroot()

        while not num.isdigit() or int(num) > len(root):
            num = input("There are not that many number of publications in this file or you entered not a number. Enter another number: ")
        return num

    @staticmethod
    def is_xml_valid(path): 
        publication_type_keys_map = {
            'news': {'city', 'text', 'date'},
            'privatead': {'text', 'actual_until_date'},
            'weatherforecast': {'text', 'date', 'city', 'temperature'}
        }
        is_valid = True
        xml_file = ET.parse(path)
        root = xml_file.getroot()

        for element in root:
            list_of_tags = {inner.tag for inner in element}
            is_valid = is_valid & (list_of_tags == publication_type_keys_map.get(element.tag, set()))

        return is_valid

    @staticmethod
    def input_file_path_with_validation(path):
        while not os.path.exists(path) or not path.__contains__('.xml') or not XmlFilePublication.is_xml_valid(path):
            path = input("Your file doesn't exist OR XML is in invalid format. Enter another path: ")
        return path

    @staticmethod
    def initialize_from_user_input():
        is_custom_path = input('Do you want to use a custom path? (y/n): ')
        if is_custom_path == 'y':
            path = input('Enter the path to the file: ')
            path = XmlFilePublication.input_file_path_with_validation(path)
        else:
            path = XmlFilePublication.input_file_path_with_validation(r'ex1.xml')

        num_of_publ = int(XmlFilePublication.input_num_of_publ_with_validation(f'Enter number of publications you want to publish from the file: ', path))
        direction = FilePublication.input_direction_with_validation('Specify from what end you want to take publications: \n 1 - from the beginning \n 2 - from the end ')
        return XmlFilePublication(num_of_publ, direction, path)

    def add_post_to_feed(self):
        file_path = 'news_feed.txt'
        xml_file = ET.parse(self.path)
        root = xml_file.getroot()

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        with open(file_path, 'a') as f:
            if self.direction == '1':
                for element in root[:self.num_of_publ]:
                    f.write(f'----------{element.tag.capitalize()}----------\n')
                    for el in element:
                        f.write(f'{el.tag.capitalize()}: {el.text}\n')
                    f.write('\n\n\n')
                    root.remove(element)

            else:
                for element in root[len(root) - 1 : len(root) - self.num_of_publ -1 : -1]:
                    f.write(f'----------{element.tag.capitalize()}----------\n')
                    for el in element:
                        f.write(f'{el.tag.capitalize()}: {el.text}\n')
                    f.write('\n\n\n')
                    root.remove(element)

            # Save the modified XML back to the file
            xml_file.write(self.path)
            self.root = xml_file.getroot()

    def remove_empty_file(self):
        if os.path.exists(self.path) and len(self.root) == 0:
            os.remove(self.path)

    def insert_data(self):
        db = DbManager()
        xml_file = ET.parse(self.path)
        root = xml_file.getroot()
        elements = list(root)

        if self.direction == '1':
            selected = elements[:self.num_of_publ]
        else:
            selected = elements[len(elements) - 1 : len(elements) - self.num_of_publ -1 : -1]

        for element in selected:
            block_text = ""
            for child in element:
                if child.tag == "text":
                    block_text = child.text
                    break
            block_type = element.tag

            # Check for duplicates based on both text and type
            result = db.duplication_validation(block_text, block_type)
            if result[0][0] > 0:
                print(f"Duplicate detected: {block_type} with text '{block_text}' already exists in the database.")
                continue

            db.insert_from_xml_block(element)
