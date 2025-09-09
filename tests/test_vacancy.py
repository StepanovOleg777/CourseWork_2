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
    vacancy1 = Vacancy("Dev1", "url1", {"from": 100000}, "desc1", "req1")
    vacancy2 = Vacancy("Dev2", "url2", {"from": 150000}, "desc2", "req2")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 != vacancy2


def test_vacancy_validation():
    """Тест валидации данных"""
    with pytest.raises(ValueError):
        Vacancy("", "url", {}, "desc", "req")