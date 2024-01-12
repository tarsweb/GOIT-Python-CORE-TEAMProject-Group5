from .notes import Note
from .record import Record
from cli_utils import register, get_success_message


def initialize():
    notes = Note()

    @register("note-add")
    def add(text: str) -> None:
        """
        Add notes
        """

        record = Record(text=text)

        notes.add(record)

        return get_success_message(f"Note `{text}` added")

    @register("note-show")
    def show() -> str:
        """
        Show all notes
        """

        list_notes = list(
            get_success_message(f"{notes.index(note) + 1} : {note}") for note in notes
        )
        return "\n".join(list_notes)
