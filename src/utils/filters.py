# Убираем относительные импорты, используем абсолютные
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.vacancy import Vacancy
from typing import List


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтровать вакансии по ключевым словам в описании

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        text = f"{vacancy.description} {vacancy.requirements}".lower()
        if any(word.lower() in text for word in filter_words if word):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтровать вакансии по диапазону зарплат

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат (формат: "100000-150000")

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not salary_range or not salary_range.strip():
        return vacancies

    try:
        # Обработка разных форматов ввода
        if '-' in salary_range:
            min_salary, max_salary = map(int, salary_range.split('-'))
        else:
            min_salary = int(salary_range)
            max_salary = float('inf')
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.avg_salary
        if min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортировать вакансии по убыванию зарплаты

    Args:
        vacancies: Список вакансий

    Returns:
        List[Vacancy]: Отсортированный список вакансий
    """
    return sorted(vacancies, key=lambda x: x.avg_salary, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получить топ N вакансий

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        List[Vacancy]: Топ N вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывести вакансии в читаемом формате

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy}")
        print("-" * 50)