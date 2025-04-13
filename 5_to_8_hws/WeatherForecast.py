from Publication import Publication
from DbManager import DbManager
import os


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
 

    @DbManager.open_close_manager
    def insert_data(self):
        db = DbManager()
        if db.duplication_validation(self.text, "weatherforecast")[0][0] > 0:
            print(f"Duplicate detected: WeatherForecast with text '{self.text}' already exists in the database.")
            return None, None
    
        query = '''
            INSERT INTO feed (
                type, text, date, fromtxt, fromjson, fromxml,
                city, temperature, weatheradvice, userinput
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            "weatherforecast",
            self.text,
            self.date,
            False,
            False,
            False,
            self.city,
            self.temperature,
            self.__generate_advice(),
            True
        )
        return query, params