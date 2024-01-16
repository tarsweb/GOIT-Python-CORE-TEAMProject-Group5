import re
from .fields import Field


class Email(Field):
    def __init__(self, email: str) -> None:
        super().__init__(self.is_valid_email(email))

    @property
    def email(self):
        return self.value

    @email.setter
    def email(self, email: str):
        self.value = self.is_valid_email(email)

    @staticmethod
    def is_valid_email(email: str) -> str | Exception:
        if not email is None:
            email_pattern = re.compile(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
            )
            if isinstance(email, str):
                match_object = email_pattern.match(email)
                if match_object is not None:
                    return match_object.group()
                raise ValueError("Invalid email")
            raise ValueError("Invalid email")

    def __str__(self):
        return "unknown" if self.email is None else str(self.email)
