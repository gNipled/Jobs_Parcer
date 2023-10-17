from abc import ABC, abstractmethod
import os
import json
from src.vacancy import Vacancy


class FileSaver(ABC):
    """
    Abstract class for file savers
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary: int):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy, vac_list: list):
        pass


class JSONSaver(FileSaver):
    """
    Class for JSON saver, that saves vacancy information in .json file in vacancies folder
    """
    def __init__(self):
        self.file_name = os.path.join('../', 'Vacancies', 'vacancies.json')

    def __str__(self):
        return f'saver for .json files'

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def add_vacancy(self, vacancy):
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(vacancy.get_json(), file, ensure_ascii=False)
        else:
            vac_list = self.get_vacancies()
            vac_list.append(vacancy)
            self.save_vacancy_list(vac_list)

    def save_vacancy_list(self, vac_list: list):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([vac.get_json() for vac in vac_list], file, ensure_ascii=False)

    def get_vacancies(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancies_json = json.load(file)
        return[Vacancy.init_from_json(vacancy) for vacancy in vacancies_json]

    def get_vacancies_by_salary(self, rev: bool):
        return sorted(self.get_vacancies(), reverse=rev)

    def get_remote_vacancies(self):
        return [Vacancy.init_from_json(vacancy) for vacancy in self.get_vacancies() if vacancy["schedule"] == 'remote']

    def get_vacancies_by_employment(self, employment: bool):
        if employment:
            status = 'full time'
        else:
            status = 'part time'
        return [Vacancy.init_from_json(vacancy) for vacancy in self.get_vacancies() if vacancy["employment"] == status]

    def delete_vacancy(self, vacancy: Vacancy, vac_list: list):
        vac_list.remove(vacancy)
        self.save_vacancy_list(vac_list)
