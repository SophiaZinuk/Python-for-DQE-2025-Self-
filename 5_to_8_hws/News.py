from Publication import Publication
import os
from datetime import date, datetime, timedelta
from DbManager import DbManager

class News(Publication):
    def __init__(self, text, city, date):
        super().__init__(text, date)
        self.city = city
 
    @staticmethod
    def initialize_from_user_input():
        city = Publication.input_text_with_validation('Enter news city: ')
        text = Publication.input_text_with_validation('Enter news text: ')
        date = Publication.input_date_with_validation('Enter news date: ')
        return News(text, city, date)
 
 
    def create_post(self):
        file_path = 'news_feed.txt'
   
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
   
        with open(file_path, 'a') as f:
            f.write(f'----------News----------\n{self.text} \n{self.city}, {self.date}\n\n\n\n')
    
    @DbManager.open_close_manager
    def insert_data(self):
        query = '''
            INSERT INTO feed (
                type, text, date, fromtxt, fromjson, fromxml,
                city, temperature, weatheradvice, userinput
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            "privatad",
            self.text,
            self.date,
            False,
            False,
            False,
            self.city,
            None,
            None,
            True
        )
        return query, params