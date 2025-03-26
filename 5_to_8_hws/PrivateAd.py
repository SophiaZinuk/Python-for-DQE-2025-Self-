from Publication import Publication
from datetime import date, datetime, timedelta
import os


class PrivateAd(Publication):
    def __init__(self, text, date):
        super().__init__(text, date)
        self.exp_date = self.__calculate_last_day()
 
 
    @staticmethod
    def initialize_from_user_input():
        text = Publication.input_text_with_validation('Enter ad text: ')
        date = int(Publication.input_number_with_validation('Enter number of days for this ad: '))
        return PrivateAd(text, date)
 
    def __calculate_last_day(self):
        return date.today() + timedelta(days=self.date)
   
    def __calculate_days_left(self):
        return (self.exp_date - date.today()).days
 
   
    def create_post(self):
        file_path = 'news_feed.txt'
   
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        with open(file_path, 'a') as f:
            f.write(f'----------Private Ad----------\n{self.text}\nActual until: {self.exp_date}, {self.__calculate_days_left()} days left\n\n\n\n')
 