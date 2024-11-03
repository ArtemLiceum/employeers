import sqlite3
import sys
from employee import Employee


class DatabaseHandler:
    def __init__(self, database):
        try:
            self.conn = sqlite3.connect(database)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error connecting to database: {e}\n")
            sys.exit(1)

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    full_name TEXT,
                    birth_date TEXT,
                    gender TEXT
                );
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error creating table: {e}\n")

    def insert_employee(self, employee):
        try:
            self.cursor.execute("""
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (?, ?, ?)
            """, (employee.full_name, employee.birth_date, employee.gender))
            self.conn.commit()
        except sqlite3.IntegrityError:
            sys.stderr.write("Record already exists.\n")
        except sqlite3.Error as e:
            sys.stderr.write(f"Error inserting employee: {e}\n")

    def fetch_all_employees(self):
        try:
            self.cursor.execute("""
                SELECT DISTINCT full_name, birth_date, gender
                FROM employees
                ORDER BY full_name
            """)
            rows = self.cursor.fetchall()

            employees = []
            for row in rows:
                full_name, birth_date, gender = row
                emp = Employee(full_name, birth_date, gender)
                age = emp.calculate_age()
                employees.append((full_name, birth_date, gender, age))

            return employees
        except sqlite3.Error as e:
            sys.stderr.write(f"Error fetching employees: {e}\n")
            return []

    def batch_insert_employees(self, employees):
        try:
            self.cursor.executemany("""
                INSERT INTO employees (full_name, birth_date, gender)
                VALUES (?, ?, ?)
            """, [(emp.full_name, emp.birth_date, emp.gender) for emp in employees])
            self.conn.commit()
        except sqlite3.IntegrityError:
            sys.stderr.write("One or more records already exist.\n")
        except sqlite3.Error as e:
            sys.stderr.write(f"Error in batch insert: {e}\n")

    def fetch_male_f_employees(self):
        try:
            self.cursor.execute("""
                SELECT full_name, birth_date, gender FROM employees
                WHERE gender = 'Male' AND full_name LIKE 'F%'
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error fetching male employees with names starting with 'F': {e}\n")
            return []

    def optimize_database(self):
        try:
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_male_f
                ON employees (full_name)
                WHERE full_name LIKE 'F%' AND gender = 'Male';
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error optimizing database: {e}\n")

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            sys.stderr.write(f"Error closing database connection: {e}\n")
