from collections import UserDict
import datetime 


class Field:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return str(self.value)
    
#class ValueError(Exception):
#    pass    

class Name(Field):
    def __init__(self, value:str):
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            check_value = datetime.datetime.strptime(value, '%d.%m.%Y')
            
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        self.value = check_value.strftime('%d.%m.%Y')
        
          
class Phone(Field):
    def __init__(self, value:str):
        if len(value) == 10 and value.isdigit(): # checking
           self.value = value
        else:
            raise ValueError ("Phone number has wrong format")
 
    def __eq__(self, value: object) -> bool:
        return self.value == value
        

class Record:
    def __init__(self, name:str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)   

    def add_phone(self, phone:str):
        self.phones.append(Phone(phone))
        
    
    def remove_phone(self, phone:str):
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            return f"Phone {phone} is not in record"
        
    def edit_phone(self, old_phone:str, new_phone:str):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        if old_phone in self.phones:
            self.phones.remove(old_phone)
            self.phones.append(new_phone)
        else:
            raise ValueError   

    def find_phone(self, phone:str):
        for  item in self.phones:
            if item == phone:
                return item 
        return None


    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"
        return f"Contact name: {self.name.value},  phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}


    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None
    
    def get_upcoming_birthdays(self):
        week_birth = []
        one_birth = {}

        current_day = datetime.datetime.today() # get current date
        for name, record in self.data.items():

            if record.birthday:
                day_for_congrats = datetime.datetime.strptime(record.birthday.value, '%d.%m.%Y').replace(year=current_day.year) 
                               
                if day_for_congrats - current_day < datetime.timedelta(days=7):
                    if day_for_congrats.weekday() < 5:
                        one_birth = {'name': name, 'birthday': day_for_congrats.date()}
                    else:
                        one_birth = {'name': name, 'birthday': day_for_congrats.date() + datetime.timedelta(days=2) if day_for_congrats.weekday() == 5\
                                else day_for_congrats.date() + datetime.timedelta(days=1)}          
                        
                         
                    week_birth.append(one_birth)
        return  week_birth
    
    def delete(self, name:str):
        self.data.pop(name, None)

    def __str__(self):
        return  '\n'.join([str(i) for i in self.values()])
    
# Створення нової адресної книги
#book = AddressBook()

# Створення запису для John
#john_record = Record("John")

#john_record.add_phone("1234567890")
#john_record.add_phone("5555555555")
#print(john_record)
#book.add_record(john_record)
#timi_record = Record("Timi")
#timi_record.add_phone("9875687654")
#timi_record.add_birthday('24.03.2000')
#sofi_record = Record("Sofi")
#sofi_record.add_phone("9876597436")
#sofi_record.add_birthday('29.03.2022')
##yus_record = Record("Yusik")
#yus_record.add_phone("8754354321")
#yus_record.add_birthday('30.03.2022')
#print(timi_record)
#print(type(timi_record.birthday.value))
#book.add_record(timi_record)
#book.add_record(sofi_record)
#book.add_record(yus_record)
#print(book.get_upcoming_birthdays())

    # Виведення всіх записів у книзі
     
#print(book)
#john = book.find("John")
#print(john)
#found_phone = john.find_phone("5555555555")
#print(f"{john.name}: {found_phone}")
#john_record.remove_phone("1234567890")
#print(john_record)
##john_record.edit_phone("5555555555", "0987654321")
#print(john_record)
#john_record.edit_phone("0987654321", "0454588787")
#john.add_phone('1234567890')
#book.delete("Jane")
#print(book)