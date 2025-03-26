import News
import PrivateAd
import WeatherForecast
import TxtFilePublication
import JsonFilePublication
from CsvCreator import CsvCreator  

 
if __name__ == '__main__':  
    while True:
        publication_method = input(f'''Enter publication method: \n 1 - input from the keyboard \n 2 - download from .txt file \n 3 - download from .json file
                                 \n Enter smth else to exit:''')
        if publication_method == '1':
            publication = input(f'Enter the type of publication: \n 1 - news \n 2 - private ad \n 3 - weather forecast \n Enter smth else to exit: ')
            if publication == '1':
                pub  = News.News.initialize_from_user_input()
            elif publication == '2':
                pub = PrivateAd.PrivateAd.initialize_from_user_input()
            elif publication == '3':    
                pub = WeatherForecast.WeatherForecast.initialize_from_user_input()
            else:
                break
            pub.create_post()
        elif publication_method == '2':
            pub = TxtFilePublication.TxtFilePublication.initialize_from_user_input()
            pub.add_post_to_feed()
            pub.remove_empty_file()
        elif publication_method == '3':
            pub = JsonFilePublication.JsonFilePublication.initialize_from_user_input()
            pub.add_post_to_feed()
            pub.remove_empty_file()
        else:
            break

        CsvCreator.update_csvs()

        