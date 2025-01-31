# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""This module is a collection of independent, basic functions, which are used
in the project multiple places.

Libs
----
* uuid
* hashlib

Help
----
* https://www.pythoncentral.io/hashing-strings-with-python/

Contents
--------
"""
import secrets
import string
import time
import uuid
import hashlib


class InputError(Exception):
    """ Exception for InputValidatorBaseClass. """


class InputValidatorBaseClass:
    """ Validator object, used for converting textfield inputs. Class methods
    are always returning a value (converted or fallback (default)) and an error
    message for displaying purposes in PyQt dialogs.
    """
    def __init__(self):
        pass

    # pylint: disable = no-self-argument, lost-exception, raise-missing-from
    def _validate(func):
        """ Decorator function, to wrap function in a try-catch block.

        The purpose of this function to catch and handle user input errors and
        typing mistakes (trailing or leading spaces, underlines as separators
        in large integers), and either handle it internally (if missing, using
        default value), or raise Exception, to catch it in the main loop, to
        allow correction. No need for 'self' as argument.
        """
        def inner(self, *args, **kwargs):
            error_msg = ""  # Msg for user! Default is empty.
            value = args[0]
            output = kwargs.get("default", None)  # Fallback, if input is missing.

            try:
                # Checking if textfield was empty ("" or None)
                if not (value == "" or value is None):
                    # pylint: disable = not-callable
                    output = func(self, *args, **kwargs)

                return output

            # Logging exceptions:
            except TypeError as e_msg:
                error_msg = f"TypeError ({value})"
                raise InputError(error_msg) from None

            except ValueError as e_msg:
                error_msg = f"ValueError ({value})"
                raise InputError(error_msg) from None

            except Exception as e_msg:
                error_msg = f"Unexpected error ({value}): {e_msg}"
                raise InputError(error_msg) from None

        return inner

    # pylint: disable = unused-argument
    @_validate
    def ival(self, value, default=None):
        """ Returns input converted to integer.

        :return: output
        :rytpe: int
        """
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        # Removes spaces and '_' from input, before tries to convert to int
        return int(value.replace(" ", "").replace("_", ""))

    # pylint: disable = unused-argument
    @_validate
    def fval(self, value, default=None):
        """ Returns input converted to float.

        :return: output
        :rytpe: float
        """
        if isinstance(value, float):
            return value

        if isinstance(value, int):
            return float(value)

        # Removes spaces and '_' from input, before tries to convert to int
        return float(value.replace(" ", "").replace("_", ""))

    # pylint: disable = unused-argument
    @_validate
    def sval(self, value, default=None, chars=30, suffix=""):
        """ Returns input converted to string. After conversion truncates
        string to 'chars' length and adds suffix.

        :return: output
        :rytpe: str
        """
        output = str(value)
        return output.strip()[:chars] + suffix

    # pylint: disable = unused-argument
    @_validate
    def pval(self, value, default=None, chars=30):
        """ Converts input to string, removes trailing spaces, replaces any
        remaining space with '_'. Changes all characters lowercase and truncates
        string to 'chars' length.

        :return: (output, massage)
        :rytpe: (str, str)
        """
        output = str(value)
        return output.strip().replace(" ", "_").lower()[:chars]

    # def is_within_limits(int, lower, upper):

    #      # if lower_limit is not None and

    #     return int(value)


def get_actual_time():
    """Formats the actual time.

    :return: Actual time, in the following format: YYYY-MM-DD HH:MM:SS
    :rtype: str

    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def generate_uuid_string():
    """Generate UUID string.

    :return: UUID string.
    :rtype: str

    """
    return str(uuid.uuid4())


def reset_password():
    """Generate random string, hashes it, then return both.

    :return: (raw_password, hashed_password)
    :rytpe: (str, str)

    """
    letter_pool = string.ascii_uppercase + string.ascii_lowercase + string.digits
    temp_password_raw = ''.join(secrets.choice(letter_pool) for _ in range(6))
    return temp_password_raw, hash_password(temp_password_raw)


def hash_password(password):
    """Generates a hashed password using uuid for salting.

    :param str password: User password.
    :return: Hashed password.
    :rtype: str

    """
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, raw_password):
    """Check if raw password matches with hashed password.

    :param str hashed_password: Hashed password.
    :param str raw_password: Password without encrypting.
    :return: Hashed and raw password match, or not.
    :rtype: bool

    """
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + raw_password.encode()).hexdigest()


if __name__ == '__main__':
    pass
