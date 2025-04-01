from task_classes import AddressBook, Record
import pickle

# decorator for exceptions
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0] # we return args of error, in order to know what kind of error we catch
        except IndexError:
            return 'This contact cannot be added, it already exists.'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner


# function for greeting

def greeting():
    return 'How can I help you?'

# add contact in dict and check the number of args
@input_error
def add_contact(book, *args):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    
@input_error
def add_phone(book, *args):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        message = "This contact isn`t in your addressbook."
    elif phone:
        record.add_phone(phone)
        message = f"Contact  {name} birthday is added."
    return message

# check the number of args, change phone of contact 
@input_error
def change_contact(book, *args):
    #if len(args) < 2:
    #    return 'Not enough arguments'
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        message = "This contact isn`t in your addressbook."
    else:
        record.edit_phone(old_phone, new_phone)
        message = f'Contact  {name} changed'
    return message

# check contacts existance and show contact information when contacts exist
@input_error
def show_phone(book, *args):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = "This contact isn`t in your addressbook."
    else:
        message = f"Contact name: {record.name.value},  phones: {'; '.join(p.value for p in record.phones)}"
    return message    


def show_all(book):
    return book
    
@input_error
def add_birthday(book, *args):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        message = "This contact isn`t in your addressbook."
    elif birthday:
        record.add_birthday(birthday)
        message = f"Contact  {name} birthday is added."
    return message

@input_error
def show_birthday(book, *args):
    name, *_ = args
    record = book.find(name)
    if record is None:
        message = "This contact isn`t in your addressbook."
    else:
        message = record.birthday.value
    return message    

@input_error
def birthdays(book):
    bith_list = book.get_upcoming_birthdays()
    if not bith_list:
        message = "None of the contacts have a birthday in the next 7 days."
    else:
        message = f'\n'.join([f"Name: {item['name']}, Day for congratulations: {item['birthday'].strftime('%d.%m.%Y')}" for item in bith_list])
    return message   


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення
    
# dict with commands as keys and function as values    
COMMAND_HANDLER = {
                   'hello': greeting,
                   'add': add_contact,
                   'add-phone': add_phone,
                   'change': change_contact,
                   'phone': show_phone,
                   'all': show_all,
                   'add-birthday':add_birthday,
                   'show-birthday': show_birthday,
                   'birthdays': birthdays
                   }


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
  
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit"]:
            save_data(book)
            print("Good bye!")
            break
        # there commands are turn into function calling
        elif command in COMMAND_HANDLER:
            result = COMMAND_HANDLER.get(command)(book, *args)
            print(result)
        
        else:
            print("Invalid command.")

if __name__ == "__main__":
    
    main()
    

