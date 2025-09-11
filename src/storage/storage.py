from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.vacancy import Vacancy


class Storage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получить вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из файла"""
        pass