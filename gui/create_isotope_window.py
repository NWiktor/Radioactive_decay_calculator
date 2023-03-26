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
from datetime import date

# Third party imports
# pylint: disable = no-name-in-module
from PyQt5.QtWidgets import (
QDialog, QWidget,
QFormLayout,
QCheckBox,
QLineEdit,
QVBoxLayout,
QHBoxLayout,
QPushButton,
QComboBox,
QListWidget,
QDateEdit,
QLabel)
from PyQt5.QtCore import (Qt, QDateTime, QDate)

# Local application imports
from logger import MAIN_LOGGER as l

# Class and function definitions
class CreateIsotopeWindow(QDialog):
    """Project creation window for PyQt5.

    """
    # TODO: implement default data, to fill out the form == this class can be used for editing as well
    def __init__(self, default_data=None):
        super().__init__(parent=None)
        self.setWindowTitle("Create new isotope")
        self.default_data = default_data
        self.results = None

        # Initialize window
        self.layout = QVBoxLayout()
        self._create_fields()
        self._create_decay_field()
        self._create_buttons() # OK és Close gombok az ablak alján
        self.setLayout(self.layout)


    def _create_fields(self):
        """  """

        # name
        form_layout1 = QFormLayout()
        isotope_name_label = QLabel("Isotope name")
        isotope_name_label.setFixedWidth(135)
        self.isotope_name = QLineEdit("")
        self.isotope_name.setPlaceholderText("e.g. Uranium")
        self.isotope_name.setFixedWidth(100)
        form_layout1.addRow(isotope_name_label, self.isotope_name)

        # symbol
        self.symbol = QLineEdit("")
        self.symbol.setPlaceholderText("e.g. U")
        self.symbol.setFixedWidth(100)
        form_layout1.addRow(QLabel("Symbol*"), self.symbol)

        # mass_number
        self.mass_number = QLineEdit("")
        self.mass_number.setPlaceholderText("e.g. 238")
        self.mass_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Mass number*"), self.mass_number)

        # proton_number
        self.proton_number = QLineEdit("")
        self.proton_number.setPlaceholderText("(optional)")
        self.proton_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Proton number"), self.proton_number)

        # neutron_number
        self.neutron_number = QLineEdit("")
        self.neutron_number.setPlaceholderText("(optional)")
        self.neutron_number.setFixedWidth(100)
        form_layout1.addRow(QLabel("Neutron number"), self.neutron_number)

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
        self.layout.addLayout(form_layout1)


    def _create_decay_field(self):

        self.decay_field_widget = QWidget()
        layout2 = QVBoxLayout()

        # Half life
        form_layout2 = QFormLayout()
        half_life_label = QLabel("Half life")
        half_life_label.setFixedWidth(135)
        self.half_life = QLineEdit("")
        self.half_life.setPlaceholderText("in seconds")
        self.half_life.setFixedWidth(100)
        form_layout2.addRow(half_life_label, self.half_life)

        layout2.addLayout(form_layout2)
        layout2.addWidget(QLabel("Isotope decay modes"))

        # Generate field for decays        
        i = 2
        for i in range(0,2):
            decays_layout = QFormLayout()

            # decay_type
            decay_label = QLabel("Decay type")
            decay_label.setFixedWidth(135)
            self.decay_type = QLineEdit("")
            self.decay_type.setPlaceholderText("e.g. alpha")
            self.decay_type.setFixedWidth(100)
            decays_layout.addRow(decay_label, self.decay_type)

            # product
            self.product = QLineEdit("")
            self.product.setPlaceholderText("e.g. U-238")
            self.product.setFixedWidth(100)
            decays_layout.addRow(QLabel("Product"), self.product)

            # probability
            self.probability = QLineEdit("")
            self.probability.setPlaceholderText("e.g.: 0.9845")
            self.probability.setFixedWidth(100)
            decays_layout.addRow(QLabel("Probability"), self.probability)

            # released_energy
            self.released_energy = QLineEdit("")
            self.released_energy.setPlaceholderText("in MeV")
            self.released_energy.setFixedWidth(100)
            decays_layout.addRow(QLabel("Released energy"), self.released_energy)

            layout2.addLayout(decays_layout)
        
        self.decay_field_widget.setEnabled(False)
        self.decay_field_widget.setLayout(layout2)
        self.layout.addWidget(self.decay_field_widget)


    def _create_buttons(self):
        # Feedback widget
        self.status_text = QLabel('')
        self.status_text.setStyleSheet("color: red")
        self.layout.addWidget(self.status_text, alignment=Qt.AlignCenter)

        # Buttons
        button_box = QHBoxLayout()
        button_box.addStretch()
        button_accept = QPushButton("OK")
        button_accept.clicked.connect(self.accept_input)
        button_close = QPushButton("Cancel")
        button_close.clicked.connect(self.close_window)
        button_box.addWidget(button_accept)
        button_box.addWidget(button_close)
        self.layout.addLayout(button_box)


    def toggle_decay_field(self):
        self.decay_field_widget.setEnabled(not self.stable.isChecked())


    def accept_input(self):
        """Collects the given inputs, and accepts them if all valid.

        This function collects the inputs from the textboxes, removes leading
        and trailing whitespaces, and checks if all the required inputs are
        given. If not, displays warning and returns. If yes, and specified,
        validates the inputs by calling the validator function.

        :param event: Empty event to allow binding (default = None).

        """
        # self.status_text.setText("")
        # results = {}
        # project_name = self.project_name.text()

        # if project_name == "":
        #     self.status_text.setText("Project name is a mandatory parameter!")
        #     return

        # results["project_name"] = project_name.capitalize()
        # results["description"] = self.description.text()
        # results["start_date"] = self.start_date_edit.text()
        # results["end_date"] = self.end_date_edit.text()
        # # TODO: Implement this item
        # # results["sub_projects"] = self.parent_project_cbox.text()
        # results["public"] = self.public.isChecked()

        # items = []
        # for i in range(self.project_members_list_widget.count()):
        #     value = str(self.project_members_list_widget.item(i).text())
        #     items.append(value)

        # results["project_members"] = items

        # ### Accept settings
        # self.results = results # Csak az OK esetén adjuk vissza a beállításokat!

        # selected_parent_project = self.parent_project_cbox.currentText().strip()
        # if selected_parent_project != "":
        #     for i in self.projects:
        #         if i[0] == selected_parent_project:
        #             self.parent_project = i

        self.close_window()


    def close_window(self):
        self.close()


# Include guard
if __name__ == '__main__':
    pass
