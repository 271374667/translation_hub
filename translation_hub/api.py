from abc import ABC, abstractmethod
from translation_hub.core.enums import Languages


class Api(ABC):
    api_url: str = ""
    api_key: str = ""

    @abstractmethod
    def translate(
        self,
        text: str,
        source: Languages | str = Languages.English,
        target: Languages | str = Languages.Chinese,
    ) -> str:
        pass
