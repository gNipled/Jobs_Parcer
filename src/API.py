import json

import requests
import os
from datetime import date
from abc import ABC, abstractmethod


SUPERJOB_TOKEN = os.getenv('API_SuperJob')
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
CURRENCY_RATES_FILE = 'currency_rates.json'


class AbstractAPI(ABC):
    """Abstract class for APIs"""

    @abstractmethod
    def get_vacancies(self) -> list:
        """Method for parsing vacancy sites"""
        pass


class HeadHunterAPI(AbstractAPI):
    """Class for hh.ru API"""
    def __init__(self, keyword: str):
        self.keyword = keyword

    def __str__(self):
        return {self.keyword}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.keyword})"

    def get_vacancies(self) -> list:
        """
        Method for parsing hh.ru for vacancy by 'keyword'
        :return list in format [name, link, schedule, employment,
        payment range min, payment range max, payment currency]
        """
        response = requests.get(f'https://api.hh.ru/vacancies', headers={'User-Agent': 'jobparcerforstudy'},
                                params={'per_page': 100, 'text': self.keyword})
        output = []
        for vacancy in response.json()['items']:
            results = [vacancy['name'], vacancy['alternate_url'], vacancy['schedule']['name'],
                       vacancy['employment']['name']]
            try:
                results.append(vacancy['salary']['from'])
            except TypeError:
                results.append(0)
            try:
                results.append(vacancy['salary']['to'])
            except TypeError:
                results.append(0)
            try:
                results.append(vacancy['salary']['currency'])
            except TypeError:
                results.append('RUR')
            output.append(results)
        return output


class SuperJobAPI(AbstractAPI):
    """Class for SuperJob.ru API"""
    def __init__(self, keyword: str):
        self.keyword = keyword

    def __str__(self):
        return {self.keyword}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.keyword})"

    def get_vacancies(self) -> list:
        """
        Method for parsing superjob.ru for vacancy by 'keyword'
        :return list in format [name, link, schedule, employment,
        payment range min, payment range max, payment currency]
        """
        response = requests.get(f'https://api.superjob.ru/2.0/vacancies/', headers={'X-Api-App-Id': SUPERJOB_TOKEN},
                                params={'keyword': self.keyword, 'page': 0, 'count': 100})
        # return response.json()
        return [[x['profession'], x['link'], x['place_of_work']['title'], x['type_of_work']['title'],
                 x['payment_from'], x['payment_to'], 'RUR'] for x in response.json()['objects']]


class CurrencyRateAPI:
    """Class to get currency exchange rate"""
    def __init__(self, currency: str):
        self.currency = currency
        self.rate = self.get_rate()

    def __str__(self):
        return f'{self.currency} rate to RUB is {self.rate}'

    def __repr__(self):
        return f"{self.__class__.__name__}({self.currency}, {self.rate})"

    @classmethod
    def get_currency_rate(cls):
        url = f"https://api.apilayer.com/exchangerates_data/latest"
        response = requests.get(url, headers={'apikey': API_KEY}, params={'base': 'RUB'})
        return response.json()

    def get_rate(self):
        if os.path.exists('../src/rates.json'):
            file = open('../src/rates.json', 'r')
            if json.load(file)['date'] == str(date.today().isoformat()):
                rate = 1/float(json.load(file)['rates'][self.currency])
                file.close()
                return rate
            else:
                file.close()
                with open('../src/rates.json', 'w') as file:
                    info = self.get_currency_rate()
                    json.dump(info, file)
                    return 1/float(info['rates'][self.currency])
        else:
            with open('../src/rates.json', 'w') as file:
                info = self.get_currency_rate()
                json.dump(info, file)
                return 1/float(json.load(file)['rates'][self.currency])
