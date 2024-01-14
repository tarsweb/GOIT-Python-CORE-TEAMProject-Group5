import re
from collections import UserList
from prettytable import PrettyTable

from .record import Record

import pickle
import os


class Note(UserList):

    def __init__(self):

    def add(self, record: Record) -> None:
        self.data.append(record)

    def delete(self, index: int) -> None:
        index = index-1
        if index < (len(self.data)-1):
            del self.data[index]
        else:
            print('Немає нотатки з таким номером')


    def show_all_notes(self):
        table = PrettyTable()
        table.field_names = ['№ of note', 'Text', 'Creation time', 'Tags']
        if self.data:
            for i, note in enumerate(self.data, start=1):
                table.add_row([i, note.note, note.creation_time,
                               ', '.join(note.tags)])
            return table
        else:
            print('Ви не додали жодної нотатки ')

    def find(self, index: int) -> Record | None:
        index = index - 1
        print(index)
        if (len(self.data)) > index:
            table = PrettyTable()
            table.field_names = ['№ of note', 'Text', 'Creation time', 'Tags']
            table.add_row([index+1, self.data[index].note, self.data[index].creation_time, self.data[index].tags]) 
            return str(table)
        else:
            return 'Немає нотатки з таким індексом'

    def search(self, search_string: str) -> list:
        pattern = re.compile(search_string, re.IGNORECASE)
        mathces = [record for record in self.data if 
                   pattern.search(record.note)]
        if mathces:
            return mathces
        else:
            print("Збігів не знайдено")
            return []

    def add_tag_to_note(self, note_number, tag):
        note_number = note_number-1
        if note_number < len(self.data):
            self.data[note_number].add_tag(tag)
        else:
            print("Немає нотатки з таким номером.")

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


notes = Note()
