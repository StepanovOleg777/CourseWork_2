from typing import List, Dict, Any
from pathlib import Path
from .base_storage import BaseStorage


class TXTStorage(BaseStorage):
    """Класс для работы с TXT-файлом (дополнительный формат)"""

    def __init__(self, file_path: str = "data/vacancies.txt"):
        super().__init__(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление вакансий в TXT-файл"""
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(f"Вакансия: {vacancy['name']}\n")
            f.write(f"Ссылка: {vacancy['url']}\n")
            f.write(f"Зарплата: {vacancy['salary']}\n")
            f.write("---\n")

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получение вакансий из TXT-файла"""
        # Для TXT формат сложнее, возвращаем пустой список
        return []

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаление вакансий из TXT-файла"""
        # Для TXT сложно реализовать удаление конкретной вакансии
        pass

    def clear_all(self) -> None:
        """Очистка всех данных"""
        if self.file_path.exists():
            self.file_path.unlink()