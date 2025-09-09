from typing import List, Dict, Any
from src.api.api import API


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """Получение вакансий с HeadHunter по поисковому запросу"""
        params = {
            "text": query,
            "area": 113,  # Россия
            "per_page": 100,
            "page": 0
        }

        try:
            # Используем приватный метод из абстрактного класса
            data = self._make_request(self._base_url, params)
            return data.get("items", [])
        except Exception as e:
            print(f"Ошибка при получении вакансий с HH: {e}")
            return []