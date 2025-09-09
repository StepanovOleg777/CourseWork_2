from typing import Dict, Optional, List, Any


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ('_name', '_url', '_salary', '_description', '_requirements')

    def __init__(self, name: str, url: str, salary: Optional[Dict[str, Any]],
                 description: str, requirements: str):
        """
        Инициализация вакансии с валидацией данных

        Args:
            name: Название вакансии
            url: Ссылка на вакансию
            salary: Информация о зарплате
            description: Описание вакансии
            requirements: Требования
        """
        self._name = self._validate_name(name)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_text(description, "описание")
        self._requirements = self._validate_text(requirements, "требования")

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

    def _validate_salary(self, salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Валидация зарплаты"""
        if salary is None:
            return {"from": 0, "to": 0, "currency": "RUB"}

        # Валидация числовых значений зарплаты
        salary_from = salary.get("from")
        salary_to = salary.get("to")

        validated_salary = {
            "from": salary_from if isinstance(salary_from, (int, float)) and salary_from > 0 else 0,
            "to": salary_to if isinstance(salary_to, (int, float)) and salary_to > 0 else 0,
            "currency": salary.get("currency", "RUB") or "RUB"
        }
        return validated_salary

    def _validate_text(self, text: str, field_name: str) -> str:
        """Валидация текстовых полей"""
        if not text or not isinstance(text, str):
            return "Не указано"
        return text.strip()

    @property
    def name(self) -> str:
        """Название вакансии"""
        return self._name

    @property
    def url(self) -> str:
        """URL вакансии"""
        return self._url

    @property
    def salary(self) -> Dict[str, Any]:
        """Информация о зарплате"""
        return self._salary

    @property
    def description(self) -> str:
        """Описание вакансии"""
        return self._description

    @property
    def requirements(self) -> str:
        """Требования к вакансии"""
        return self._requirements

    @property
    def avg_salary(self) -> int:
        """Средняя зарплата для сравнения"""
        salary_from = self._salary.get("from", 0) or 0
        salary_to = self._salary.get("to", 0) or 0

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
        salary_info = self._get_salary_info()

        return (f"Вакансия: {self._name}\n"
                f"Ссылка: {self._url}\n"
                f"Зарплата: {salary_info}\n"
                f"Описание: {self._description[:100]}...\n"
                f"Требования: {self._requirements[:100]}...")

    def _get_salary_info(self) -> str:
        """Получить информацию о зарплате в читаемом формате"""
        if self.avg_salary == 0:
            return "Зарплата не указана"

        salary_from = self._salary.get("from", 0)
        salary_to = self._salary.get("to", 0)
        currency = self._salary.get("currency", "RUB")

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
            "name": self._name,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "requirements": self._requirements
        }

    # Методы сравнения по зарплате
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented

        # Вакансии без зарплаты считаются меньшими
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

        Args:
            vacancies_data: Список вакансий в формате API

        Returns:
            List[Vacancy]: Список объектов Vacancy
        """
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                name = vacancy_data.get('name', 'Без названия')
                url = vacancy_data.get('alternate_url', '')
                salary = vacancy_data.get('salary')

                # Извлекаем описание и требования из snippet
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