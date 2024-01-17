class Record:
    def __init__(self, text: str) -> None:
        self.text = text
        self.tags = []

    def edit_text(self, text: str):
        self.text = text

    def remove_text(self):
        self.text = None

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def edit_tag(self, old_tag: str, new_tag: str) -> None:
        if old_tag not in self.tags:
            raise ValueError("Tag `{old_tag}` not found")

        index_tag = self.tags.index(old_tag)
        self.tags[index_tag] = new_tag

    def remove_tag(self, tag: str) -> None:
        self.tags = list(filter(lambda current_tag: current_tag != tag, self.tags))

    def __str__(self) -> str:
        return f"`{self.text}` : tags `{self.tags}`"
