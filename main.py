from manager import CarManager


def show_menu():
    manager = CarManager()

    while True:
        print("\n=== Автомобильная база данных ===")
        print("1. Показать все автомобили")
        print("2. Добавить новый автомобиль")
        print("3. Поиск по марке")
        print("4. Сортировка по цене (возрастание)")
        print("5. Сортировка по году выпуска (убывание)")
        print("6. Выход")

        choice = int(input("Выберите действие (1-6): "))

        if choice == 1:
            cars = manager.db.get_all('cars')
            if not cars:
                print('В базе нет машин')
                continue

            print('Список автомобилей:')
            for car_id, car in cars.items():
                print(f'\nID: {car_id}')
                for field, value in car.items():
                    print(f'{field}: {value}')

        elif choice == 2:
            print("\nДобавление нового автомобиля:")
            manager.add_car()

        elif choice == 3:
            brand = input('Введите марку: ')
            results = manager.db.query('cars', 'brand', brand)

            if not results:
                print('Нет результатов по Вашему запросу((')
                continue

            print(f'Результаты по запросу {brand}: ')
            for car in results:
                print('\n' + '\n'.join(f'{k}: {v}' for k, v in car.items()))

        elif choice == 4:
            sorted_cars = manager.sort_cars('price')
            print("\nАвтомобили по цене (от дешёвых к дорогим):")
            for car in sorted_cars:
                print(f"{car['brand']} {car['model']} - {car['price']}$")

        elif choice == 5:
            sorted_cars = manager.sort_cars('year')
            print("\nАвтомобили по году выпуска (новые сначала):")
            for car in sorted_cars:
                print(f"{car['year']} {car['brand']} {car['model']}")

        elif choice == 6:
            print("\nВыход из программы...")
            break

        else:
            print("\nНеверный ввод! Пожалуйста, выберите пункт от 1 до 6.")

if __name__ == "__main__":
    show_menu()
