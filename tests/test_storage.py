import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.storage.json_storage import JSONStorage
from src.storage.txt_storage import TXTStorage
from src.storage.base_storage import BaseStorage


class TestJSONStorage:
    """Тесты для JSONStorage"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.test_file = "test_vacancies.json"
        self.storage = JSONStorage(self.test_file)

    def teardown_method(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_init_creates_file(self):
        """Тест, что файл создается при инициализации"""
        assert os.path.exists(self.test_file)
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data == []

    def test_add_vacancy(self):
        """Тест добавления вакансии"""
        vacancy = {
            "name": "Test Developer",
            "url": "https://test.com",
            "salary": {"from": 100000, "to": 150000},
            "description": "Test description"
        }

        self.storage.add_vacancy(vacancy)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["name"] == "Test Developer"

    def test_prevent_duplicates(self):
        """Тест предотвращения дубликатов"""
        vacancy = {
            "name": "Test Developer",
            "url": "https://test.com",
            "salary": {"from": 100000, "to": 150000},
            "description": "Test description"
        }

        # Добавляем дважды
        self.storage.add_vacancy(vacancy)
        self.storage.add_vacancy(vacancy)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1  # Дубликат не добавлен

    def test_get_vacancies(self):
        """Тест получения вакансий"""
        vacancy1 = {"name": "Dev1", "url": "url1", "salary": {}, "description": "desc1"}
        vacancy2 = {"name": "Dev2", "url": "url2", "salary": {}, "description": "desc2"}

        self.storage.add_vacancy(vacancy1)
        self.storage.add_vacancy(vacancy2)

        vacancies = self.storage.get_vacancies()
        assert len(vacancies) == 2

        filtered = self.storage.get_vacancies({"name": "Dev1"})
        assert len(filtered) == 1
        assert filtered[0]["name"] == "Dev1"

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        vacancy = {
            "name": "Test Developer",
            "url": "https://test.com",
            "salary": {},
            "description": "Test description"
        }

        self.storage.add_vacancy(vacancy)
        self.storage.delete_vacancy(vacancy)

        vacancies = self.storage.get_vacancies()
        assert len(vacancies) == 0

    def test_clear_all(self):
        """Тест очистки всех данных"""
        vacancy = {
            "name": "Test Developer",
            "url": "https://test.com",
            "salary": {},
            "description": "Test description"
        }

        self.storage.add_vacancy(vacancy)
        self.storage.clear_all()

        vacancies = self.storage.get_vacancies()
        assert len(vacancies) == 0


class TestTXTStorage:
    """Тесты для TXTStorage"""

    def setup_method(self):
        self.test_file = "test_vacancies.txt"
        self.storage = TXTStorage(self.test_file)

    def teardown_method(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_vacancy_creates_file(self):
        """Тест, что добавление вакансии создает файл"""
        vacancy = {
            "name": "Test Developer",
            "url": "https://test.com",
            "salary": {"from": 100000, "to": 150000}
        }

        self.storage.add_vacancy(vacancy)
        assert os.path.exists(self.test_file)

    def test_clear_all_removes_file(self):
        """Тест, что очистка удаляет файл"""
        vacancy = {"name": "Test", "url": "test.com", "salary": {}}
        self.storage.add_vacancy(vacancy)
        self.storage.clear_all()
        assert not os.path.exists(self.test_file)


class TestBaseStorage:
    """Тесты для абстрактного базового класса хранилища"""

    def test_abstract_methods(self):
        """Тест, что абстрактные методы требуют реализации"""
        with pytest.raises(TypeError):
            BaseStorage("test.txt")