from .fields import Field


class Email(Field):
    def __init__(self, email: str):
        super().__init__(self.__is_valid_email(email))

    @property
    def email(self):
        return self.value

    @email.setter
    def email(self, value):
        self.value = self.__is_valid_email(value)

    @staticmethod
    def __is_valid_email(email: str):
        # if not email:
        #     raise ValueError("Email is required")
        return email

    def __str__(self):
        return "unknown" if self.email is None else str(self.email)
