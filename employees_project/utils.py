import random
import string


def generate_random_name():
    first_letter = random.choice(string.ascii_uppercase)
    last_name = first_letter + ''.join(random.choices(string.ascii_lowercase, k=5))
    first_name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    middle_name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    return f"{last_name} {first_name} {middle_name}"


def generate_random_date(start_year=1960, end_year=2000):
    try:
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"
    except ValueError as e:
        print(f"Error generating random date: {e}")
        return "1960-01-01"
