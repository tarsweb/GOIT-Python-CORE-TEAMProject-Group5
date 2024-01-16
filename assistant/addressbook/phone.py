import re
from .fields import Field


class Phone(Field):
    # реалізація класу
    def __init__(self, phone_number: str):
        super().__init__(self.is_valid_phone_number(phone_number))

    @property
    def phone(self):
        return self.value

    @phone.setter
    def phone(self, phone_number:str) -> None:
        self.value = self.is_valid_phone_number(phone_number)

    @staticmethod
    def is_valid_phone_number(phone_number: str) -> str | Exception:
        phone_number_pattern = re.compile(r"(?=\+\d{1,3}\(\d{1,3}\)\d{3}\-\d{1,2}\-\d{2,3}).{17}")
        match_object = phone_number_pattern.match(phone_number)
        if match_object is None:
            raise ValueError(f"Phone {phone_number} not valid use format +1-3(1-2)3-[1-2]-[2-3] simbols only digital "
                             f"for example +38(044)123-12-12 +972(505)123-1-24")
            
        return match_object.group()
