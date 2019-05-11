import re
from models.user import User
from peewee_validates import ModelValidator, validate_length


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


def form_validation(fields):
    """Validates the field passed in by the user via the sign up form"""

    errors = {}

    for k, v in fields.items():
        if k == "username":
            errors.update(length_validation(Username=v))
            pass

        elif k == "email":
            errors.update(length_validation(Email=v))

            # Check if email is of a valid format
            if not email_validity(fields["email"]):
                errors.update({"email": "Enter a valid email"})
            pass

        elif k == "password":

            # Check if passwords match
            if fields["password"] != fields["confirm"]:
                errors.update({"password": "Passwords do not match"})

            # Check for password complexity
            if not pw_complexity(fields["password"]):
                errors.update(
                    {"password": "Include at least one uppercase letter, one lowercase letter, one number and one special character"})
            pass

    return errors


def update_queries(to_be_changed, **fields):
    # queries = {User.privacy: fields.privacy}
    queries = {}
    for k, v in to_be_changed.items():
        if k == "username":
            queries.update({User.username: v})
            pass
        elif k == "email":
            queries.update({User.email: v})
            pass
        elif k == "password":
            queries.update({User.password: v})
            pass
        elif k == "profile_picture":
            queries.update({User.profile_picture: v})
            pass
    return queries
