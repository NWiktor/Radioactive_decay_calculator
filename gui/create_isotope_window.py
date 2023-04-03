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

# Third party imports
# pylint: disable = no-name-in-module
from PyQt5.QtWidgets import (QDialog, QWidget,
QFormLayout, QCheckBox,QLineEdit, QVBoxLayout,
QHBoxLayout, QGridLayout, QPushButton, QComboBox,
QLabel, QCompleter)
from PyQt5.QtCore import Qt

# Local application imports
from logger import MAIN_LOGGER as l
from modules.entry_objects import IsotopeEntry
from modules.utils import InputValidatorBaseClass, InputError


class ChooseIsotopeWindow(QDialog):
    """ Isotope combobox window for PyQt5.
    """

    def __init__(self, keys):
        super().__init__(parent=None)
        self.setWindowTitle("Choose isotope")
        self.keys = keys
        self.results = None

        # Initialize window
        self.layout = QVBoxLayout()
        self._create_fields()
        self._create_buttons()
        self.setLayout(self.layout)


    def _create_fields(self):
        """  """
        form_layout = QFormLayout()
        self.isotope_name_cbox = QComboBox() # Isotope name Cbox
        self.isotope_name_cbox.addItems(sorted(self.keys))
        self.isotope_name_cbox.setFixedWidth(70)
        self.isotope_name_cbox.setEditable(True)
        self.isotope_name_cbox.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.isotope_name_cbox.setInsertPolicy(QComboBox.NoInsert)
        form_layout.addRow(QLabel("Choose to edit:"), self.isotope_name_cbox)
        self.layout.addLayout(form_layout)


    def _create_buttons(self):
        """  """
        button_box = QHBoxLayout()
        button_box.addStretch()
        button_accept = QPushButton("OK")
        button_accept.clicked.connect(self.accept_input)
        button_close = QPushButton("Cancel")
        button_close.clicked.connect(self.close_window)
        button_box.addWidget(button_accept)
        button_box.addWidget(button_close)
        self.layout.addLayout(button_box)


    def accept_input(self):
        name = self.isotope_name_cbox.currentText()
        self.results = name
        self.close()


    # pylint: disable = missing-function-docstring
    def close_window(self):
        self.close()


# Class and function definitions
class CreateIsotopeWindow(QDialog):
    """Isotope creation window for PyQt5.
    """

    def __init__(self, default_data=None):
        super().__init__(parent=None)
        self.setWindowTitle("Create new isotope")
        self.results = None

        # Initialize window
        self.layout = QGridLayout()
        self._create_fields()
        self._create_decay_field()
        self._create_buttons()
        if default_data is not None:
            self.add_default_values(default_data)
        self.setLayout(self.layout)


    def _create_fields(self):
        """  """
        # header
        field_layout = QVBoxLayout()
        field_layout.addWidget(QLabel("Isotope properties"), alignment=Qt.AlignCenter)

        # name
        form_layout1 = QFormLayout()
        isotope_name_label = QLabel("Isotope name*")
        isotope_name_label.setFixedWidth(135)
        self.isotope_name = QLineEdit("")
        self.isotope_name.setPlaceholderText("e.g. Uranium")
        self.isotope_name.setFixedWidth(100)
        form_layout1.addRow(isotope_name_label, self.isotope_name)

        # symbol
        self.isotope_symbol = QLineEdit("")
        self.isotope_symbol.setPlaceholderText("e.g. U")
        self.isotope_symbol.setFixedWidth(100)
        form_layout1.addRow(QLabel("Symbol*"), self.isotope_symbol)

        # mass_number
        self.mass_number = QLineEdit("")
        self.mass_number.setPlaceholderText("e.g. 238")
        self.mass_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Mass number*"), self.mass_number)

        # proton_number
        self.proton_number = QLineEdit("")
        self.proton_number.setPlaceholderText("(optional)")
        self.proton_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Proton number (Z)"), self.proton_number)

        # neutron_number
        self.neutron_number = QLineEdit("")
        self.neutron_number.setPlaceholderText("(optional)")
        self.neutron_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Neutron number (N)"), self.neutron_number)

        # reference
        self.reference = QLineEdit("")
        self.reference.setPlaceholderText("(optional)")
        self.reference.setFixedWidth(100)
        form_layout1.addRow(QLabel("Data reference"), self.reference)

        # stable
        self.stable = QCheckBox()
        self.stable.setChecked(True)
        form_layout1.addRow(QLabel("Stable isotope?"), self.stable)
        self.stable.stateChanged.connect(self.toggle_decay_field)

        field_layout.addLayout(form_layout1)
        field_layout.addStretch()
        self.layout.addLayout(field_layout, 0, 0)


    def _create_decay_field(self):
        """  """
        self.decay_field_list = []
        self.decay_field_widget = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("Isotope decay"), alignment=Qt.AlignCenter)

        # Half life
        form_layout2 = QFormLayout()
        half_life_label = QLabel("Half life")
        half_life_label.setFixedWidth(135)
        self.half_life = QLineEdit("")
        self.half_life.setPlaceholderText("in seconds")
        self.half_life.setFixedWidth(100)
        form_layout2.addRow(half_life_label, self.half_life)
        layout2.addLayout(form_layout2)

        # Generate field for decays
        for i in range(0,3):
            layout2.addWidget(QLabel(f"Decay mode {i+1}"), alignment=Qt.AlignCenter)
            decays_layout = QFormLayout()

            # decay_type
            decay_label = QLabel("Decay type")
            decay_label.setFixedWidth(135)
            decay_type = QComboBox()
            decay_type.addItems(["", "alpha", "beta_minus", "gamma"])
            decay_type.setEditable(False)
            decay_type.setInsertPolicy(QComboBox.InsertAlphabetically)
            decay_type.setFixedWidth(100)
            decays_layout.addRow(decay_label, decay_type)

            # product
            product = QLineEdit("")
            product.setPlaceholderText("e.g. U-238")
            product.setFixedWidth(100)
            decays_layout.addRow(QLabel("Product"), product)

            # probability
            probability = QLineEdit("")
            probability.setPlaceholderText("e.g.: 0.9845")
            probability.setFixedWidth(100)
            decays_layout.addRow(QLabel("Probability"), probability)

            # released_energy
            released_energy = QLineEdit("")
            released_energy.setPlaceholderText("in MeV")
            released_energy.setFixedWidth(100)
            decays_layout.addRow(QLabel("Released energy"), released_energy)

            self.decay_field_list.append(decays_layout)
            layout2.addLayout(decays_layout)

        self.decay_field_widget.setEnabled(False)
        self.decay_field_widget.setLayout(layout2)
        self.layout.addWidget(self.decay_field_widget, 0, 1)


    def _create_buttons(self):
        """  """
        # Feedback widget
        self.status_text = QLabel('')
        self.status_text.setStyleSheet("color: red")
        self.layout.addWidget(self.status_text, 1,0)

        # Buttons
        button_box = QHBoxLayout()
        button_box.addStretch()
        button_accept = QPushButton("OK")
        button_accept.clicked.connect(self.accept_input)
        button_close = QPushButton("Cancel")
        button_close.clicked.connect(self.close_window)
        button_box.addWidget(button_accept)
        button_box.addWidget(button_close)
        self.layout.addLayout(button_box, 1, 1)


    # pylint: disable = missing-function-docstring
    def toggle_decay_field(self):
        self.decay_field_widget.setEnabled(not self.stable.isChecked())


    def add_default_values(self, defaults):
        """ Fills fields with default values. """
        short_id = defaults.get("short_id", "")
        self.setWindowTitle(f"Edit isotope - {short_id}")

        # Set values
        self.isotope_name.setText(defaults.get("name", ""))
        self.isotope_symbol.setText(defaults.get("symbol", ""))
        self.mass_number.setText(str(defaults.get("mass_number", "")))
        self.proton_number.setText(str(defaults.get("proton_number", "")))
        self.neutron_number.setText(str(defaults.get("neutron_number", "")))
        self.reference.setText(defaults.get("reference", ""))

        if defaults["half_life"] is not None:
            self.stable.setChecked(False)
            self.half_life.setText(str(defaults["half_life"]))

            step = 0
            for isotope, decay in defaults["decays"].items():
                decay_field = self.decay_field_list[step]
                decay_field.itemAt(1).widget().setCurrentText(isotope)
                decay_field.itemAt(3).widget().setText(decay.get("product", ""))
                decay_field.itemAt(5).widget().setText(str(decay.get("probability", "")))
                decay_field.itemAt(7).widget().setText(str(decay.get("released_energy", "")))
                step += 1


    def accept_input(self):
        """ Collects the given inputs, and accepts them if all valid. """
        IVC = InputValidatorBaseClass()
        self.status_text.setText("")

        # Read inputs
        try:
            name = IVC.sval(self.isotope_name.text())
            symbol = IVC.sval(self.isotope_symbol.text())
            mass_number = IVC.ival(self.mass_number.text())

            # Check mandatory params
            if name is None:
                self.status_text.setText("Isotope name is a mandatory parameter!")
                return
            if symbol is None:
                self.status_text.setText("Symbol is a mandatory parameter!")
                return
            if mass_number is None:
                self.status_text.setText("Mass number is a mandatory parameter!")
                return

            # Fill params into a class
            new_isotope = IsotopeEntry(name, symbol, mass_number)
            new_isotope.proton_number = IVC.ival(self.proton_number.text())
            new_isotope.neutron_number = IVC.ival(self.neutron_number.text())
            new_isotope.reference = IVC.sval(self.reference.text())

            if not self.stable.isChecked():
                new_isotope.half_life = IVC.fval(self.half_life.text())
                new_isotope.decays = {}

                for field_layout in self.decay_field_list:
                    decay_type = IVC.sval(field_layout.itemAt(1).widget().currentText())
                    if decay_type != "":
                        product = IVC.sval(field_layout.itemAt(3).widget().text())
                        probability = IVC.fval(field_layout.itemAt(5).widget().text(), default=1)
                        released_energy = IVC.fval(field_layout.itemAt(7).widget().text(), default=None)
                        new_isotope.decays.update(new_isotope.create_decay(decay_type, product,
                        probability, released_energy))

        except InputError as iee:
            self.status_text.setText(iee)
            return

        # Accept settings
        l.info(f"New isotope entry created: {new_isotope.short_id}!")
        self.results = new_isotope.dump() # Set results only when 'OK' is pressed!
        self.close_window()


    # pylint: disable = missing-function-docstring
    def close_window(self):
        self.close()


# Include guard
if __name__ == '__main__':
    pass
