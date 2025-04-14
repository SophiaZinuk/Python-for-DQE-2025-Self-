from CityDistanceManager import CityDistanceManager


if __name__ == '__main__': 
    print('Hello! This program will help you to calculate straight-line distance between different cities based on coordinates!')
    run = True

    manager = CityDistanceManager()

    while run:
        action = input('\nTo continue enter GO \nTo quit enter QUIT ')
        if action == 'QUIT':
            run = False
        elif action == 'GO':
            city1 = input('Provide first city: ')
            city2 = input('Provide second city: ')
            distance = manager.get_distance_between_cities(city1, city2)
            if distance is not None:
                print(f"Distance between {city1.lower().capitalize()} and {city2.lower().capitalize()}: {distance:.2f} km")
                # for row in manager.run_to_check():
                #     print(row)
            else:
                print("Could not calculate distance due to missing data.")

