from typing import List, Dict, Any
from src.api.api import API


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии с HeadHunter по поисковому запросу

        Args:
            query: Поисковый запрос

        Returns:
            List[Dict[str, Any]]: Список вакансий
        """
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