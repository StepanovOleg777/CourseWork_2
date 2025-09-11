from typing import Dict, Optional, List, Any


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ('__name', '__url', '__salary', '__description', '__requirements')

    def __init__(self, name: str, url: str, salary: Optional[Dict[str, Any]],
                 description: str, requirements: str):
        """
        Инициализация вакансии с валидацией данных
        """
        self.__name = self.__validate_name(name)
        self.__url = self.__validate_url(url)
        self.__salary = self.__validate_salary(salary)
        self.__description = self.__validate_text(description, "описание")
        self.__requirements = self.__validate_text(requirements, "требования")

    def __validate_name(self, name: str) -> str:
        """Валидация названия вакансии"""
        if not name or not isinstance(name, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return name.strip()

    def __validate_url(self, url: str) -> str:
        """Валидация URL вакансии"""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Некорректный URL вакансии")
        return url

    def __validate_salary(self, salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Валидация зарплаты"""
        if salary is None:
            return {"from": 0, "to": 0, "currency": "RUB"}

        salary_from = salary.get("from")
        salary_to = salary.get("to")

        validated_salary = {
            "from": salary_from if isinstance(salary_from, (int, float)) and salary_from > 0 else 0,
            "to": salary_to if isinstance(salary_to, (int, float)) and salary_to > 0 else 0,
            "currency": salary.get("currency", "RUB") or "RUB"
        }
        return validated_salary

    def __validate_text(self, text: str, field_name: str) -> str:
        """Валидация текстовых полей"""
        if not text or not isinstance(text, str):
            return "Не указано"
        return text.strip()

    @property
    def name(self) -> str:
        """Название вакансии"""
        return self.__name

    @property
    def url(self) -> str:
        """URL вакансии"""
        return self.__url

    @property
    def salary(self) -> Dict[str, Any]:
        """Информация о зарплате"""
        return self.__salary

    @property
    def description(self) -> str:
        """Описание вакансии"""
        return self.__description

    @property
    def requirements(self) -> str:
        """Требования к вакансии"""
        return self.__requirements

    @property
    def avg_salary(self) -> int:
        """Средняя зарплата для сравнения"""
        salary_from = self.__salary.get("from", 0) or 0
        salary_to = self.__salary.get("to", 0) or 0

        if salary_from and salary_to:
            return (salary_from + salary_to) // 2
        elif salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        else:
            return 0

    def __str__(self) -> str:
        """Человекочитаемое представление вакансии"""
        salary_info = self.__get_salary_info()

        return (f"Вакансия: {self.__name}\n"
                f"Ссылка: {self.__url}\n"
                f"Зарплата: {salary_info}\n"
                f"Описание: {self.__description[:100]}...\n"
                f"Требования: {self.__requirements[:100]}...")

    def __get_salary_info(self) -> str:
        """Получить информацию о зарплате в читаемом формате"""
        if self.avg_salary == 0:
            return "Зарплата не указана"

        salary_from = self.__salary.get("from", 0)
        salary_to = self.__salary.get("to", 0)
        currency = self.__salary.get("currency", "RUB")

        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return "Зарплата не указана"

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать вакансию в словарь для сохранения"""
        return {
            "name": self.__name,
            "url": self.__url,
            "salary": self.__salary,
            "description": self.__description,
            "requirements": self.__requirements
        }

    # Методы сравнения по зарплате
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented

        if self.avg_salary == 0 and other.avg_salary == 0:
            return False
        if self.avg_salary == 0:
            return True
        if other.avg_salary == 0:
            return False

        return self.avg_salary < other.avg_salary

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Преобразовать список словарей в список объектов Vacancy
        """
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                name = vacancy_data.get('name', 'Без названия')
                url = vacancy_data.get('alternate_url', '')
                salary = vacancy_data.get('salary')

                snippet = vacancy_data.get('snippet', {})
                description = snippet.get('responsibility', '') or snippet.get('requirement', '')
                requirements = snippet.get('requirement', '') or description

                vacancy = cls(
                    name=name,
                    url=url,
                    salary=salary,
                    description=description,
                    requirements=requirements
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies