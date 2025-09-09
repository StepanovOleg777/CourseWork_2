import pytest
import requests
from unittest.mock import Mock, patch
from src.api.hh_api import HeadHunterAPI
from src.api.base_api import BaseAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_init(self):
        """Тест инициализации API"""
        api = HeadHunterAPI()
        assert api.base_url == "https://api.hh.ru/vacancies"

    @patch('src.api.base_api.requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "description": "Test description",
                    "snippet": {"requirement": "Python experience"}
                }
            ]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        mock_get.assert_called_once()

    @patch('src.api.base_api.requests.get')
    def test_get_vacancies_empty_response(self, mock_get):
        """Тест пустого ответа от API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Nonexistent")

        assert len(vacancies) == 0

    @patch('src.api.base_api.requests.get')
    def test_get_vacancies_api_error(self, mock_get):
        """Тест ошибки API"""
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        api = HeadHunterAPI()

        with pytest.raises(ConnectionError):
            api.get_vacancies("Python")


class TestBaseAPI:
    """Тесты для абстрактного базового класса API"""

    def test_abstract_methods(self):
        """Тест что абстрактные методы требуют реализации"""
        with pytest.raises(TypeError):
            BaseAPI("https://test.com")