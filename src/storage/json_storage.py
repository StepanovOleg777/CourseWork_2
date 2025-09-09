import json
from typing import List, Dict, Any
from pathlib import Path
from .base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, file_path: str = "data/vacancies.json"):
        super().__init__(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Проверка наличия файла"""
        if not self.file_path.exists():
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_data(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _is_duplicate(self, new_vacancy: Dict[str, Any], existing_data: List[Dict[str, Any]]) -> bool:
        """Проверка является ли вакансия дубликатом"""
        for vacancy in existing_data:
            if (vacancy['name'] == new_vacancy['name'] and
                    vacancy['url'] == new_vacancy['url']):
                return True
        return False

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансий в JSON-файл"""
        data = self._read_data()

        if not self._is_duplicate(vacancy, data):
            data.append(vacancy)
            self._write_data(data)

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        data = self._read_data()

        if not criteria:
            return data

        filtered_data = []
        for vacancy in data:
            match = True
            for key, value in criteria.items():
                if key not in vacancy or vacancy[key] != value:
                    match = False
                    break
            if match:
                filtered_data.append(vacancy)

        return filtered_data

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление вакансий из JSON-файла"""
        data = self._read_data()
        data = [v for v in data if not (
                v['name'] == vacancy['name'] and v['url'] == vacancy['url']
        )]
        self._write_data(data)

    def clear_all(self) -> None:
        """Очистка всех данных"""
        self._write_data([])