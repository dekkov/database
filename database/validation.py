import re


def is_valid_name(name):
    """Validates a name with the folowing format: Firstname Lastname"""

    if re.match(r"^[a-zA-Z]+ [a-zA-Z]+$", name):
        return True
    else:
        return False


def is_valid_email(email):
    """Validates an email address with the folowing format: email@domain.com"""

    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    else:
        return False


def is_valid_phone(phone):
    """Validates a phone number with the folowing format: (123) 456-7890"""

    if re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone):
        return True
    else:
        return False
