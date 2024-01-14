from datetime import datetime


class Record:
    def __init__(self, text: str) -> None:
        self.note = text
        self.creation_time = datetime.now().replace(microsecond=0)
        self.tags = []

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def __str__(self) -> str:
        return f"`{self.note}` : tags `{self.tags}`"