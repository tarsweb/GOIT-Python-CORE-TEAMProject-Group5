from cli_utils import register, get_success_message


def initialize():
    @register("clear-folder", "cleaner")
    def clean(path_to_dir: str) -> str:
        return get_success_message(f"report clear {path_to_dir}")
