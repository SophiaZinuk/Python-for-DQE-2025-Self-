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

    @abstractmethod
    def date_input_control(self):
        pass


class News(Publication):
    def __init__(self, text, city, date):
        super().__init__(text, date)
        self.city = city

    @staticmethod
    def initialize_from_user_input():
        city = input('Enter news city: ')
        text = input('Enter news text: ')
        date = input('Enter news date: ')
        return News(text, city, date)

    def date_input_control(self):
        correct = False
        while not correct:
            try:
                datetime.strptime(self.date, "%Y-%m-%d")
                correct = True
            except ValueError:
                self.date = input("Enter news date in the format YYYY-MM-DD: ")



    def create_post(self):
        file_path = 'news_feed.txt'
    
        # Check if the file exists, if not, create it and add the header
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
    
        # Append the new post to the file
        with open(file_path, 'a') as f:
            f.write(f'----------News----------\n{self.text} ({self.date})\n{self.city}, {datetime.now()}\n\n\n\n')
    

class PrivateAd(Publication):
    def __init__(self, text, date):
        super().__init__(text, date)
        self.exp_date = self.__calculate_last_day()

    @staticmethod
    def initialize_from_user_input():
        text = input('Enter ad text: ')
        date = int(input('Enter number of days for this ad: '))
        return PrivateAd(text, date)

    def __calculate_last_day(self):
        return date.today() + timedelta(days=self.date)
    
    def __calculate_days_left(self):
        return (self.exp_date - date.today()).days
    
    def date_input_control(self):
        correct = False
        while not correct:
            if self.date > 0:
                correct = True
            else:
                self.date = input("Enter number of days for this ad: ")
    
    def create_post(self):
        file_path = 'news_feed.txt'
    
        # Check if the file exists, if not, create it and add the header
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        # Append the new post to the file
        with open(file_path, 'a') as f:
            f.write(f'----------Private Ad----------\n{self.text}\nActual until: {self.exp_date}, {self.__calculate_days_left()} days left\n\n\n\n')



class WeatherForecast(Publication):
    def __init__(self, city, date, temperature, text):
        super().__init__(text, date)
        self.city = city
        self.temperature = temperature

    @staticmethod
    def initialize_from_user_input():
        city = input('Enter the city: ')
        date = input('Enter the date: ')
        temperature = int(input('Enter the temperature: '))
        text = input('Enter the text: ')
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
        
    def date_input_control(self):
        correct = False
        while not correct:
            try:
                datetime.strptime(self.date, "%Y-%m-%d")
                correct = True
            except ValueError:
                self.date = input("Enter the date in the format YYYY-MM-DD: ")
        

    def create_post(self):
        file_path = 'news_feed.txt'
    
        # Check if the file exists, if not, create it and add the header
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("News feed:\n\n")
        # Append the new post to the file
        with open(file_path, 'a') as f:
            f.write(f'----------Weather Forecast for {self.city}, {self.date}----------\n{self.text}\nTemperature: {self.temperature}\nAdvice: {self.__generate_advice()}\n\n\n\n')


if __name__ == '__main__':  
    while True:
        publication = input(f'Enter the type of publication: \n 1 - news \n 2 - private ad \n 3 - weather forecast \n Enter smth else to exit: ')
        if publication == '1':
            pub  = News.initialize_from_user_input()
        elif publication == '2':
            pub = PrivateAd.initialize_from_user_input()
        elif publication == '3':    
            pub = WeatherForecast.initialize_from_user_input()
        else:
            break
        pub.date_input_control()
        pub.create_post()