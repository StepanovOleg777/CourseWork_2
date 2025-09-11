from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class API(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""
        pass