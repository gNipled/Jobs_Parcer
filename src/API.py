import requests
from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get_vacancy(self):
        pass
