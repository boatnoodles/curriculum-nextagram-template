import re
from peewee_validates import ModelValidator, validate_length
from models.user import User


class FormValidator(ModelValidator):
    class Meta:
        messages = {
            'email.required': 'Email is required',
            'password.required': 'Password is required',
            'username.required': 'Username is required',
            'email.unique': 'An account is already registered to this email',
            'username.unique': 'Username taken'
        }


def valid_length(field, min, max):
    """Checks if length requirements are fulfilled"""
    length = len(field)
    if length >= min and length <= max:
        return True
    elif length < min:
        return "too short"
    elif length > max:
        return "too long"


def length_validation(**fields):
    errors = {}
    for key, value in fields.items():
        res = valid_length(value, 6, 255)
        # Checks length of username, password
        if res == True:
            pass
        else:
            errors[key] = f"{key} is {res}"
    return errors


def pw_complexity(password):
    if re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', password):
        return True
    return False


def email_validity(email):
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$', email):
        return True
    return False
