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
        self.schedule = schedule
        self.employment = employment
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = payment_currency
        if self.currency == 'RUR':
            self.currency_rate = 1
        else:
            self.currency_rate = CurrencyRateAPI(self.currency).rate

    def __str__(self):
        return f'{self.name}, {self.payment_from} - {self.payment_to} {self.currency}'

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name},{self.payment_from} - {self.payment_to} {self.currency})'

    def __lt__(self, other):
        return self.currency_rate * self.payment_from < other.currency_rate * other.payment_from

    def __gt__(self, other):
        return self.currency_rate * self.payment_from > other.currency_rate * other.payment_from

    def __le__(self, other):
        return self.currency_rate * self.payment_from <= other.currency_rate * other.payment_from

    def __ge__(self, other):
        return self.currency_rate * self.payment_from >= other.currency_rate * other.payment_from

    def __eq__(self, other):
        return self.currency_rate * self.payment_from == other.currency_rate * other.payment_from
