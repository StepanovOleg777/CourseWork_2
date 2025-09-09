import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.filters import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies


def user_interaction():
    """
    Основная функция взаимодействия с пользователем
    """
    print("=== Анализатор вакансий с hh.ru ===")

    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    # Ввод данных от пользователя
    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: ").strip() or "10")
    except ValueError:
        print("Некорректное число. Будет использовано значение по умолчанию: 10")
        top_n = 10

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ").strip()

    print("\n⏳ Получаем вакансии с hh.ru...")

    try:
        # Получение вакансий с API
        vacancies_data = hh_api.get_vacancies(search_query, per_page=50)
        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        if not vacancies:
            print("По вашему запросу вакансий не найдено.")
            return

        # Сохранение в файл
        for vacancy in vacancies:
            storage.add_vacancy(vacancy.to_dict())

        print(f"✅ Получено и сохранено {len(vacancies)} вакансий")

        # Фильтрация и сортировка
        filtered_vacancies = filter_vacancies(vacancies, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Вывод результатов
        print(f"\n🎯 Топ {len(top_vacancies)} вакансий:")
        print_vacancies(top_vacancies)

        # Дополнительная информация
        print(f"\n📊 Статистика:")
        print(f"Всего получено: {len(vacancies)} вакансий")
        print(f"После фильтрации: {len(filtered_vacancies)} вакансий")
        print(f"После фильтрации по зарплате: {len(ranged_vacancies)} вакансий")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")


def additional_features():
    """
    Дополнительные функции для работы с сохраненными вакансиями
    """
    storage = JSONStorage()

    print("\n=== Дополнительные функции ===")
    print("1. Показать все сохраненные вакансии")
    print("2. Поиск по ключевым словам")
    print("3. Очистить все данные")
    print("4. Выход")

    choice = input("Выберите опцию (1-4): ").strip()

    if choice == "1":
        vacancies_data = storage.get_vacancies()
        vacancies = [Vacancy.from_dict(data) for data in vacancies_data]
        print_vacancies(vacancies)

    elif choice == "2":
        keyword = input("Введите ключевое слово для поиска: ").strip()
        vacancies_data = storage.get_vacancies()
        vacancies = [Vacancy.from_dict(data) for data in vacancies_data]
        filtered = filter_vacancies(vacancies, [keyword])
        print_vacancies(filtered)

    elif choice == "3":
        confirm = input("Вы уверены, что хотите очистить все данные? (y/n): ").strip().lower()
        if confirm == 'y':
            storage.clear_all()
            print("Все данные очищены.")

    elif choice == "4":
        print("Выход...")

    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    try:
        user_interaction()
        additional_features()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")