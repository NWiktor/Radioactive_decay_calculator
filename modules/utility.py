# -*- coding: utf-8 -*-
#!/usr/bin/python3

"""This module is a collection of independent, basic functions, which are used regularly.

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
import calendar
import uuid
import hashlib


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
    """Generate random string and hashes it."""
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
