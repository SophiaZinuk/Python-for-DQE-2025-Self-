from abc import ABC, abstractmethod
from datetime import date

class Publication(ABC):
    def __init__(self, text, date):
        self.text = text
        self.date = date

    @abstractmethod
    def create_post(self):
        pass


class News(Publication):
    def __init__(self, text, city, date):
        super().__init__(text, date)
        self.city = city

    def create_post(self):
        pass
    

class PrivatAd(Publication):
    def __init__(self, text, date):
        super().__init__(text, date)

    def __calculate_days_left(self):
        return - date.today() + self.date
    
    def create_post(self):
        pass


class WeatherForecast(Publication):
    def __init__(self, city, date, temperature, text):
        super().__init__(text, date)
        self.city = city
        self.temperature = temperature

    def __generate_advice(self):
        pass

    def create_post(self):
        pass

