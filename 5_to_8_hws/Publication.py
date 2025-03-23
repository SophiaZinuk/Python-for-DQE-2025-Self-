from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
import os

class Publication(ABC):
    def __init__(self, text, date):
        self.text = text
        self.date = date
 
    @abstractmethod
    def create_post(self):
        pass
 
    @abstractmethod
    def initialize_from_user_input(self):
        pass
 
 
    @staticmethod
    def input_text_with_validation(message):
        text = input(message)
        while not text.strip():
            text = input("Publication can't be w/o text. Enter the text: ")
        return text
   
    @staticmethod
    def input_date_with_validation(message):
        correct = False
        date = input(message)
        while not correct:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                correct = True
            except ValueError:
                date = input("Enter the date in the format YYYY-MM-DD: ")
        return date
   
    @staticmethod
    def input_number_with_validation(message):
        number = input(message)
        while not number.isdigit():
            number = input("Enter a number: ")
        return number
    
    @staticmethod
    def input_file_path_with_validation(message):
        file_path = input(message)
        while not os.path.exists(file_path):
            file_path = input("The path does not exist. Please enter a valid file path: ")
        return file_path