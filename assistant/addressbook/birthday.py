from .fields import Field
from datetime import datetime
import re


class Birthday(Field):
    def __init__(self, birthday: str):
        self.value = birthday  # Викличемо сетер для валідації та зберігання значення

    @staticmethod
    def validate_date_of_birth(birthday):
        pattern = re.compile(r'^(\d{4}[- /._]\d{1,2}[- /._]\d{1,2}|\d{1,2}[- /._]\d{1,2}[- /._]\d{4})$')
        if bool(pattern.match(birthday)):
            return Birthday.parse_date(birthday)
        else:
            raise ValueError('The date format must match (yyyy mm dd), (dd mm yyyy)')

    @staticmethod
    def parse_date(date_string):

        parts = re.split(r'[ \-,.]', date_string)
        current_date = datetime.now()

        if len(parts[0]) == 4:
            year, month, day = parts
        else:
            day, month, year = parts
        birthdate = datetime(int(year), int(month), int(day))
        if current_date >= birthdate:
            return birthdate.date()
        else:
            raise ValueError('Date of birth is greater than the current date')

    @property
    def value(self):
        return str(self._value)

    @value.setter
    def value(self, new_value):
        if new_value:
            Field.__init__(self, self.validate_date_of_birth(new_value))
        else:
            self._value = ''
