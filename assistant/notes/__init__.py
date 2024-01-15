from cli_utils import register, get_success_message

from .notes import Note
from .record import Record


def initialize():
    notes = Note()

    section = "notes"

    @register("add-note", section=section)
    def add(text: str) -> None:
        """
        Add notes
        """

        record = Record(text=text)

        notes.add(record)

        return get_success_message(f"Note `{text}` added")

    @register("edit-note", section=section)
    def edit(index: str) -> None:
        """
        Edit note
        """
        record = notes.find(int(index))

        if record is None:
            raise ValueError(f"Note with index `{index}` not exist")

        return get_success_message(f"Note `{record}` edit")

    @register("show-notes", section=section)
    def show() -> str:
        """
        Show all notes
        """

        list_notes = list(
            get_success_message(f"{notes.index(note) + 1} : {note}") for note in notes
        )
        if len(list_notes) == 0:
            raise ValueError("No notes")

        return "\n".join(list_notes)
