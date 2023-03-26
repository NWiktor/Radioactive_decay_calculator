# -*- coding: utf-8 -*-
#!/usr/bin/python3

# TODO: Rewrite documentation
"""This module collects the database entry classes for the SeatUP project. The
main purpose of the classes are, to ensure every key is included in the entry,
and has a default value. Moreover, obsolete keys (which are not defined here)
will be filtered out automatically.

Contents
--------
"""

from logger import MAIN_LOGGER as l


class EntryObjectBaseClass():
    """  """

    def __init__(self):
        pass


    def dump_data(self):
        """Returns a dictionary with entry data."""
        return self.__dict__.copy()


    def clear(self):
        """Erases all loaded and existing data to allow refresh."""
        self.__dict__ = {}


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


# TODO: rework this section
# class IsotopeEntry(EntryObjectBaseClass):
#    """This class is intended to initialize a JSON settings entry."""


# class Isotope:
#   def __init__(name, symbol, proton_number, neutron_number):
#       self.name = name
#       self.symbol = symbol
#       self.proton_number = proton_number
#       self.neutron_number = neutron_number
#       self.mass_number = proton_number + neutron_number
#       self.short_id = f"{name}-{proton_number}"
#       self.decays = {} # dict of dicts - multiple decay is possible, each of them with multiple products


    # def __init__(self, raw_settings):
    #     self.total_holidays = raw_settings.get("total_holidays", {})
    #     self.week_schedule = raw_settings.get("week_schedule", [8,8,8,8,8,0,0])
    #     self.start_fullscreen = raw_settings.get("start_fullscreen", False)
    #     self.shown_projects = raw_settings.get("shown_projects", [])
    #     self.absolute_overwork_limit = raw_settings.get("absolute_overwork_limit", 12) # This cannot be exceeded in any case
    #     self.overwork_limit = raw_settings.get("overwork_limit", 8) # Below this, no overwork signal
    #     self.completeness_percentage = raw_settings.get("completeness_percentage", 0.5) # Minimum % value to show completed day
    #     l.info("Settings initialized!")


if __name__ == '__main__':
    pass
