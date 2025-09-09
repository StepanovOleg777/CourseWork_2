from typing import List, Optional
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтровать вакансии по ключевым словам в описании

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов для фильтрации

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Объединяем описание и требования для поиска
        text = f"{vacancy.description} {vacancy.requirements}".lower()

        # Проверяем наличие всех ключевых слов
        if all(word.lower() in text for word in filter_words if word.strip()):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтровать вакансии по диапазону зарплат

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат в формате "100000-150000"

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not salary_range or not salary_range.strip():
        return vacancies

    try:
        # Парсим диапазон зарплат
        range_parts = salary_range.replace(' ', '').split('-')
        if len(range_parts) == 2:
            min_salary = int(range_parts[0])
            max_salary = int(range_parts[1])
        else:
            # Если указана одна цифра, ищем вакансии с зарплатой выше
            min_salary = int(range_parts[0])
            max_salary = float('inf')
    except ValueError:
        print("Некорректный формат диапазона зарплат. Используйте формат: 100000-150000")
        return vacancies

    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.avg_salary
        if min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Отсортировать вакансии по убыванию зарплаты

    Args:
        vacancies: Список вакансий для сортировки

    Returns:
        List[Vacancy]: Отсортированный список вакансий
    """
    return sorted(vacancies, key=lambda x: x.avg_salary, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получить топ N вакансий по зарплате

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        List[Vacancy]: Топ N вакансий
    """
    if not vacancies or top_n <= 0:
        return []

    return vacancies[:top_n]