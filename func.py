
from datetime import timedelta
import colorama
from colorama import Fore
colorama.init(autoreset=True)
import Record
import AddressBook

def adjust_for_weekend(date):
    weekday = date.weekday()
    if weekday == 5:  # якщо др випадає на суботу
        return date + timedelta(days=2)
    elif weekday == 6:  # якщо др випадає на неділю
        return date + timedelta(days=1)
    return date

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return (Fore.RED + f"ValueError: {str(e)}\nPlease provide correct arguments.")
        except KeyError as k:
            return (Fore.RED + f"KeyError: {str(k)}\nEnter a valid command again\n")
        except IndexError as i:
            return (Fore.RED + f"IndexError: {str(i)} Invalid number of arguments.")
        
    return inner

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please, try again.")
    name, phone = args[:2]
    record = book.find(name)
    message = Fore.GREEN + "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = Fore.GREEN + "Contact added."
    record.add_phone(phone)
    return message

@input_error
def delete_contact(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please, try again.")
    name = args[0]
    record = book.find(name)
    if record:
        del book[name]
        return Fore.GREEN + "Contact deleted"
    else:
        return Fore.YELLOW + "Contact not found."

@input_error
def delete_phone(args, book):
    if len(args) < 1:
        raise ValueError("Wrong command to delete users phone. Please enter command 'delete-phone' + 'name' + 'phone number'")
    name, phone = args
    record = book.find(name)
    if record:
        record.remove_phone(phone)
        return Fore.GREEN + "Phone number deleted."
    else:
        return Fore.YELLOW + "Contact not found."
    
@input_error
def change_phone(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return Fore.GREEN + "Phone number updated."
    else:
        return Fore.YELLOW + "Contact not found."

@input_error
def show_phone(args, book):
    if len(args) < 1:
        raise ValueError("Wrong command to show users phone. Please enter command 'phone' and 'name'")
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(str(p) for p in record.phones)
        return Fore.GREEN + f"Phone number: {phones}" if phones else Fore.YELLOW + "No phone numbers found."
    else:
        return Fore.YELLOW + "Contact not found."

@input_error
def show_all(book:AddressBook):
    records_info = "\n".join(str(record) for record in book.values())
    return records_info if records_info else Fore.YELLOW + "No contacts found."

@input_error
def add_birthday(args, book:AddressBook):
    if len(args) < 2:
        raise ValueError("Wrong command to add birthday. Please enter command 'add-birthday' + 'name' + 'date of birthday'")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return Fore.GREEN + "Birthday added."
    else:
        return Fore.YELLOW + "Contact not found."

@input_error
def show_birthday(args, book:AddressBook):
    if len(args) < 1:
        raise ValueError("Wrong command to show birthday. Please enter command 'show-birthday' and 'name'")
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return Fore.GREEN + f"Birthday: {record.birthday}"
        else:
            return Fore.YELLOW + "Birthday not set."
    else:
        return Fore.YELLOW + "Contact not found."