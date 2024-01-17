import sys
import os

sys.path.append(os.path.join(sys.path[0], "assistant"))

from .cli_utils import listener, show_register_command
from .addressbook import initialize as initialize_addressbook
from .notes import initialize as initialize_notes
from .clear_folder import initialize as initialize_clean_folder


def main():
    initialize_addressbook()
    initialize_notes()
    initialize_clean_folder()

    print(show_register_command())
    listener()


if __name__ == "__main__":
    main()
