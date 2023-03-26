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


    def dump(self):
        """Returns a dictionary with entry data."""
        return self.__dict__.copy()


    def clear(self):
        """Erases all loaded and existing data to allow refresh."""
        self.__dict__ = {}


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class IsotopeEntry(EntryObjectBaseClass):
   """This class is intended to initialize a JSON settings entry."""

    # TODO: Kell ez a fv. ? Összedolgozni a load()-al?
    def create(self, name, symbol, mass_number, proton_number=None, neutron_number=None):
        """ Create new isotrope entry, with minimum data. """
        self.name = name
        self.symbol = symbol
        self.mass_number = mass_number
        self.proton_number = proton_number
        self.neutron_number = neutron_number
        self.short_id = f"{name}-{mass_number}"
        self.reference = None
        self.half_life = None
        self.decays = None # dict of dicts - multiple decay type is possible
        l.info("Entry created!")


    def load(self, raw_data):
        """ Load existing data (dict) to class structure, to filter entry, and set defaults. """
        self.name = raw_data.get("name", None)
        self.symbol = raw_data.get("symbol", None)
        self.mass_number = raw_data.get("mass_number", None)
        self.proton_number = raw_data.get("proton_number", None)
        self.neutron_number = raw_data.get("neutron_number", None)
        self.short_id = raw_data.get("short_id", None)
        self.reference = raw_data.get("reference", None)
        self.half_life = raw_data.get("half_life", None)

        if self.half_life is None:
            self.decays = None

        else:
            raw_decay_data = raw_data.get("decays", None)
            if raw_decay_data is not None
                self.decays = self._load_decays(raw_decay_data)

            else:
                l.error("Undefined decay for unstable isotope! Please check input data!")
                self.decays = None

        l.info("Entry loaded!")


    def _load_decays(self, raw_data):
        """  """
        decays = {}
        for decay, decay_data in raw_data.items():
            product = decay_data.get("product", None)
            released_energy = decay_data.get("released_energy", None)
            probability = decay_data.get("probability", 1.0)
            decays.update(self._create_decay(decay, product, released_energy, probability))

        self.decays = decays
        l.info("Decays loaded!")


    def _create_decay(self, decay_type, product, probability, released_energy):
        """  """
        decay = {decay_type : {
        "product" : product,
        "probability": probability,
        "released_energy" : released_energy
        }}
        return decay


if __name__ == '__main__':
    pass
