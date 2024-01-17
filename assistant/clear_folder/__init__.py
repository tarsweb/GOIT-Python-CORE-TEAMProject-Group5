from pathlib import Path
from cli_utils import register, print_clear_folder, get_warning_message
from .clearfolder import clearfolder


def initialize():
    @register("clear-folder", "cleaner")
    def clean(path_to_dir: str) -> str:
        if not Path(path_to_dir).exists():
            return get_warning_message(clean.__name__, f"Folder `{path_to_dir}` not exist")
        result = clearfolder(path_to_dir)
        return print_clear_folder(result)
