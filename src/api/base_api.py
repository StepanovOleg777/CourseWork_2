from abc import ABC, abstractmethod
import requests
from typing import Dict, List, Any


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с API вакансий"""

    @abstractmethod
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получить вакансии по поисковому запросу"""
        pass

    def _connect_to_api(self, url: str, params: Dict[str, Any]) -> requests.Response:
        """Приватный метод для подключения к API"""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")