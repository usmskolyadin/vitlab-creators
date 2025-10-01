from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def get_stats(self, url: str) -> dict:
        """
        Должен вернуть словарь вида:
        {
            "platform": "YouTube",
            "account": "channel_id",
            "likes": 1000,
            "views": 20000,
            "comments": 300
        }
        """
        pass