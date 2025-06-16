from DataBase import Database
from qsort import quick_sort

class CarManager:
    def __init__(self, filename='cars.json'):
        self.db = Database(filename)
        self.fields = [
            'brand', 'model', 'year',
            'mileage', 'price',
            'acceleration', 'engine_volume'
        ]

        if 'cars' not in self.db.tables:
            self.db.create_table('cars')
            self._init_demo_data()

    def _init_demo_data(self):
        demo_cars = [
            {'brand': 'Toyota', 'model': 'Camry', 'year': 2020, 'mileage': 35000,
             'price': 25000, 'acceleration': 7.8, 'engine_volume': 2.5},
            {'brand': 'BMW', 'model': 'X5', 'year': 2019, 'mileage': 45000,
             'price': 42000, 'acceleration': 5.5, 'engine_volume': 3.0},
            {'brand': 'Tesla', 'model': 'Model 3', 'year': 2021, 'mileage': 15000,
             'price': 38000, 'acceleration': 3.1, 'engine_volume': 0.0}
        ]

        for car_id, car_data in enumerate(demo_cars, start=1):
            self.db.insert('cars', str(car_id), car_data)

        self.db.create_index('cars', 'brand')
        self.db.create_index('cars', 'price')

    def sort_cars(self, sort_by='price'):
        cars = list(self.db.tables['cars'].values())

        if sort_by == 'price':
            return quick_sort(cars, key=self._get_price)
        else:
            return quick_sort(cars, key=self._get_negative_year)

    def _get_price(self, car):
        return car['price']

    def _get_negative_year(self, car):
        return -car['year']

    def add_car(self):
        new_car = {}
        print("\nДобавление новой машины:")

        for field in self.fields:
            value = input(f"{field}: ")
            try:
                if field in ['year', 'mileage']:
                    value = int(value)
                if field in ['price', 'acceleration', 'engine_volume']:
                    value = float(value)
                new_car[field] = value
            except ValueError:
                print(f'Неверное значение в {field}!')

        if self.db.tables['cars']:
            new_id = str(max(map(int, self.db.tables['cars'].keys())) + 1)
        else:
            new_id = '1'

        self.db.insert('cars', new_id, new_car)
        print('Ваша машина добавлена!')
