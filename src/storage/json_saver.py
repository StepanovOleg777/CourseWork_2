import json
import os
from typing import List, Dict, Any
from src.models.vacancy import Vacancy
from src.storage.storage import Storage


class JSONSaver(Storage):
    """Класс для сохранения информации о вакансиях в JSON-файл"""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создать файл, если он не существует"""
        if not os.path.exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Прочитать вакансии из файла"""
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Записать вакансии в файл"""
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавить вакансию в файл (не сохраняет дубликаты)

        Args:
            vacancy: Объект вакансии для добавления
        """
        vacancies = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты по URL
        if not any(v.get('url') == vacancy_dict.get('url') for v in vacancies):
            vacancies.append(vacancy_dict)
            self._write_vacancies(vacancies)
            print(f"Вакансия '{vacancy.name}' добавлена в файл")
        else:
            print("Вакансия уже существует в файле")

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Получить вакансии по критериям

        Args:
            criteria: Словарь с критериями фильтрации

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список вакансий
        """
        vacancies = self._read_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True

            # Фильтрация по ключевым словам в описании
            if 'keyword' in criteria and criteria['keyword']:
                keyword = criteria['keyword'].lower()
                text = f"{vacancy.get('description', '')} {vacancy.get('requirements', '')}".lower()
                if keyword not in text:
                    matches = False

            # Фильтрация по зарплате
            if 'min_salary' in criteria and criteria['min_salary'] > 0:
                salary = vacancy.get('salary', {})
                salary_from = salary.get('from', 0) or 0
                salary_to = salary.get('to', 0) or 0
                avg_salary = (salary_from + salary_to) // 2 if salary_from and salary_to else max(salary_from,
                                                                                                  salary_to)

                if avg_salary < criteria['min_salary']:
                    matches = False

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию из файла

        Args:
            vacancy: Объект вакансии для удаления
        """
        vacancies = self._read_vacancies()
        original_count = len(vacancies)

        # Удаляем вакансию по URL
        vacancies = [v for v in vacancies if v.get('url') != vacancy.url]

        if len(vacancies) < original_count:
            self._write_vacancies(vacancies)
            print(f"Вакансия '{vacancy.name}' удалена из файла")
        else:
            print("Вакансия не найдена в файле")

    # Заглушки для будущей интеграции
    def add_vacancies(self, query: str, vacancies: List[Vacancy]) -> None:
        """Добавить вакансии по запросу (заглушка для будущего использования)"""
        for vacancy in vacancies:
            self.add_vacancy(vacancy)

    def get_vacancies_by_query(self, query: str) -> List[Dict[str, Any]]:
        """Получить вакансии по запросу (заглушка для будущего использования)"""
        return self.get_vacancies({'keyword': query})