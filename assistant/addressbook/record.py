from .name import Name


class Record:
    def __init__(self, name: str):
        self.name = Name(name)

    def __str__(self) -> str:
        return f"{self.name}"
