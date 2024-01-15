import re
from collections import UserList


from .record import Record

import pickle
import os


class Note(UserList):



    def add(self, record: Record) -> None:
        self.data.append(record)

    def delete(self, index: int) -> None:
        index = index-1
        if index < (len(self.data)):
            del self.data[index]
        else:
            raise ValueError('Немає нотатки з таким номером')


    def show_all_notes(self):
        if not self.data:
            raise ValueError('Ви не додали жодної нотатки')
        return ', '.join(map(str, self.data)) 

    def find(self, index: int) -> Record | None:
        if index > len(self.data):
            return None
        return self.data[index]

    def search(self, search_string: str) -> list:
        pattern = re.compile(search_string, re.IGNORECASE)
        mathces = [str(record.note) for record in self.data if 
                   pattern.search(record.note)]
        if mathces:
            
            return mathces
        else:
            return ("Збігів не знайдено")

    def add_tag_to_note(self, note_number, tag):
        note = self.find(note_number)
        if note is not None:
            note.add_tag(tag)
        else:
            raise ValueError(f"Запис з номером {note_number} не знайдено.")
        
    def edit_note(self, note_number, new_text):
        note_number = note_number-1
        if note_number < len(self.data):
            self.data[note_number].note = new_text
        else:
            raise ValueError('Немає нотатки з таким номером')

    def edit_tag(self, old_tag, new_tag):
        for note in self.data:
            if old_tag in note.tags:
                note.tags.remove(old_tag)
                note.tags.append(new_tag)
            else:
                return 'Нотатки з таким  тегом не існує'


    def find_notes_by_tags(self, tag):
        notes = [str(note) for note in self.data if tag in note.tags]
        return notes if notes else 'Немає нотаток з таким тегом'
    
    def sort_by_tags(self):
        self.data.sort(key=lambda tag : tag.tags)



    filename = 'data.pickle'
    if not os.path.exists(filename):
        with open(filename, 'w'): 
            pass
        

    def save_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        with open('data.pickle', 'rb') as f:
            self.data = pickle.load(f)

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        pass

