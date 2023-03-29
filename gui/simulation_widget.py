# -*- coding: utf-8 -*-
#!/usr/bin/python3

""" Summary of this code file goes here. The purpose of this module can be
expanded in multiple sentences. Below a short free-text summary of the included
classes and functions to give an overview. More detailed summary of the
functions can be provided inside the function's body.

Libs
----
* some_module - This is used for imported, non-standard modules, to help track
    dependencies. Summary is not needed.

Help
----
* https://blog.logrocket.com/how-to-build-gui-pyqt/

Contents
--------
"""

# Standard library imports
# First import should be the logging module if any!
from copy import deepcopy

# Third party imports
# pylint: disable = no-name-in-module
from PyQt5.QtWidgets import (QWidget,
QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QMenu,
QPushButton, QComboBox, QListWidget, QLabel)
from PyQt5.QtCore import QEvent, Qt

# Local application imports
from logger import MAIN_LOGGER as l

# Class and function definitions
class SimulationWidget(QWidget):
    """Widget for simulation parameter input."""

    def __init__(self, idb):
        super().__init__()

        # Initialize window
        # TODO: enable it in production code:
        # self.isotopes_list = {}
        # TODO: remove this from production code:
        self.isotopes_list = {"Ra-225": 10, "Ac-225": 10}
        self._idb = idb

        # Add Widgets
        self.layout = QVBoxLayout()
        self._create_fields()
        self._create_buttons()
        self._create_listview()
        self.setLayout(self.layout)


    def _create_fields(self):
        """  """
        form_layout = QFormLayout()
        self.interval = QLineEdit(str(500))
        self.interval.setFixedWidth(70)
        form_layout.addRow(QLabel("Time interval [s]"), self.interval)
        self.step_number = QLineEdit(str(15000))
        self.step_number.setFixedWidth(70)
        form_layout.addRow(QLabel("Number of steps"), self.step_number)
        self.isotope_name_cbox = QComboBox()
        self.isotope_name_cbox.addItems(self._idb.keys())
        self.isotope_name_cbox.setEditable(False)
        self.isotope_name_cbox.setFixedWidth(70)
        self.isotope_name_cbox.setInsertPolicy(QComboBox.InsertAlphabetically)
        form_layout.addRow(QLabel("Isotope name"), self.isotope_name_cbox)

        self.isotope_mass = QLineEdit(str(""))
        self.isotope_mass.setFixedWidth(70)
        form_layout.addRow(QLabel("Isotope mass [kg]"), self.isotope_mass)
        self.layout.addLayout(form_layout)


    def _create_buttons(self):
        """  """
        button_box = QHBoxLayout()
        button_accept = QPushButton("Add")
        button_accept.clicked.connect(self.accept_input)
        button_box.addWidget(button_accept)
        button_box.addStretch()
        self.layout.addLayout(button_box)


    def _create_listview(self):
        """  """
        self.layout.addWidget(QLabel("Starting isotopes"))
        self.shown_iso_list_widget = QListWidget()
        for name, mass in self.isotopes_list.items():
            self.shown_iso_list_widget.addItem(f"{name} - {mass} [kg]")
        self.shown_iso_list_widget.installEventFilter(self)
        self.layout.addWidget(self.shown_iso_list_widget)


    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.shown_iso_list_widget:
            menu = QMenu()
            menu.addAction('Delete')
            # menu.addAction('Action 2')
            #menu.addAction('Action 3')

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                key = (item.text().split(" ")[0])
                self.isotopes_list.pop(key)
                self.refresh_listview()

            return True
        return super().eventFilter(source, event)


    def accept_input(self):
        """  """
        try:
            name = self.isotope_name_cbox.currentText().strip()
            mass = float(self.isotope_mass.text().strip())

        except:
            l.error("Wrong input for mass value!")
            return

        self.isotopes_list.update({name: mass})
        self.refresh_listview()


    def refresh_listview(self):
        """ Clear listview and repopulate. """
        self.shown_iso_list_widget.clear()
        for name, mass in self.isotopes_list.items():
            self.shown_iso_list_widget.addItem(f"{name} - {mass} [kg]")
        l.debug("Isotopes for calculation: %s", self.isotopes_list)


    def get_simulation_parameters(self):
        """  """
        return (deepcopy(self.isotopes_list),
            int(self.interval.text().strip()), int(self.step_number.text().strip()))


# Include guard
if __name__ == '__main__':
    pass
