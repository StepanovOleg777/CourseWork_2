import json
import os
from typing import List, Dict, Any
from src.models.vacancy import Vacancy
from src.storage.storage import Storage


class JSONSaver(Storage):
    """Класс для сохранения информации о вакансиях в JSON-файл"""

    def __init__(self, filename: str = "vacancies.json"):
        self.__filename = filename
        self.__ensure_file_exists()

    def __ensure_file_exists(self) -> None:
        """Создать файл, если он не существует"""
        if not os.path.exists(self.__filename):
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def __read_vacancies(self) -> List[Dict[str, Any]]:
        """Прочитать вакансии из файла"""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def __write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Записать вакансии в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в файл"""
        vacancies = self.__read_vacancies()
        vacancy_dict = vacancy.to_dict()

        if not any(v.get('url') == vacancy_dict.get('url') for v in vacancies):
            vacancies.append(vacancy_dict)
            self.__write_vacancies(vacancies)
            print(f"Вакансия '{vacancy.name}' добавлена в файл")
        else:
            print("Вакансия уже существует в файле")

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Получить вакансии по критериям"""
        vacancies = self.__read_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            matches = True

            if 'keyword' in criteria and criteria['keyword']:
                keyword = criteria['keyword'].lower()
                text = f"{vacancy.get('description', '')} {vacancy.get('requirements', '')}".lower()
                if keyword not in text:
                    matches = False

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
        """Удалить вакансию из файла"""
        vacancies = self.__read_vacancies()
        original_count = len(vacancies)

        vacancies = [v for v in vacancies if v.get('url') != vacancy.url]

        if len(vacancies) < original_count:
            self.__write_vacancies(vacancies)
            print(f"Вакансия '{vacancy.name}' удалена из файла")
        else:
            print("Вакансия не найдена в файле")