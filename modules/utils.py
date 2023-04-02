# -*- coding: utf-8 -*-
#!/usr/bin/python3

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
    pass


class InputValidatorBaseClass():
    """  """

    def __init__(self):
        pass


    def _validate(func):
        """ Decorator function, to wrap function in a try-catch block. """


        def inner(self, *args, **kwargs):
            error_msg = "" # Msg for user! Default is empty.
            value = args[0]
            output = kwargs.get("default", None) # Default, if try fails

            try:
                # Checking if the textfield was empty ("" or None)
                if value == "" or value is None:
                    raise InputError()

                # Try to run the function
                output = func(self, *args, **kwargs)

            ## Logs exceptions
            except InputError: # Custom exception for my own messages!
                error_msg = f"InputError ({value}): Input is missing, using default value: {output}" 
                # l.info(error_msg)

            except TypeError as e_msg:
                error_msg = f"TypeError ({value}): {e_msg}"
                # l.info(error_msg)

            except ValueError as e_msg:
                error_msg = f"ValueError ({value}): {e_msg}"
                # l.info(error_msg)

            except Exception as e_msg:
                error_msg = f"Unexpected error ({value}): {e_msg}"
                # l.info(error_msg)

            finally:
                # Return output and error message
                # print(error_msg)
                return output, error_msg

        return inner


    @_validate
    def ival(self, value, default=None):
        """  """
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        else:
            # Removes spaces and '_' from input, before tries to convert to int
            return int(value.replace(" ","").replace("_",""))


    @_validate
    def fval(self, value, default=None):
        """  """
        if isinstance(value, float):
            return value

        if isinstance(value, int):
            return float(value)

        else:
            # Removes spaces and '_' from input, before tries to convert to int
            return float(value.replace(" ","").replace("_",""))


    @_validate
    def sval(self, value, default=None, chars=30, suffix=""):
        """  """
        output = str(value)
        return output.strip()[:chars] + suffix


    @_validate
    def pval(self, value, default=None, chars=30):
        """ Converts input to string, removes trailing spaces, replace any remaining
        space with '_'. Finally change all characters lowercase.
        """
        output = str(output)
        return output.strip().replace(" ","_").lower()[:chars]


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
    temp_password_raw = ''.join(secrets.choice(letter_pool) for i in range(6))
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
