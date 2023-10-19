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
    def delete_vacancy(self, vacancy: Vacancy):
        pass


class JSONSaver(FileSaver):
    """
    Class for JSON saver, that saves vacancy information in .json file in vacancies folder.
    Default file name is vacancies.json. Can be changed to create different file in the same folder.
    """
    def __init__(self, file_name='vacancies'):
        self.file_name = f'{file_name}.json'
        self.file_path = os.path.join('Vacancies', self.file_name)

    def __str__(self):
        return f'saver for .json files'

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def add_vacancy(self, vacancy: Vacancy):
        """
        adds single object from Vacancy class to a file
        """
        vac_list = self.get_vacancies()
        if vac_list is None:
            vac_list = [vacancy]
        else:
            vac_list.append(vacancy)
        self.save_vacancy_list(vac_list)

    def save_vacancy_list(self, vac_list: list):
        """
        saves list of objects from Vacancy class to a file
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([vac.get_json() for vac in vac_list], file, ensure_ascii=False)

    def get_vacancies(self):
        """
        gets vacancies from file and returns list of objects from Vacancy class or None if file doesn't exist
        :return: None, list
        """
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, 'r', encoding='utf-8') as file:
            vacancies_json = json.load(file)
        output = []
        for vacancy in vacancies_json:
            if Vacancy.init_from_json(vacancy) is None:
                continue
            else:
                output.append(Vacancy.init_from_json(vacancy))
        if len(output) == 0:
            return None
        else:
            return output

    def get_vacancies_by_salary(self, rev: bool):
        """
        get vacancies from file sorted by salary, can reverse order. True to sort from bigger, False to sort from
        smaller salary. If there was no information about salary, vacancy will be counted as if salary is 0.
        Returns list of objects from Vacancy class
        :param rev: True, False
        :return: list
        """
        return sorted(self.get_vacancies(), reverse=rev)

    def get_remote_vacancies(self):
        """
        gets remote vacancies from file, returns None if file doesn't exist
        :return: None, list
        """
        vac_list = self.get_vacancies()
        if vac_list is None:
            return None
        return [vacancy for vacancy in vac_list if vacancy.schedule == 'remote']

    def get_vacancies_by_employment(self, employment: bool):
        """
        Gets from file full time vacancies if it gets True on call or part-time vacancies if it gets False on call.
        Returns list of objects from Vacancy class
        :param employment: True, False
        :return: list
        """
        vac_list = self.get_vacancies()
        if vac_list is None:
            return None
        if employment:
            status = 'full time'
        else:
            status = 'part time'
        return [vacancy for vacancy in vac_list if vacancy.employment == status]

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Deletes single object from Vacancy class from a file
        :param vacancy: Vacancy
        """
        vac_list = self.get_vacancies()
        if vac_list is None or len(vac_list) == 0:
            return None
        try:
            vac_list.remove(vacancy)
        except ValueError:
            return None
        self.save_vacancy_list(vac_list)
        return True
