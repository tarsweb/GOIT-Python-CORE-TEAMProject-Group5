import os
import shutil

from cli_utils import get_success_message, get_error_message, get_warning_message

SYMBOLS = """ !"#$%&'()*+№,-/:;<=>?@[\\]^`{|}~"""
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
for symbol in SYMBOLS:
    TRANS[ord(symbol)] = "_"


FILE_TYPES = {
    "images": ["JPEG", "PNG", "JPG", "SVG", "BMP"],
    "video": ["AVI", "MP4", "MOV", "MKV"],
    "documents": ["DOC", "DOCX", "TXT", "PDF", "XLS", "XLSX", "PPTX"],
    "audio": ["MP3", "OGG", "WAV", "AMR"],
    "archives": ["ZIP", "GZ", "TAR", "RAR"],
}

FOLDER_ARCHIVE = ("archives",)
FOLDER_UNKNOWN = "unknown"

files_by_type = {}

result_work = {
    "error": (),
    "remove_folder": (),
    "unknown_extension": (),
    "message": (),
}


def get_extention_file(path_to_file: str) -> str:
    return os.path.splitext(path_to_file)[1].replace(".", "")


def find_type_files(folder_path: str, type_files: list) -> list:
    return list(
        os.path.join(folder_path, item)
        for item in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, item))
        and get_extention_file(item).upper() in type_files
    )


def unknown_files(folder_path: str, known_files: list) -> list:
    return list(
        os.path.join(folder_path, item)
        for item in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, item))
        and os.path.join(folder_path, item) not in known_files
    )


def subfolder_list(folder_path: str, ignore_path: tuple = tuple()) -> list:
    return [
        item
        for item in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, item)) and item not in ignore_path
    ]


def normalize(string: str) -> str:
    return string.translate(TRANS)


def move_files(destination: str, file_list: list, unpack=False) -> None:
    for file in file_list:
        name_file, extention = os.path.splitext(os.path.basename(file))
        file_name = normalize(name_file)
        new_file_path = os.path.join(destination, "".join((file_name, extention)))
        counter_bad_name = 0
        while True:
            if not os.path.exists(new_file_path):
                if counter_bad_name != 0:
                    file_name = f"{file_name}-{counter_bad_name}"
                break
            else:
                maby_file_name = f"{file_name}-{counter_bad_name + 1}"
                new_file_path = os.path.join(
                    destination, "".join((maby_file_name, extention))
                )
                counter_bad_name += 1
        try:
            shutil.move(file, new_file_path)
        except FileExistsError:
            update_result_work("error", f"{file} replace error")

        if unpack:
            try:
                shutil.unpack_archive(
                    new_file_path, os.path.join(destination, file_name)
                )
                # Remove
                os.remove(new_file_path)
            except shutil.ReadError:
                update_result_work(
                    "error", f"Find archive {new_file_path} unpack error"
                )
            except FileNotFoundError:
                update_result_work("error", f"File {new_file_path} not found")


def remove_empty_folders(folder):
    for root, dirs, _ in os.walk(folder, topdown=False):
        for i in dirs:
            dir_path = os.path.join(root, i)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                update_result_work("remove_folder", dir_path)


def scan_folder(folder_path, ignore_path: tuple = tuple()):
    files_by_type_current_folder = {}

    for category, type_files in FILE_TYPES.items():
        file_by_category = find_type_files(folder_path, type_files)
        files_by_type[category] += file_by_category
        files_by_type_current_folder.setdefault(category, file_by_category)

    list_known = []
    _ = [list_known.extend(v) for k, v in files_by_type.items()]

    files_by_type["unknown"] += unknown_files(folder_path, list_known)

    for item in subfolder_list(folder_path, ignore_path):
        scan_folder(os.path.join(folder_path, item))


def file_handlers(folder_result_path):
    for category, file_list in files_by_type.items():
        if len(file_list) == 0:
            continue  ## skip if not files

        destination_path = os.path.join(folder_result_path, category)
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        move_files(destination_path, file_list, unpack=category in FOLDER_ARCHIVE)


def update_result_work(result_key: str, *args) -> None:
    global result_work
    if result_key in result_work:
        result_work[result_key] = (*result_work[result_key], *args)


def get_result_work(folder_result_path, ignore_path: tuple = tuple()) -> list:
    global result_work

    used_extension = ()

    for i in ignore_path:
        current_path = os.path.join(folder_result_path, i)
        if not os.path.exists(current_path):
            continue

        in_folder = list(item for item in os.listdir(current_path))
        if i == FOLDER_UNKNOWN:
            update_result_work(
                "unknown_extension",
                *tuple(
                    get_extention_file(item).upper()
                    for item in in_folder
                    if os.path.isfile(os.path.join(current_path, item))
                ),
            )
        else:
            used_extension = (
                *used_extension,
                *set(
                    get_extention_file(item).upper()
                    for item in in_folder
                    if os.path.isfile(os.path.join(current_path, item))
                ),
            )
            update_result_work(
                "message",
                f"The folder '{i}' contains : {', '.join(in_folder)}",
            )

    result = []
    for k, v in result_work.items():
        if k == "error":
            if len(v) != 0:
                result.append({"Error": "\n".join([get_error_message(i) for i in v])})
        elif k == "remove_folder":
            if len(v) != 0:
                result.append({"Remove folder": get_warning_message("", ", ".join(v))})
        elif k == "unknown_extension":
            if len(v) != 0:
                result.append(
                    {
                        "Unknown extension": get_warning_message(
                            "", " ".join(set(v)).strip()
                        )
                    }
                )
        else:
            if len(v) != 0:
                result.append(
                    {"Statistics": "\n".join([get_success_message(i) for i in v])}
                )

    if len(used_extension) > 0:
        result.append({"Used extension": get_success_message(" ".join(used_extension))})

    return result


def clearfolder(folder_path, folder_result: str = None):
    global files_by_type
    global result_work

    folder_result = folder_path if folder_result is None else folder_result

    files_by_type = {category: [] for category in FILE_TYPES}
    files_by_type.setdefault(FOLDER_UNKNOWN, [])

    result_work = dict.fromkeys(result_work, tuple())

    if folder_path == folder_result:
        ignore_path = tuple(FILE_TYPES)
    else:
        ignore_path = tuple()

    scan_folder(folder_path, ignore_path)

    file_handlers(folder_result)

    remove_empty_folders(folder_path)

    return get_result_work(folder_result, tuple([*list(FILE_TYPES), FOLDER_UNKNOWN]))
