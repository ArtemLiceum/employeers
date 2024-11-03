import sys
import sqlite3
from datetime import datetime, date


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        try:
            birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
            today = date.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except ValueError as e:
            print(f"Error calculating age: {e}")
            return None

    def save_to_db(self, db):
        try:
            db.insert_employee(self)
        except sqlite3.Error as e:
            sys.stderr.write(f"Error saving employee to database: {e}\n")
