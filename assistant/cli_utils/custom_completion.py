from typing import Iterable
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document


class CustomCompleter(Completer):
    def __init__(self, commands: dict) -> None:
        super().__init__()
        self.commands = commands

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text_before_cursor.lstrip()
        if text:
            return
        for command, value in self.commands.items():
            if value is None:
                yield Completion(f"{command}")
                continue
            elif isinstance(value, dict):
                yield Completion(
                    f"{command}",
                    start_position=0,
                    display=value.get("display", None),
                    display_meta=value.get("display_meta", None),
                )
