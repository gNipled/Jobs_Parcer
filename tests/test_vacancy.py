import pytest
from src.vacancy import Vacancy

vac = Vacancy('a', 'a', 'a', 'a', 0, 0, 'USD')
vac_json = {
    "name": 'a', "url": 'a', "schedule": 'remote', "employment": 'full time',
    "payment": {"from": 31444, "to": 231324, "currency": 'RUR'}
}
vac_json1 = {
    "name": 'a', "url": 'a', "schedule": 'remote', "employment": 'full time',
    "payment": {"from": 231324, "to": 231324, "currency": 'RUR'}
}
vac1 = Vacancy.init_from_json(vac_json)
vac2 = Vacancy.init_from_json(vac_json1)


def test_get_payment():
    assert Vacancy.get_payment(None, 5) == 5
    assert Vacancy.get_payment(None, None) == 0
    assert Vacancy.get_payment(0, 0) == 0
    assert Vacancy.get_payment(5, None) == 5
    assert Vacancy.get_payment(0, 5) == 5


def test_get_json():
    assert type(vac.get_json()) == dict
    assert len(vac.get_json()) == 5


def test_init_from_json():
    assert Vacancy.init_from_json({"name": 'a'}) is None
    assert Vacancy.init_from_json(vac_json).name == 'a'


def test___str__():
    assert str(Vacancy.init_from_json(vac_json)) == (f'Vacancy: a\n'
                                                     f'Payment: 31444-231324 RUB\n'
                                                     f'Link: a\n'
                                                     f'Schedule: remote\n'
                                                     f'Employment: full time\n'
                                                     )
    assert str(vac) == (f'Vacancy: a\n'
                        f'Payment: not specified paid in USD\n'
                        f'Link: a\n'
                        f'Schedule: office\n'
                        f'Employment: part time\n'
                        )
    assert str(Vacancy.init_from_json(vac_json1)) == (f'Vacancy: a\n'
                                                      f'Payment: 231324 RUB\n'
                                                      f'Link: a\n'
                                                      f'Schedule: remote\n'
                                                      f'Employment: full time\n'
                                                      )


def test___repr__():
    assert repr(vac) == 'Vacancy (a, 0 - 0 USD)'


def test_eq():
    assert (vac1 < vac2) is True
    assert (vac1 > vac2) is False
    assert (vac1 <= vac2) is True
    assert (vac1 >= vac2) is False
    assert (vac1 == vac2) is False
