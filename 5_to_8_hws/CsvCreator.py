import csv
from re import split as sp
from re import findall

class CsvCreator:
    file_path = 'news_feed.txt'

    def __word_counter() -> dict:
        with open(CsvCreator.file_path, 'r') as file:
            text = file.read()
            list_of_values = sp(r'[-!,.? :;\n"()]', text.lower())

        list_of_words = [word for word in list_of_values if word.isalpha()]

        words_dict = {word : list_of_words.count(word) for word in list_of_words}

        return words_dict


    def __letter_counter():
        with open(CsvCreator.file_path, 'r') as file:
            text = file.read()
            list_of_letters = sp(r'', text.lower())
            dict_of_values = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
            for letter in list_of_letters:
                if letter in dict_of_values.keys():
                    dict_of_values[letter] += 1
            sum_num = sum(dict_of_values.values())
        return dict_of_values, sum_num
    
    def __upper_letter_counter() -> dict:
        with open(CsvCreator.file_path, 'r') as file:
            text = file.read()
            list_of_upper_letters = findall(r'[A-Z]', text)
            dict_of_upper_letters = {i : list_of_upper_letters.count(i.upper()) for i in CsvCreator.__letter_counter()[0].keys()}
            return dict_of_upper_letters


    def update_csvs():
        with open('word_count.csv', 'w', newline='') as word_count:
            writer = csv.writer(word_count, delimiter='-')
            for k, v in CsvCreator.__word_counter().items():
                writer.writerow([k, v])
        
        with open('letter_count.csv', 'w', newline='') as letter_count:
            headers = ['letter', 'count_all', 'count_uppercase', 'percentage, %']
            writer = csv.DictWriter(letter_count, fieldnames=headers)
            writer.writeheader()
            for letter, count in CsvCreator.__letter_counter()[0].items():
                writer.writerow({'letter': letter, 'count_all' : count, 'count_uppercase' : CsvCreator.__upper_letter_counter()[letter], 'percentage, %' : round(count/CsvCreator.__letter_counter()[1]*100, 2)})

# print(CsvCreator.letter_counter())