from classes import Address_book, Contact, Birthday, Phone, Email, Note_book , Note
from sorter import start
import pathlib
import pickle

cache = Address_book()
note_cache = Note_book()

# Функція декоратор для обробки помилок
def input_error(inner):
    def wrap(*args):
        try:
            return inner(*args)
        except IndexError:
            return "IndexError, use command 'about' to learn about the correctness of entering commands"
        except ValueError:
            return "ValueError, use command 'about' to learn about the correctness of entering commands"
        except KeyError:
            return "KeyError, use command 'about' to learn about the correctness of entering commands"
        except TypeError:
            return "TypeError, use command 'about' to learn about the correctness of entering commands"
        except ArithmeticError:
            return "ArithmeticError, use command 'about' to learn about the correctness of entering commands"
    return wrap

@ input_error
def greeting(data):
    return "Вітаю! Ласкаво просимо до вашого персонального помічника."

@ input_error
def add_contact(data):
    name = data
    result = cache.add_contact(Contact(name))
    if result:
        return result

@ input_error    
def add_phone(data):
    name, phone = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    phone = Phone(phone)
    if phone:
        return cache[name].add_phone(phone.value) 

@ input_error
def edit_phone(data):
    name, old_phone, new_phone = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.edit_phone(old_phone,new_phone)

@ input_error
def del_phone(data):
    name, phone = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    phone = Phone(phone)
    if phone is None:
        return 
    elif cache[name].find_phone(phone.value):
        cache[name].remove_phone(phone.value)
        return f'Phone: {phone.value} for contact: {name} deleted'
    return f'Contact: {name} not have this phone: {phone.value}\n{cache[name]}'

@ input_error
def contact_output(data):
    return cache.search_contact(data)

@ input_error
def add_email(data):
    name, email = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.add_email(email)

@ input_error
def edit_email(data):
    name, old_email, new_email = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.edit_email(new_email)

@ input_error
def add_address(data):
    name, new_address = data[0] , '  '.join(i for i in data[1:])
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.add_address(new_address)

@ input_error
def edit_address(data):
    name, new_address = data[0], ' '.join(i for i in data[1:])
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.edit_address(new_address)

@ input_error
def add_birthday(data):
    name, birthday = data
    name = name.lower().capitalize()
    contact = cache.search_contact(name)
    if contact is None:
        return 
    contact.add_birthday(birthday)

@ input_error
def about(data):
    commands = [['Command', 'Parameters', 'Description'],
                   ['show all', '', 'list all information about users'],
                   ['add contact', '[Name]', 'create new user [Name] in adress book'],
                   ['edit name', '[old_Name] [new_Name]', 'edit name of [old_Name] to [new_Name]'],
                   ['del contact', '[Name]', 'remove user [Name] from adress book'],
                   ['add phone', '[Contact_id] [Phone]', 'add to user [Contact_id] a [Phone]'],
                   ['edit phone', '[Contact_id] [Phone] [new_Phone]', 'replace for user [Contact_id] a [Phone] by [new_Phone]'],
                   ['del phone', '[Name] [Phone]', 'remove phone [Phone] from user [Name]'],
                   ['add email', '[Contact_id] [Email]', 'add to user [Contact_id] an [Email]'],
                   ['edit email', '[Contact_id] [Email] [new_Email]', 'replace for user [Contact_id] an [Email] by [new_Email]'],
                   ['address', '[Contact_id] [Address]', 'set for user [Name] an address [Address]'],
                   ['edit address', '[Contact_id] [New address]', 'replace for user [Contact_id] an [New address]'],
                   ['birthday', '[Contact_id] [Birthday]', 'set for user [Contact_id] a birthday at [Birthday]'],
                   ['next-birthdays', '[int]', 'shows upcoming birthdays if exist in period from today till [int] days'],
                   ['add note', '[string]', 'Add a note to Note Book'],
                   ['all notes', '', 'list all notes'],
                   ['del note', '[Title]', 'Remove [Note_id] note from Note Book'],
                   ['add tag', '[Title] [Tag]', 'add [Tag] to note [Title]'],
                   ['del tag', '[Title] [Tag]', 'remove [Tag] from note [Title]'],
                   ['find note', '[searchstring]', 'list all Notes with [searchstring] data in note and tags.[searchstring] must be 2 symbols minimum'],
                   ['find tag', '[searchstring]', 'list all Notes with [searchstring] data in tags.[searchstring] must be 2 symbols minimum'],
                   ['sort tag', '', 'list all Notes sorted by number of tags'],
                   ['close, exit', '', 'exit the bot'],
                   ['about', '', 'list all bot commands'],
                   ['sort notes', '', 'sorting notes from tag'],
                   ['sorting', '[path to folder]', 'sorted files in folder by format']
                   ]
    dashes = "{0:<14} + {1:50} + {2:^32} \n".format("-" * 14, "-" * 50, "-" * 32)
    help_string = ''

    for i in commands:
        help_string += f'{i[0]:^14} | {i[1]:^50} | {i[2]:^32} \n'
        help_string += dashes
    return help_string

@ input_error
def show_all(data):
    return cache

@ input_error
def delete(data):
    name = data.lower().capitalize()
    result = cache.search_contact(name)
    if result:
        cache.remove_contact(name)
        print(f'Contact with name: {name} deleted')

@ input_error
def days_to_birthday():
    days_left = int(input('Введіть кількість днів до Дня народження: '))
    contacts = Contact()
    return contacts.days_to_birthday(days_left)

@ input_error
def add_note(data):
    text = ' '.join(i for i in data)
    note_cache.add_note(text)

@ input_error
def all_notes(data):
    return note_cache.__str__()

@ input_error
def del_note(data):
    title = data.lower().capitalize()
    notes = note_cache.search_note_with_title(title)
    print(notes,type(notes),len(notes))
    if notes is not str():
        print(f'Found {len(notes)} notes with title or tag: {title}')
        for i in notes:
            print(i)
            user_input = input('Delete this note?\n[input:"y"->Enter]->delete\n[Enter]->skip\n>>>')
            if user_input == 'y':
                note_cache.del_note(i)
        return
    return notes

@ input_error
def add_tag(data):
    title, tag = data
    title = title.lower().capitalize()
    note = note_cache.search_note_with_title(title)
    if note is not None:
        note[0].add_tag(tag)
        return f'Tag {tag} for {title}'
    return note

@ input_error
def del_tag(data):
    title, tag = data
    tag = tag .lower().capitalize()
    title = title.lower().capitalize()
    note = note_cache.search_note_with_title(title)
    if note is not None :
        note[0].remove_tag_in_note(tag)
        return
    return note

@ input_error
def find_note(data):
    title = data.lower().capitalize()
    note = note_cache.search_note_with_title(title)
    if note is not None:
        for n in note:
            print(n)
            return
    note = note_cache.search_note_with_tag(title)
    if note is not None:
        print(1)
        for n in note:
            print(n)
            return
    
@ input_error
def find_tag(data):
    tag = data.lower().capitalize()
    note = note_cache.search_note_with_tag(tag)
    if note is not None:
        for n in note:
            print(n)

def sort_notes(data):
    note_cache.sort_by_tags()


def sorting(data):
    start(*data)

# Функція для запису кешу в окремий файл для зберігання данних
def exit(data):
    # Якщо кеш пустий та окремий файл для зберігання існує тоді файл буде видалено
    if not cache and pathlib.Path('cache.bin').exists():
        pathlib.Path('cache.bin').unlink()
    if not note_cache and pathlib.Path('note_cache.bin').exists():
        pathlib.Path('note_cache.bin').unlink()
    if not cache and not note_cache:
        return
    with open('cache.bin', 'wb') as file:
        pickle.dump(cache, file)
    with open('note_cache.bin', 'wb') as file:
        pickle.dump(note_cache, file)

# Функія для відновлення кешу при повторному виклику програми
def return_cache():
    with open('cache.bin', 'rb') as file:
        global cache
        cache = pickle.load(file)

def return_note_cache():
    with open('note_cache.bin', 'rb') as file:
        global note_cache
        note_cache = pickle.load(file) 

# Словник ключ = Функція, значення= Ключові слова для запуску функцій
COMMANDS = {
    greeting: 'hello',#
    add_contact: 'add contact',#
    add_phone: 'add phone',#
    edit_phone: 'edit phone',#
    del_phone: 'del phone',#
    contact_output: 'contact',#
    add_email: 'add email',#
    edit_email: 'edit email',#
    add_address: 'add address',#
    edit_address: 'edit address',#
    add_birthday: 'birthday',#
    show_all: 'show all',#
    exit: ['exit', 'good bye', 'close'],#
    delete: 'del contact',#
    about: 'about',#
    days_to_birthday: 'days to birthday',
    add_note: 'add note',#
    all_notes: 'all notes',#
    del_note: 'del note',#
    find_note: 'find note',#
    add_tag: 'add tag',#
    del_tag: 'del tag',#
    find_tag: 'find tag',#
    sorting: 'sorting',#
    sort_notes: 'sort notes'#
}

def commands(data):
    # Поділ переданих данних користувачем через пробіл
    comand_list = data.lower().split()
    for key, value in COMMANDS.items():
        if len(comand_list) == 1:
            if comand_list[0] == value:
                return key, None
            elif comand_list[0] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 2:
            if comand_list[0] == value:
                return key, comand_list[1:]
            elif comand_list[0] + ' ' + comand_list[1] == value:
                return key, None
            elif comand_list[0] + ' ' + comand_list[1] in COMMANDS[exit]:
                return exit, None
        elif len(comand_list) == 3:
            if comand_list[0] == value:
                return key, comand_list[1:]
            if comand_list[0] + ' ' + comand_list[1] == value:
                return key, comand_list[2]
        elif len(comand_list) > 3:
            if ' '.join(comand_list[0:2]) == value:
                return key, comand_list[2:]
            if ' '.join(comand_list[0:3]) == value:
                return key, comand_list[3:]
    # Якщо не було знайдено переданої команди
    return None, None

def main():
    # Якщо раніше використовувалася програма та було створено кеш: його буде відновлено
    if pathlib.Path('cache.bin').exists():
        return_cache()
    if pathlib.Path('note_cache.bin').exists():
        return_note_cache()
    # Цикл для тривалої роботи програми
    while True:
        # Отримання даних від користувачаa
        user_input = input('>>>')
        if user_input:
            func, data = commands(user_input)
        if func == None:
            continue
        elif func == exit:
            # Вихід з програми та запис кешу в окремий файл
            func(data)
            print('Good bye')
            break
        else:
            # Запуск команд
            result = func(data)
            if result is None:
                continue
            print(result)


if __name__ == '__main__':
    main()
