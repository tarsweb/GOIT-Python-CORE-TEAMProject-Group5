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
    ################################################################
    
    @register("note-find")
    def find(index: int) -> None:
        """
        Find notes by index
        """
        index = int(index)
        note = notes.find(index)
        return str(note)
        
    @register("note-remove")
    def delete(index: int) -> None:
        """
        Find notes by index
        """
        index = int(index)
        note = notes.delete(index)
        return str(note)
    
    @register('add-tag')
    def add_tag_to_note( note_number : int, tag : str ):
        note_number = int(note_number)
        notes.add_tag_to_note(note_number,tag)

    @register('note-search')
    def search(search_string: str) -> list:
        note = notes.search(search_string)
        return note
   
    @register('note-edit')
    def note_edit(note_number,new_text):
        note_number = int(note_number)
        notes.edit_note(note_number, new_text)


    @register('tag-edit')
    def edit_tag(old_tag,new_tag):
        notes.edit_tag(old_tag, new_tag)

    @register('find-by-tag')
    def find_tags(tag): 
        return(notes.find_notes_by_tags(tag))

    @register('sort-by-tags')
    def sort_by_tags():
        notes.sort_by_tags()


        


