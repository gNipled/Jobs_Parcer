import json
from src.config import SUPERJOB_TOKEN, API_KEY
import requests
import os
from datetime import date
from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Abstract class for APIs"""

    @abstractmethod
    def get_vacancies(self):
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

    def get_vacancies(self):
        """
        Method for parsing hh.ru for vacancy by 'keyword'
        :return list in format [name, link, schedule, employment,
        payment range min, payment range max, payment currency]
        """
        response = requests.get(f'https://api.hh.ru/vacancies', headers={'User-Agent': 'jobparcerforstudy'},
                                params={'per_page': 100, 'text': self.keyword})
        if response.status_code != 200:
            return None
        output = []
        for vacancy in response.json()['items']:
            results = {
                "name": vacancy['name'], "url": vacancy['alternate_url'], "schedule": vacancy['schedule']['name'],
                "employment": vacancy['employment']['name'], "payment": {
                    "from": 0, "to": 0, "currency": "RUR"
                }
            }
            try:
                results["payment"]["from"] = vacancy['salary']['from']
            except TypeError:
                results["payment"]["from"] = 0
            try:
                results["payment"]["to"] = vacancy['salary']['to']
            except TypeError:
                results["payment"]["to"] = 0
            try:
                results["payment"]["currency"] = vacancy['salary']['currency']
            except TypeError:
                results["payment"]["currency"] = 'RUR'
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

    def get_vacancies(self):
        """
        Method for parsing superjob.ru for vacancy by 'keyword'
        :return list in format [name, link, schedule, employment,
        payment range min, payment range max, payment currency]
        """
        response = requests.get(f'https://api.superjob.ru/2.0/vacancies/', headers={'X-Api-App-Id': SUPERJOB_TOKEN},
                                params={'keyword': self.keyword, 'page': 0, 'count': 100})
        if response.status_code != 200:
            return None
        return [{
            "name": x['profession'], "url": x['link'], "schedule": x['place_of_work']['title'],
            "employment": x['type_of_work']['title'],
            "payment": {"from": x['payment_from'], "to": x['payment_to'], "currency": 'RUR'},
        } for x in response.json()['objects']]


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
        """
        method to get currency exchange rate for ruble
        """
        url = f"https://api.apilayer.com/exchangerates_data/latest"
        response = requests.get(url, headers={'apikey': API_KEY}, params={'base': 'RUB'})
        return response.json()

    def get_rate(self):
        """
        method to get exchange rate for currency. Checks rates.json file in src folder for exchange rates,
        if file is old or not exist get new rates and write them to file
        """
        if os.path.exists(os.path.join('currency_rates', 'rates.json')) and self.is_rate_today():
            with open(os.path.join('currency_rates', 'rates.json'), 'r') as file:
                return 1 / float(json.load(file)['rates'][self.currency])
        else:
            if not os.path.isdir('currency_rates'):
                os.mkdir('currency_rates')
            with open(os.path.join('currency_rates', 'rates.json'), 'w') as file:
                info = self.get_currency_rate()
                json.dump(info, file)
                return 1 / float(info['rates'][self.currency])

    @staticmethod
    def is_rate_today():
        with open(os.path.join('currency_rates', 'rates.json'), 'r') as file:
            if json.load(file)['date'] == str(date.today().isoformat()):
                return True
            else:
                return False


print(CurrencyRateAPI('USD').get_rate())
