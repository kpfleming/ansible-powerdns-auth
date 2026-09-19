from enum import Enum


class ZoneKind(str, Enum):
    CONSUMER = "Consumer"
    MASTER = "Master"
    NATIVE = "Native"
    PRODUCER = "Producer"
    SLAVE = "Slave"

    def __str__(self) -> str:
        return str(self.value)
