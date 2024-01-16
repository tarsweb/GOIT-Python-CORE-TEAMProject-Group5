class Record:
    def __init__(self, text: str) -> None:
        self.text = text
        self.tags = []

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def __str__(self) -> str:
        return f"`{self.text}` : tags `{self.tags}`"
