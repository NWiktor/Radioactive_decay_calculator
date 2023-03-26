# -*- coding: utf-8 -*-
#!/usr/bin/python3

""" Logger modul for other programs/apps. This modul contains all settings
for the logger, which saves the logs of the last five run.

Help
----
* https://www.toptal.com/python/in-depth-python-logging
* https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules
* https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller

Contents
--------
"""


import logging
import os
import sys
from logging.handlers import RotatingFileHandler


# Ha ez nincs, akkor .exe file nem működik!
if getattr(sys, 'frozen', False):
    initdir = os.path.dirname(sys.executable)
elif __file__:
    initdir = os.path.dirname(__file__)

LOG_DIRPATH = "log/"
LOG_FILENAME = "main.txt"

# Ha a naplófájl mappa hiányzik, létrehozom
if not os.path.isdir(os.path.join(initdir, LOG_DIRPATH)):
    os.mkdir(os.path.join(initdir, LOG_DIRPATH))

LOG_FILE = os.path.join(initdir, LOG_DIRPATH, LOG_FILENAME)
FORMATTER = logging.Formatter(
'%(asctime)s %(module)s [%(levelname)s] : %(message)s',
datefmt='%Y/%m/%d %H:%M:%S')

MAIN_LOGGER = None

def init_logger():
    """ Initializes a logger named *'Main'* for all modules.

    This function is called when this module is first imported. When this
    happens, it creates a logger, which is intended to used by every other
    modules. The logger level is DEBUG, as it is intended to catch every
    log message. **EVERY MODUL WITHIN THIS PROJECT SCOPE MUST USE THE FOLLOWING
    SYNTAX AT THE HEADER TO ACCESS THIS LOGGER:**

    .. code-block::

       from logger import MAIN_LOGGER as l

    The logger consists of two log handler: a console handler, and filehandler,
    the latter uses filerotating and stores the logs of the last five (5)
    running.
    """

    global MAIN_LOGGER

    MAIN_LOGGER = logging.getLogger("Main")
    MAIN_LOGGER.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(FORMATTER)
    MAIN_LOGGER.addHandler(console_handler)

    # Nincs felső byte limit - max. 5 indítás logját tartalmazza
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=0, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(FORMATTER)
    file_handler.doRollover() # Átforgatja a logot minden indításnál
    MAIN_LOGGER.addHandler(file_handler) # Format, és file handler beállítások
    MAIN_LOGGER.info("Main logger created!")


# Running script:
init_logger() # Initializes logger for all the modules


## Modul-teszt
if __name__ == "__main__":
    pass
