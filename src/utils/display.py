from typing import List
from src.models.vacancy import Vacancy


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывести вакансии в удобочитаемом формате

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены")
        return

    print(f"\nНайдено {len(vacancies)} вакансий:\n")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"=== Вакансия {i} ===")
        print(vacancy)
        print("-" * 50)


def print_vacancy_details(vacancy: Vacancy) -> None:
    """
    Вывести подробную информацию о вакансии

    Args:
        vacancy: Вакансия для вывода
    """
    print(f"\n=== Детальная информация ===")
    print(f"Название: {vacancy.name}")
    print(f"Ссылка: {vacancy.url}")

    # Информация о зарплате
    salary = vacancy.salary
    if vacancy.avg_salary > 0:
        if salary.get('from') and salary.get('to'):
            print(f"Зарплата: {salary['from']} - {salary['to']} {salary.get('currency', 'RUB')}")
        elif salary.get('from'):
            print(f"Зарплата: от {salary['from']} {salary.get('currency', 'RUB')}")
        elif salary.get('to'):
            print(f"Зарплата: до {salary['to']} {salary.get('currency', 'RUB')}")
    else:
        print("Зарплата: Не указана")

    print(f"\nОписание:\n{vacancy.description}")
    print(f"\nТребования:\n{vacancy.requirements}")
    print("=" * 50)