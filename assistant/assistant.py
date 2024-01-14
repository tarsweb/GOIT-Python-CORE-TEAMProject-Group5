from assistant.cli_utils import register, listener, show_register_command
from assistant.addressbook import initialize as initialize_addressbook
from assistant.notes import initialize as initialize_notes
from assistant.clear_folder import initialize as initialize_clean_folder


# Example (приклад)
@register("hello")
def hello() -> str:
    return "How can I help you?"


# Example (приклад)
@register("add")
def add(num: int) -> int:
    if not isinstance(num, int):
        try:
            num = int(num)
        except ValueError:
            num = 0

    return num * 2


def main():
    # addressbook.initialize()
    # notes.initialize()
    # clear_folder.initialize()

    initialize_addressbook()
    initialize_notes()
    initialize_clean_folder()

    print(show_register_command())
    listener()


if __name__ == "__main__":
    main()
