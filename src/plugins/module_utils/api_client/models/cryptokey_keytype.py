from enum import Enum


class CryptokeyKeytype(str, Enum):
    CSK = "csk"
    KSK = "ksk"
    ZSK = "zsk"

    def __str__(self) -> str:
        return str(self.value)
