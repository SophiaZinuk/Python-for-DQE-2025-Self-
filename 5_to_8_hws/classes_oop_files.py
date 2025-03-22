from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
import os
import sys
from re import split as sp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hws2_4.string_object import sentence_correction
from CsvCreator import CsvCreator
 
 
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
            f.write(f'----------News----------\n{self.text} ({self.date})\n{self.city}, {datetime.now()}\n\n\n\n')
   
 
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
 
 
 
class WeatherForecast(Publication):
    def __init__(self, city, date, temperature, text):
        super().__init__(text, date)
        self.city = city
        self.temperature = temperature
 
    @staticmethod
    def initialize_from_user_input():
        city = Publication.input_text_with_validation('Enter the city: ')
        date = Publication.input_date_with_validation('Enter the date: ')
        temperature = int(Publication.input_number_with_validation('Enter the temperature: '))
        text = Publication.input_text_with_validation('Enter the text: ')
        return WeatherForecast(city, date, temperature, text)
 
    def __generate_advice(self):
        if self.temperature < 0:
            return 'Wear a coat'
        elif self.temperature < 10:
            return 'Wear a jacket'
        elif self.temperature < 20:
            return 'Wear a t-shirt/long-sleeved shirt'
        else:
            return 'Wear a swim suit :)'
       
 
    def create_post(self):
        file_path = 'news_feed.txt'
   
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        with open(file_path, 'a') as f:
            f.write(f'----------Weather Forecast----------\nFor {self.city}, {self.date}\n{self.text}\nTemperature: {self.temperature}\nAdvice: {self.__generate_advice()}\n\n\n\n')
 
 
class PublicationClassifier:
    keywords = {
        'news': { 'news', 'headline', 'report', 'reporter', 'journal', 'journalist',
        'breaking', 'update', 'live', 'coverage', 'announcement',
        'exclusive', 'interview', 'media', 'daily', 'broadcast', 'channel',
        'editorial', 'alert', 'developing', 'latest',
        'newspaper', 'press', 'article', 'source', 'coverage',
        'trending', 'event', 'public', 'statement', 'reveal', 'expose',
        'anchor', 'bulletin', 'issue', 'publication', 'column'},

        'privatead': {'ad', 'advertisement', 'advertising', 'promo', 'promotion',
        'sell', 'buy', 'discount', 'offer', 'deal', 'bargain', 'shop', 'shopping',
        'save', 'clearance', 'exclusive', 'coupon', 'hurry', 'subscribe', 'pricing',
        'available', 'gift', 'investment', 'purchase'},
   
        'weather': {'weather', 'forecast', 'temperature', 'rain', 'rainy', 'snow', 'snowfall',
        'cloudy', 'sunny', 'storm', 'stormy', 'wind', 'windy', 'humidity',
        'climate', 'hot', 'cold', 'freezing', 'thunder', 'lightning',
        'degrees', 'conditions', 'precipitation', 'heatwave', 'chilly', 'warm',
        'tornado', 'hail', 'fog', 'drizzle', 'meteorologist'}
    }
 
    @staticmethod
    def classify(text):
        words = set(sp(r'[!,.? :;]', text.lower()))
        match_counts = {category: len(words & kw_set) for category, kw_set in PublicationClassifier.keywords.items()}
        best_match = max(match_counts, key=match_counts.get)
        return best_match
 
 
 
class TextDivider:
    def __init__(self, divider):
        self.divider = divider

    def split_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
 
        return self.split_text(text)
 
    def split_text(self, text):
        return [block.strip() for block in text.split(self.divider) if block.strip()]
 
 
class FilePublication:
    def __init__(self, num_of_publ, direction, path = r'ex1.txt'):
        self.path = path
        self.num_of_publ = num_of_publ
        self.direction = direction

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
            path = Publication.input_file_path_with_validation('Enter the path to the file: ')
        else:
            path = r'ex1.txt'
 
        num_of_publ = int(FilePublication.input_num_of_publ_with_validation(f'Enter number of publications you want to publish from the file: ', path))
        direction = input('Specify from what end you want to take publications: \n 1 - from the beginning \n 2 - from the end ')
        return FilePublication(num_of_publ, direction, path)
   
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
                    type = (PublicationClassifier.classify(block)).capitalize()
                    f.write(f'----------{type}----------\n{sentence_correction(block)}\n\n\n\n')
                text_left = list_of_blocks[self.num_of_publ:]
            else:
                for num in range(self.num_of_publ):
                    block = list_of_blocks[-num -1]
                    type = (PublicationClassifier.classify(block)).capitalize()
                    f.write(f'----------{type}----------\n{sentence_correction(block)}\n\n\n\n')
                text_left = list_of_blocks[:-self.num_of_publ]
            with open(self.path, 'w') as f:
                f.write('\n\n\n'.join(text_left))

    def remove_empty_file(self):
        if os.path.exists(self.path) and os.path.getsize(self.path) == 0:
            os.remove(self.path)
 
 
 
if __name__ == '__main__':  
    while True:
        publication_method = input(f'''Enter publication method: \n 1 - input from the keyboard \n 2 - download from file
                                 \n Enter smth else to exit:''')
        if publication_method == '1':
            publication = input(f'Enter the type of publication: \n 1 - news \n 2 - privat ad \n 3 - weather forecast \n Enter smth else to exit: ')
            if publication == '1':
                pub  = News.initialize_from_user_input()
            elif publication == '2':
                pub = PrivateAd.initialize_from_user_input()
            elif publication == '3':    
                pub = WeatherForecast.initialize_from_user_input()
            else:
                break
            pub.create_post()
        elif publication_method == '2':
            pub = FilePublication.initialize_from_user_input()
            pub.add_post_to_feed()
            pub.remove_empty_file()
        else:
            break

        CsvCreator.update_csvs()



# 210 string: or vs and

# rewrite classes in different files
        