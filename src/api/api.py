from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class API(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""
        pass

    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить HTTP-запрос к API (приватный метод)"""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Проверка статус-кода
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к API: {e}")