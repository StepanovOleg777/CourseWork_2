from __future__ import annotations
from typing import Dict, Any, List
import re


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ('_name', '_url', '_salary', '_description', '_requirements')

    def __init__(self, name: str, url: str, salary: Dict[str, Any],
                 description: str, requirements: str = ""):
        self._name = self._validate_name(name)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_description(description)
        self._requirements = self._validate_requirements(requirements)

    def _validate_name(self, name: str) -> str:
        """Валидация названия вакансии"""
        if not name or not isinstance(name, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return name.strip()

    def _validate_url(self, url: str) -> str:
        """Валидация URL вакансии"""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Некорректный URL вакансии")
        return url

    def _validate_salary(self, salary: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация данных о зарплате"""
        if not salary:
            return {"from": 0, "to": 0, "currency": "RUR"}

        validated_salary = {
            "from": salary.get("from", 0) or 0,
            "to": salary.get("to", 0) or 0,
            "currency": salary.get("currency", "RUR") or "RUR"
        }

        return validated_salary

    def _validate_description(self, description: str) -> str:
        """Валидация описания вакансии"""
        if not description or not isinstance(description, str):
            return "Описание отсутствует"
        return description.strip()

    def _validate_requirements(self, requirements: str) -> str:
        """Валидация требований вакансии"""
        if not requirements or not isinstance(requirements, str):
            return "Требования отсутствуют"
        return requirements.strip()

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> Dict[str, Any]:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    @property
    def avg_salary(self) -> float:
        """Средняя зарплата"""
        from_val = self._salary["from"] or 0
        to_val = self._salary["to"] or 0

        if from_val and to_val:
            return (from_val + to_val) / 2
        elif from_val:
            return from_val
        elif to_val:
            return to_val
        else:
            return 0.0

    def __str__(self) -> str:
        salary_info = self._format_salary()
        return (f"Вакансия: {self._name}\n"
                f"Ссылка: {self._url}\n"
                f"Зарплата: {salary_info}\n"
                f"Описание: {self._description[:100]}...\n"
                f"Требования: {self._requirements[:100]}...")

    def _format_salary(self) -> str:
        """Форматирование информации о зарплате"""
        if not self._salary["from"] and not self._salary["to"]:
            return "Зарплата не указана"

        from_val = self._salary["from"]
        to_val = self._salary["to"]
        currency = self._salary["currency"]

        if from_val and to_val:
            return f"{from_val:,} - {to_val:,} {currency}"
        elif from_val:
            return f"от {from_val:,} {currency}"
        elif to_val:
            return f"до {to_val:,} {currency}"
        else:
            return "Зарплата не указана"

    # Методы сравнения
    def __eq__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "name": self._name,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "requirements": self._requirements
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """Создание объекта из словаря"""
        return cls(
            name=data["name"],
            url=data["url"],
            salary=data["salary"],
            description=data["description"],
            requirements=data.get("requirements", "")
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Преобразование списка словарей в список объектов Vacancy"""
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                salary = vacancy_data.get("salary") or {}
                vacancy = cls(
                    name=vacancy_data.get("name", ""),
                    url=vacancy_data.get("alternate_url", ""),
                    salary=salary,
                    description=vacancy_data.get("description", ""),
                    requirements=vacancy_data.get("snippet", {}).get("requirement", "")
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies