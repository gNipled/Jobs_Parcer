import requests
import os
from abc import ABC, abstractmethod


SUPERJOB_TOKEN = os.getenv('API_SuperJob')


class AbstractAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(AbstractAPI):
    def get_vacancies(self):
        response = requests.get(f'https://api.hh.ru/vacancies', headers={'User-Agent': 'jobparcerforstudy'},
                                params={'per_page': 100, 'text': 'python', 'schedule': 'remote'})
        return response.json()


class SuperJobAPI(AbstractAPI):
    def get_vacancies(self):
        response = requests.get(f'https://api.superjob.ru/2.0/vacancies/', headers={'X-Api-App-Id': SUPERJOB_TOKEN},
                                params={'keyword': 'python', 'page': 0, 'count': 100, 'place_of_work': 2})
        return response.json()
