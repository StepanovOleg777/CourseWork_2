from typing import Dict, List, Any
from .base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")

    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получение вакансий с hh.ru по поисковому запросу"""
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,  # Россия
            "only_with_salary": True
        }

        response = self._connect_to_api(self.base_url, params)
        data = response.json()

        return data.get("items", [])