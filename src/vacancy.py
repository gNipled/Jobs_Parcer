from src.API import CurrencyRateAPI


class Vacancy:
    """
    Class to work with vacancies, for initiation uses vacancy data in format [name, link, schedule, employment,
        payment range min, payment range max, payment currency]
    """

    def __init__(self, name: str, link: str, schedule: str, employment: str, payment_from: int,
                 payment_to: int, payment_currency: str):
        self.name = name
        self.url = link
        if schedule in ("Не имеет значения", "Удалённая работа (на дому)", "Удаленная работа"):
            self.schedule = 'remote'
        else:
            self.schedule = 'office'
        if employment in ("Полный рабочий день", "Полная занятость"):
            self.employment = 'full time'
        else:
            self.employment = 'part time'
        self.currency = payment_currency
        if self.currency in ('RUR', 'RUB'):
            self.currency_rate = 1
        else:
            self.currency_rate = CurrencyRateAPI(self.currency).rate
        self.payment_from = self.get_payment(payment_from, payment_to)
        self.payment_to = self.get_payment(payment_to, payment_from)

    def __str__(self):
        if self.payment_from == 0 and self.payment_to == 0:
            payment = f'not specified'
        elif self.payment_from == self.payment_to:
            payment = f'{self.payment_to} RUB'
        else:
            payment = f'{self.payment_from}-{self.payment_to} RUB'
        if self.currency != 'RUR':
            payment += f' paid in {self.currency}'
        output = (f"Vacancy: {self.name}\n"
                  f"Payment: {payment}\n"
                  f"Link: {self.url}\n"
                  f"Schedule: {self.schedule}\n"
                  f"Employment: {self.employment}\n"
                  )
        return output

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name},{self.payment_from} - {self.payment_to} {self.currency})'

    def __lt__(self, other):
        return self.payment_from < other.payment_from

    def __gt__(self, other):
        return self.payment_from > other.payment_from

    def __le__(self, other):
        return self.payment_from <= other.payment_from

    def __ge__(self, other):
        return self.payment_from >= other.payment_from

    def __eq__(self, other):
        return self.payment_from == other.payment_from

    def get_payment(self, payment_from, payment_to):
        """
        method to calculate salary in RUB
        :param payment_from: payment 1
        :param payment_to: payment 2
        :return: payment
        """
        if payment_from is None and payment_to is None:
            return 0
        elif payment_from is None or payment_from == 0:
            return payment_to * self.currency_rate
        else:
            return payment_from * self.currency_rate

    def get_json(self):
        """
         Method to get information formatted as json dictionary from vacancy
        """
        return {
            "name": self.name, "url": self.url, "schedule": self.schedule, "employment": self.employment,
            "payment": {"from": self.payment_from, "to": self.payment_to, "currency": self.currency}
        }

    @classmethod
    def init_from_json(cls, vacancy: dict):
        """
        method for initiate Vacancy object from json dictionary. Returns object from Vacancy class
        """
        try:
            return Vacancy(vacancy["name"], vacancy["url"], vacancy["schedule"], vacancy["employment"],
                           vacancy["payment"]["from"], vacancy["payment"]["to"], vacancy["payment"]["currency"])
        except KeyError:
            return None
