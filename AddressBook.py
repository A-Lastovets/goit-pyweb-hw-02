from datetime import datetime, timedelta
import colorama
from colorama import Fore
colorama.init(autoreset=True)
from Record import *
from func import *

class AddressBook(dict):
    def add_record(self, record):
        self[record.name.value] = record
        
    def find(self, name):
        return self.get(name)

    def get_upcoming_birthdays(self, days=7):
        current_date = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.values():
            adjusted_birthday = adjust_for_weekend()
            if record.birthday:
                birthday_date = record.birthday.value
                birthday_this_year = birthday_date.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)
            days_difference = (birthday_this_year - current_date).days
            if 0 <= days_difference <= days:
                adjusted_birthday = adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append(
                    {
                    'name': record.name.value.title(),
                    'congratulation_date': str(adjusted_birthday)
                    }
                    )
        return upcoming_birthdays

    def birthdays(book):
        upcoming_birthdays = book.get_upcoming_birthdays()
        if upcoming_birthdays:
            return Fore.RED + "Upcoming birthdays: \n" + Fore.GREEN + "\n".join(str(record) for record in upcoming_birthdays).replace('{', '').replace('}', '').replace("'", "")
        else:
            return Fore.YELLOW + "No upcoming birthdays."