from .addressbook import AddressBook
from .record import Record
from cli_utils import register, get_success_message


def initialize():
    book = AddressBook()

    @register("contact-add")
    def add_record(name: str) -> str:
        """
        Add contact with name and phone
        """
        record = Record(name)

        book.add_record(record)

        return get_success_message(f"Contact `{name}`added")

    @register("show_record")
    def show_record():
        """
        Show all record
        """
        list_record = list(get_success_message(f"{record}") for record in book)
        return "\n".join(list_record)
