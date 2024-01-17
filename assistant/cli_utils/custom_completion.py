from typing import Iterable
from prompt_toolkit.completion import (
    CompleteEvent,
    Completer,
    Completion,
    NestedCompleter
)
from prompt_toolkit.document import Document


class CustomCompleter(Completer):
    def __init__(self, commands: dict) -> None:
        super().__init__()
        self.commands = commands

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text_before_cursor.lstrip()
        # if text:
        #     return
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


class CustomSingleCompleter(Completer):
    def __init__(
        self,
        command: str,
        start_position: int = 0,
        display: str = "",
        display_meta: str = "",
    ) -> None:
        super().__init__()
        self.command_name = command
        self.start_position = start_position
        self.display = display
        self.display_meta = display_meta

    def get_completions(self, document: Document, complete_event: CompleteEvent):
        yield Completion(
            text=self.command_name,
            start_position=self.start_position,
            display=self.display,
            display_meta=self.display_meta,
        )


def get_nested_completer(dict_commads: dict) -> NestedCompleter:
    return NestedCompleter.from_nested_dict(dict_commads)
