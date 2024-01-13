from .addressbook import AddressBook
from .record import Record
from cli_utils import register, get_success_message

from functools import wraps


def initialize():
    book = AddressBook()

    section = "contacts"

    def save_data(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            book.save_data()
            return result

        return wrapper

    @register("add-contact", section=section)
    @save_data
    def add(name: str) -> str:
        """
        Add contact with name address email birthday and phone
        """
        record = book.find(name)
        if record is None:
            record = Record(name)

        # if not record.find_phone(phone_number) is None:
        #     raise ValueError(f"Phone number `{phone_number}` in contact `{name}` exist")

        # record.add_phone(phone_number)

        book.add(record)

        return get_success_message(f"Contact `{name}`added")

    @register("edit-contact", section=section)
    @save_data
    def edit(name: str) -> str:
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        return get_success_message(f"Contact `{name}`edit")

    @register("search-contact", section=section)
    def search(string_search: str):
        """
        Search name or phone in book
        """
        result_list = book.search(string_search)
        if len(result_list) == 0:
            raise ValueError("Nothing found")

        tab_result = [f"|{'NAME':^10}|"]
        tab_result.extend(list(f"|{str(name):^10}|" for name in result_list))

        return get_success_message("\n".join(tab_result))

    @register("show-contacts", section=section)
    def show_record():
        """
        Show all record
        """

        list_record = list(get_success_message(f"{book[record]}") for record in book)
        return "\n".join(list_record)

    @register("del-contact", section=section)
    @save_data
    def delete(name: str) -> str:
        """
        Remove contact by name
        """
        record = book.find(name)

        if record is None:
            raise ValueError(f"Contact with name `{name}` not exist")

        book.delete(name)

        return get_success_message(f"Contact witn `{name}` deleted")
