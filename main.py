from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_saver import JSONSaver
from src.utils.filters import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies
from src.utils.display import print_vacancies, print_vacancy_details


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль
    """
    print("=== Парсер вакансий с HeadHunter ===")
    print("Программа позволяет искать вакансии, фильтровать и сортировать их")

    # Создаем экземпляры классов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Ввод параметров поиска
    search_query = input("\nВведите поисковый запрос для запроса вакансий из hh.ru: ").strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым!")
        return

    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        if top_n <= 0:
            print("Количество должно быть положительным числом!")
            return
    except ValueError:
        print("Некорректное число!")
        return

    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ").strip()

    print(f"\nИщу вакансии по запросу: '{search_query}'...")

    # Получаем вакансии с API
    hh_vacancies_data = hh_api.get_vacancies(search_query)

    if not hh_vacancies_data:
        print("По вашему запросу вакансии не найдены.")
        return

    # Преобразуем в объекты
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)
    print(f"Найдено {len(vacancies_list)} вакансий")

    # Сохраняем все вакансии
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    # Применяем фильтры и сортировку
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Выводим результаты
    print_vacancies(top_vacancies)

    # Дополнительные возможности
    if top_vacancies:
        try:
            choice = input("\nХотите посмотреть детальную информацию о вакансии? (введите номер или 'нет'): ")
            if choice.lower() != 'нет':
                vacancy_num = int(choice) - 1
                if 0 <= vacancy_num < len(top_vacancies):
                    print_vacancy_details(top_vacancies[vacancy_num])
                else:
                    print("Неверный номер вакансии")
        except ValueError:
            print("Неверный ввод")


if __name__ == "__main__":
    user_interaction()