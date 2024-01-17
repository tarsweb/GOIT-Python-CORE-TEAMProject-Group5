from .clearfolder import clearfolder
from assistant.cli_utils import register, print_clear_folder


def initialize():
    @register("clear-folder", "cleaner")
    def clean(path_to_dir: str) -> str:
        result = clearfolder(path_to_dir)
        return print_clear_folder(result)
