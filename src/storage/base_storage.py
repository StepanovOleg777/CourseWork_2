from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path


class BaseStorage(ABC):
    """Абстрактный базовый класс для работы с хранилищем данных"""

    @abstractmethod
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансии в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление вакансии из хранилища"""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистка всех данных"""
        pass