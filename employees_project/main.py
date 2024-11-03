import sys
import random
from datetime import datetime
from employee import Employee
from database import DatabaseHandler
from utils import generate_random_name, generate_random_date

DATABASE = "employees.db"


def mode_1(db):
    db.create_table()
    print("Table created.")


def mode_2(db, args):
    try:
        full_name, birth_date, gender = args
        employee = Employee(full_name, birth_date, gender)
        employee.save_to_db(db)
        print(f"Employee {full_name} added.")
    except (ValueError, IndexError) as e:
        sys.stderr.write(f"Error in mode 2 arguments: {e}\n")


def mode_3(db):
    employees = db.fetch_all_employees()
    for full_name, birth_date, gender, age in employees:
        if age is not None:
            print(f"{full_name}, {birth_date}, {gender}, {age} years old")
        else:
            print(f"{full_name}, {birth_date}, {gender}, age calculation error")


def mode_4(db):
    try:
        employees = []
        for _ in range(1000000):
            gender = random.choice(["Male", "Female"])
            full_name = generate_random_name()
            birth_date = generate_random_date()
            employees.append(Employee(full_name, birth_date, gender))
        for _ in range(100):
            full_name = "F" + generate_random_name()[1:]
            birth_date = generate_random_date()
            employees.append(Employee(full_name, birth_date, "Male"))
        db.batch_insert_employees(employees)
        print("Batch of 1,000,100 employees inserted.")
    except Exception as e:
        sys.stderr.write(f"Error in mode 4 batch insertion: {e}\n")


def mode_5(db):
    try:
        start_time = datetime.now()
        employees = db.fetch_male_f_employees()
        end_time = datetime.now()
        for full_name, birth_date, gender in employees:
            print(f"{full_name}, {birth_date}, {gender}")
        print("Query time:", (end_time - start_time))
    except Exception as e:
        sys.stderr.write(f"Error in mode 5 query: {e}\n")


def mode_6(db):
    try:
        db.optimize_database()
        start_time = datetime.now()
        employees = db.fetch_male_f_employees()
        end_time = datetime.now()
        for full_name, birth_date, gender in employees:
            print(f"{full_name}, {birth_date}, {gender}")
        print("Optimized query time:", (end_time - start_time))
    except Exception as e:
        sys.stderr.write(f"Error in mode 6 optimized query: {e}\n")


def main():
    db = DatabaseHandler(DATABASE)
    try:
        mode = int(sys.argv[1])
    except (IndexError, ValueError) as e:
        sys.stderr.write(f"Invalid mode argument: {e}\n")
        sys.exit(1)

    if mode == 1:
        mode_1(db)
    elif mode == 2:
        if len(sys.argv) < 5:
            sys.stderr.write("Insufficient arguments for mode 2\n")
        else:
            mode_2(db, sys.argv[2:])
    elif mode == 3:
        mode_3(db)
    elif mode == 4:
        mode_4(db)
    elif mode == 5:
        mode_5(db)
    elif mode == 6:
        mode_6(db)
    else:
        sys.stderr.write("Invalid mode selected.\n")

    db.close()


if __name__ == "__main__":
    main()
