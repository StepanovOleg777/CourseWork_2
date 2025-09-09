from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.vacancy import Vacancy


class Storage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получение вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        pass

    # Методы для будущей интеграции с БД (заглушки)
    @abstractmethod
    def add_vacancies(self, query: str, vacancies: List[Vacancy]) -> None:
        """Добавление вакансии по запросу (для будущего использования)"""
        pass

    @abstractmethod
    def get_vacancies_by_query(self, query: str) -> List[Dict[str, Any]]:
        """Получение вакансий по запросу (для будущего использования)"""
        pass