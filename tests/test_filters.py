import pytest
from src.utils.filters import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)
from src.models.vacancy import Vacancy
from io import StringIO
import sys


class TestFilters:
    """Тесты для функций фильтрации"""

    def setup_method(self):
        """Создание тестовых вакансий"""
        self.vacancies = [
            Vacancy(
                "Python Developer",
                "https://hh.ru/vacancy/1",
                {"from": 100000, "to": 150000, "currency": "RUR"},
                "Разработка на Python и Django",
                "Опыт работы с Python 3+ года"
            ),
            Vacancy(
                "Java Developer",
                "https://hh.ru/vacancy/2",
                {"from": 120000, "to": 180000, "currency": "RUR"},
                "Разработка на Java и Spring",
                "Опыт работы с Java 4+ года"
            ),
            Vacancy(
                "JavaScript Developer",
                "https://hh.ru/vacancy/3",
                {"from": 90000, "to": 130000, "currency": "RUR"},
                "Разработка на React и Node.js",
                "Опыт работы с JavaScript 2+ года"
            )
        ]

    def test_filter_vacancies_with_keywords(self):
        """Тест фильтрации по ключевым словам"""
        filtered = filter_vacancies(self.vacancies, ["python", "django"])
        assert len(filtered) == 1
        assert filtered[0].name == "Python Developer"

    def test_filter_vacancies_empty_keywords(self):
        """Тест фильтрации с пустыми ключевыми словами"""
        filtered = filter_vacancies(self.vacancies, [])
        assert len(filtered) == len(self.vacancies)

    def test_filter_vacancies_no_matches(self):
        """Тест фильтрации без совпадений"""
        filtered = filter_vacancies(self.vacancies, ["ruby", "php"])
        assert len(filtered) == 0

    def test_get_vacancies_by_min_salary(self):
        """Тест фильтрации по минимальной зарплате"""
        filtered = get_vacancies_by_salary(self.vacancies, "130000")
        assert len(filtered) == 1
        assert filtered[0].name == "Java Developer"

    def test_get_vacancies_by_salary_invalid_input(self):
        """Тест фильтрации с некорректным вводом"""
        filtered = get_vacancies_by_salary(self.vacancies, "invalid")
        assert len(filtered) == len(self.vacancies)

    def test_sort_vacancies(self):
        """Тест сортировки вакансий"""
        sorted_list = sort_vacancies(self.vacancies)
        salaries = [v.avg_salary for v in sorted_list]
        assert salaries == sorted(salaries, reverse=True)
        assert sorted_list[0].name == "Java Developer"  # Самая высокая зарплата

        top_0 = get_top_vacancies(self.vacancies, 0)
        assert len(top_0) == 0

        top_10 = get_top_vacancies(self.vacancies, 10)
        assert len(top_10) == len(self.vacancies)

    def test_print_empty_vacancies(self, capsys):
        """Тест вывода пустого списка вакансий"""
        print_vacancies([])
        captured = capsys.readouterr()
        assert "Вакансии не найдены" in captured.out