from abc import ABC, abstractmethod
from translatehub.core.enums import Languages


class Api(ABC):
    api_url: str = ""
    api_key: str = ""

    @abstractmethod
    def translate(
        self,
        text: str,
        source: Languages | str = Languages.ENGLISH,
        target: Languages | str = Languages.CHINESE,
    ) -> str:
        pass
