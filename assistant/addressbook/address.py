from .fields  import Field

class Address(Field):
    def __init__(self, address: str):
        super().__init__(address)

    @property
    def address(self):
        return self.value

    @address.setter
    def email(self, value):
        self.value = value

    def __str__(self):
        return "-" if self.address is None else str(self.address)