from .fields import Field


class Name(Field):
    def __init__(self, name: str):
        super().__init__(self.is_valid_name(name))

    @property
    def name(self):
        return self.value

    @name.setter
    def name(self, name:str) -> None:
        self.value = self.is_valid_name(name)

    @staticmethod
    def is_valid_name(name: str):
        if not name:
            raise ValueError("Name is required")
        return name
