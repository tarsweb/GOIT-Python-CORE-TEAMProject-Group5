import re
from datetime import date, datetime
from .fields import Field


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        super().__init__(self.is_valid_birthday(birthday))

    @property
    def birthday_date(self):
        return self.value

    @birthday_date.setter
    def birthday_date(self, birthday: str):
        self.value = self.is_valid_birthday(birthday)

    @staticmethod
    def is_valid_birthday(birthday: str) -> date | Exception:
        def parse_date(date_string):
            parts = re.split(r"[ \-,.]", date_string)
            current_date = datetime.now()

            if len(parts[0]) == 4:
                year, month, day = parts
            else:
                day, month, year = parts
            birthdate = datetime(int(year), int(month), int(day))
            if current_date <= birthdate:
                raise ValueError("Date of birth is greater than the current date")

            return birthdate.date()

        if birthday is not None:
            pattern = re.compile(r"^(\d{4}\.\d{1,2}\.\d{1,2}|\d{1,2}\.\d{1,2}\.\d{4})$")
            if not pattern.match(birthday):
                raise ValueError(
                    "The date format must match (yyyy.mm.dd) or (dd.mm.yyyy)"
                )

            return parse_date(birthday)

    def __str__(self):
        return "unknown" if self.birthday_date is None else str(self.birthday_date)
