import pytest
from src.models.vacancy import Vacancy


def test_vacancy_creation():
    """Тест создания вакансии"""
    vacancy = Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы 3+ года"
    )

    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.avg_salary == 125000


def test_vacancy_comparison():
    """Тест сравнения вакансий"""
    # Используем корректные URL
    vacancy1 = Vacancy("Dev1", "https://hh.ru/vacancy/1", {"from": 100000}, "desc1", "req1")
    vacancy2 = Vacancy("Dev2", "https://hh.ru/vacancy/2", {"from": 150000}, "desc2", "req2")
    vacancy3 = Vacancy("Dev3", "https://hh.ru/vacancy/3", {"from": 80000}, "desc3", "req3")

    # Тестируем сравнение
    assert vacancy2 > vacancy1
    assert vacancy1 > vacancy3
    assert vacancy2 >= vacancy1
    assert vacancy1 <= vacancy2

    # Тестируем равенство (когда зарплаты одинаковые)
    vacancy4 = Vacancy("Dev4", "https://hh.ru/vacancy/4", {"from": 100000}, "desc4", "req4")
    assert vacancy1 == vacancy4


def test_vacancy_validation():
    """Тест валидации данных"""
    with pytest.raises(ValueError):
        Vacancy("", "url", {}, "desc", "req")