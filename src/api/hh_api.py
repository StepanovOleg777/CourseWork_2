from typing import List, Dict, Any
import requests
from src.api.api import API


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def __make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполнить HTTP-запрос к API (приватный метод)
        """
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к API: {e}")

    def get_vacancies(self, query: str) -> List[Dict[str, Any]]:
        """
        Получить вакансии с HeadHunter по поисковому запросу
        """
        params = {
            "text": query,
            "area": 113,
            "per_page": 100,
            "page": 0
        }

        try:
            data = self.__make_request(self.__base_url, params)
            return data.get("items", [])
        except Exception as e:
            print(f"Ошибка при получении вакансий с HH: {e}")
            return []