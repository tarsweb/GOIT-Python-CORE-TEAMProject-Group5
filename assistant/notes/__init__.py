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
        return notes.show_all_notes()
    
    @register("note-find")
    def find(index: int) -> None:
        """
        Find notes by index
        """
        index = int(index)
        note = notes.find(index)
        return str(note)
        


