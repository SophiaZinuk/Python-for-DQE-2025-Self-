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
    def create_tables(self):
        return '''  CREATE TABLE IF NOT EXISTS news (
            text text,
            date date,
            city varchar(32) );
                    CREATE TABLE IF NOT EXISTS weatherforecast (
            text text,
            date date,
            city varchar(32),
            temperature float );
                    CREATE TABLE IF NOT EXISTS privatead (
            text text,
            date date );
                    '''

    @open_close_manager
    def run_to_check(self):
        return f'SELECT * FROM news'
    
    @open_close_manager
    def run_to_check_1(self):
        return f'SELECT * FROM privatead'
    
    @open_close_manager
    def insert_from_txt_block(self, block_type, text):
        query = f'''
            INSERT INTO {block_type} (
                text
            ) VALUES (?)
        '''
        params = (
            text
        )
        return query, params


    @open_close_manager
    def duplication_validation(self, text, type):
        query = f"SELECT COUNT(*) FROM {type} WHERE text = ?"
        params = (text)
        return query, params


    @open_close_manager
    def insert_from_json_block(self, block):
        match block.get("type"):
            case "news":
                query = ''' INSERT INTO news (
                text, date, city
            ) VALUES (?, ?, ?) '''
                
                params = (
                    block.get("text"),
                    block.get("date"),
                    block.get("city")
                )

            case "privatead":
                query = ''' INSERT INTO privatead (
                text, date
            ) VALUES (?, ?) '''
                
                params = (
                    block.get("text"),
                    block.get("date")
                )

            case "weatherforecast":
                query = ''' INSERT INTO weatherforecast (
                text, date, city, temperature
            ) VALUES (?, ?, ?, ?) '''
                
                params = (
                    block.get("text"),
                    block.get("date"),
                    block.get("city"),
                    block.get("temperature")
                )

        return query, params
    
    
    @open_close_manager
    def insert_from_xml_block(self, block):

        block_type = block.tag
        params = {
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

        match block_type:
            case "news":
                query = '''
                    INSERT INTO news (
                    text, date, city
                    ) VALUES (?, ?, ?)
                '''

                final_values = (
                    params['text'],
                    params['date'],
                    params['city']
                    )
            case "privatead":
                query = '''
                    INSERT INTO privatead (
                    text, date
                    ) VALUES (?, ?)
                '''

                final_values = (
                    params['text'],
                    params['date']
                    )
                
            case "weatherforecast":
                query = '''
                    INSERT INTO weatherforecast (
                    text, date, city, temperature
                    ) VALUES (?, ?, ?, ?)
                '''

                final_values = (
                    params['text'],
                    params['date'],
                    params['city'],
                    float(params['temperature'])
                    )

        return query, final_values
