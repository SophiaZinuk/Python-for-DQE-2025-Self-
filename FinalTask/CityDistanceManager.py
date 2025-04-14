import pyodbc
import math
from functools import wraps


class CityDistanceManager:

    def open_close_manager(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            con = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};Direct=True;Database=citycoordinates.db;String Types=Unicode')
            cursor = con.cursor()
            try:
                result = func(self, cursor, *args, **kwargs)

                if result is None or (isinstance(result, tuple) and result[0] is None):
                    return

                return result
            finally:
                cursor.commit()
                cursor.close()
                con.close()
        return wrapper
    

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
    

    @open_close_manager
    def get_distance_between_cities(self, cursor, city1, city2):
        self.create_table()

        def get_coords(city):
            cursor.execute("SELECT latitude, longitude FROM citycoordinates WHERE city = ?", (city.lower(),))
            return cursor.fetchone()

        # Handle each city
        for city in [city1, city2]:
            row = get_coords(city)
            if not row:
                print(f"City '{city}' not found in DB.")
                if not self.duplication_validation(city):
                    lat = CityDistanceManager.input_latitude_with_validation(f"Enter latitude for {city}: ")
                    lon = CityDistanceManager.input_longitude_with_validation(f"Enter longitude for {city}: ")
                    cursor.execute(
                    "INSERT INTO citycoordinates (city, latitude, longitude) VALUES (?, ?, ?)",
                    (city.lower(), lat, lon)
                    )

        row1 = get_coords(city1)
        row2 = get_coords(city2)

        if not row1 or not row2:
            print("Still missing data. Cannot calculate distance.")
            return None

        lat1, long1 = map(float, row1)
        lat2, long2 = map(float, row2)

        return self.calculate_distance(lat1, long1, lat2, long2)


    @open_close_manager
    def create_table(self, cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS citycoordinates (
            city varchar(64),
            latitude varchar(10),
            longitude varchar(11)
        );''')


    @open_close_manager
    def run_to_check(self, cursor):
        cursor.execute("SELECT * FROM citycoordinates")
        rows = cursor.fetchall()
        return rows
    

    @open_close_manager
    def insert_data(self, cursor, city, latitude, longitude):
        query = '''
            INSERT INTO citycoordinates (
                city, latitude, longitude
            ) VALUES (?, ?, ?)
        '''
        params = (
            city.lower(),
            latitude,
            longitude
        )
        return query, params


    @open_close_manager
    def duplication_validation(self, cursor, city):
        cursor.execute("SELECT COUNT(*) FROM citycoordinates WHERE city = ?", (city.lower(),))
        result = cursor.fetchone()
        return result[0] > 0


    @staticmethod
    def input_latitude_with_validation(message):
        while True:
            lat = input(message)
            try:
                lat = float(lat.strip())
                if -90 <= lat <= 90:
                    return lat
            except:
                pass
            print("Invalid format or range. Enter latitude again.")


    @staticmethod
    def input_longitude_with_validation(message):
        while True:
            lon = input(message)
            try:
                lon = float(lon.strip())
                if -180 <= lon <= 180:
                    return lon
            except:
                pass
            print("Invalid format or range. Enter longitude again.")


