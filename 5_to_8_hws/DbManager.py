import pyodbc
from functools import wraps

class DbManager:
  
    def open_close_manager(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            con = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};Direct=True;Database=feed.db;String Types=Unicode')
            cursor = con.cursor()
            try:
                result = func(self, *args, **kwargs)

                # Skip execution if result is None or (None, None)
                if result is None or (isinstance(result, tuple) and result[0] is None):
                    return

                # Support query with optional parameters
                if isinstance(result, tuple):
                    query, params = result
                    cursor.execute(query, params)
                else:
                    query = result
                    cursor.execute(query)

                if isinstance(query, str) and query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                else:
                    con.commit()
            finally:
                cursor.close()
                con.close()
        return wrapper

    @open_close_manager
    def create_table(self):
        return '''CREATE TABLE IF NOT EXISTS feed (
            type varchar(24),
            text text,
            date date,
            fromtxt bool,
            fromjson bool,
            fromxml bool,
            city varchar(32),
            temperature float,
            weatheradvice text,
            userinput bool
        );'''

    @open_close_manager
    def run_to_check(self):
        return f'SELECT * FROM feed'
    
    @open_close_manager
    def insert_from_txt_block(self, block_type, text):
        query = '''
            INSERT INTO feed (
                type, text, date, fromtxt, fromjson, fromxml,
                city, temperature, weatheradvice, userinput
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            block_type,
            text,
            None,     # date
            True,     # fromtxt
            False,    # fromjson
            False,    # fromxml
            None,     # city
            None,     # temperature
            None,     # weatheradvice
            False     # userinput
        )
        return query, params


    @open_close_manager
    def duplication_validation(self, text, type):
        query = "SELECT COUNT(*) FROM feed WHERE text = ? AND type = ?"
        params = (text, type)
        return query, params


    @open_close_manager
    def insert_from_json_block(self, block):
        query = '''
            INSERT INTO feed (
                type, text, date, fromtxt, fromjson, fromxml,
                city, temperature, weatheradvice, userinput
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        params = (
            block.get("type"),
            block.get("text"),
            block.get("date") if "date" in block else block.get("actual_until_date"),
            False,     # fromtxt
            True,      # fromjson
            False,     # fromxml
            block.get("city"),
            block.get("temperature"),
            None,
            False      # userinput
        )

        return query, params
    
    
    @open_close_manager
    def insert_from_xml_block(self, block):
        query = '''
            INSERT INTO feed (
                type, text, date, fromtxt, fromjson, fromxml,
                city, temperature, weatheradvice, userinput
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        block_type = block.tag
        params = {
            'type': block_type,
            'text': None,
            'date': None,
            'city': None,
            'temperature': None
        }

        for child in block:
            tag = child.tag
            text = child.text
            if tag in params:
                params[tag] = text

        final_values = (
            block_type,
            params['text'],
            params['date'],
            False,      # fromtxt
            False,      # fromjson
            True,       # fromxml
            params['city'],
            float(params['temperature']) if params['temperature'] is not None else None,
            None,
            False       # userinput
        )

        return query, final_values
