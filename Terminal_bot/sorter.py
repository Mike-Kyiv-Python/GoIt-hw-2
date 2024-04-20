from pathlib import Path
import shutil
import re
import sys


IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOCS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'EXE')
AUDIO = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')
OTHER = []
FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

dict_suffixes = {"IMAGES": IMAGES, "VIDEO": VIDEO, "DOCS": DOCS, "AUDIO": AUDIO, "ARCHIVES": ARCHIVES}

dict_suffixes_reverse = {}
for category, suffixes in dict_suffixes.items():
    temp_dict = dict.fromkeys(suffixes, category)
    dict_suffixes_reverse.update(temp_dict)

# normalize

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name: str) -> str:
    new_name = name.translate(TRANS)
    split_str = new_name.split('.')
    split_str[0] = re.sub(r'\W', '_', split_str[0])
    new_name = '.'.join(split_str)
    return new_name

#scan

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'docs', 'images', 'other'):
                FOLDERS.append(item)
                scan(item)
            continue
        else:
            extension = get_extensions(file_name=item.name)
            new_name = folder / item.name
            if not extension:
                OTHER.append(new_name)
            else:
                try:
                    container = dict_suffixes_reverse[extension]
                    if not isinstance(container, list):
                        dict_suffixes_reverse[extension] = [container]
                    EXTENSION.add(extension)
                    dict_suffixes_reverse[extension].append(str(new_name))
                except KeyError:
                    UNKNOWN.add(extension)
                    OTHER.append(new_name)

#main

def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(parents=True, exist_ok=True)  # Створює папку, якщо не існує
    file_name = Path(path).name
    normalized_name = normalize(file_name)
    new_file_path = target_folder / normalized_name
    shutil.move(path, new_file_path)

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        print('Архів не було розпаковано')
        shutil.rmtree(str(archive_folder))  
        return
    except FileNotFoundError:
        print('Архів не було розпаковано')
        shutil.rmtree(str(archive_folder))  
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def sorter(folder_path):
    print(folder_path)
    scan(folder_path)

    for item in folder_path.iterdir():
        if item.is_file():
            extension = get_extensions(file_name=item.name)
            categories = dict_suffixes_reverse.get(extension, ["Other"])
            category = categories[0]  # Вибираємо першу категорію зі списку
            handle_file(item, folder_path, category)
        elif item.is_dir():
            sorter(item)  # Обробляємо файли у вкладених теках (рекурсія)

    remove_empty_folders(folder_path)

def start(data:str):
    path = data
    print(f'Start in {path}')

    folder = Path(path)
    sorter(folder.resolve())

# if __name__ == '__main__':
#     path = sys.argv[1]
#     print(f'Start in {path}')

#     folder = Path(path)
#     sorter(folder.resolve())

