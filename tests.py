import os
from manager import CarManager


def test_car_manager_basic_operations():
    test_db = "test_db.json"

    if os.path.exists(test_db):
        os.remove(test_db)

    manager = CarManager(test_db)

    try:
        cars = manager.db.get_all('cars')
        assert len(cars) == 3, "Демо-данные не загрузились"

        test_car = {
            'brand': 'TestBrand',
            'model': 'TestModel',
            'year': 2023,
            'mileage': 0,
            'price': 10000,
            'acceleration': 5.0,
            'engine_volume': 1.5
        }

        manager.db.insert('cars', 'test_id', test_car)

        car = manager.db.get('cars', 'test_id')
        assert car is not None, "Машина не добавилась в базу"
        assert car['brand'] == 'TestBrand', "Неверные данные машины"

        results = manager.db.query('cars', 'brand', 'TestBrand')
        assert len(results) == 1, "Поиск по марке не работает"
        assert results[0]['model'] == 'TestModel', "Неверный результат поиска"

        sorted_cars = manager.sort_cars('price')
        prices = [car['price'] for car in sorted_cars]
        assert prices == sorted(prices), "Сортировка по цене не работает"

        sorted_cars = manager.sort_cars('year')
        years = [car['year'] for car in sorted_cars]
        assert years == sorted(years, reverse=True), "Сортировка по году не работает"

        print("Все базовые тесты CarManager пройдены успешно!")

    finally:
        # Удаляем временный файл после тестов
        if os.path.exists(test_db):
            os.remove(test_db)


def test_menu_functions():
    test_db = "test_menu_db.json"

    if os.path.exists(test_db):
        os.remove(test_db)

    manager = CarManager(test_db)

    try:
        all_cars = manager.db.get_all('cars')
        assert isinstance(all_cars, dict), "get_all должен возвращать словарь"

        test_car = {
            'brand': 'MenuTest',
            'model': 'MenuModel',
            'year': 2022,
            'mileage': 1000,
            'price': 20000,
            'acceleration': 7.5,
            'engine_volume': 2.0
        }
        manager.db.insert('cars', 'menu_test_id', test_car)

        car = manager.db.get('cars', 'menu_test_id')
        assert car['price'] == 20000, "Ошибка при проверке добавленной машины"

        print("Тесты функций меню пройдены успешно!")

    finally:
        if os.path.exists(test_db):
            os.remove(test_db)


def test_index_operations():
    test_db = "test_index_db.json"

    if os.path.exists(test_db):
        os.remove(test_db)

    manager = CarManager(test_db)

    try:
        assert 'brand' in manager.db.indexes['cars'], "Индекс по марке не создан"
        assert 'price' in manager.db.indexes['cars'], "Индекс по цене не создан"

        bmw_cars = manager.db.query('cars', 'brand', 'BMW')
        assert len(bmw_cars) == 1, "Неверное количество BMW в демо-данных"
        assert bmw_cars[0]['model'] == 'X5', "Неверная модель BMW"

        print("Тесты работы с индексами пройдены успешно!")

    finally:
        if os.path.exists(test_db):
            os.remove(test_db)


if __name__ == "__main__":
    test_car_manager_basic_operations()
    test_menu_functions()
    test_index_operations()
    print("Все тесты пройдены успешно!")