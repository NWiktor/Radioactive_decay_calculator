# -*- coding: utf-8 -*-#
#!/usr/bin/python3
"""  GUI for radioactive decay calculation.

Libs
----
* PyQt5

Help
----

Info
----
Wetzl Viktor - 2023.03.25 - All rights reserved
"""
import sys
from datetime import date
from copy import deepcopy
import webbrowser

from fpdf import FPDF
import matplotlib.pyplot as plt
from logger import MAIN_LOGGER as l
import modules.json_handler as jdbh

# pylint: disable = no-name-in-module, unused-import
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QMainWindow,
QAction, QGridLayout, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton,
QMessageBox, QFormLayout, QLineEdit, QInputDialog, QDockWidget, QListWidget,
QTreeWidgetItem, QTreeWidget, QSizePolicy, QLabel, QSpacerItem, QComboBox)
from PyQt5.QtGui import (QFont, QPainter, QBrush, QColor, QFontMetrics)
from PyQt5.QtCore import (Qt, QRect, QSize)


# Class and function definitions
class MainWindow(QMainWindow):
    def __init__(self, IDBH):
        super().__init__(parent=None)

        # Load isotope db.
        self._idb = IDBH.load()

        # Create GUI
        self.setWindowTitle(f"Radioactive Decay Calculator App - {date.today()}")
        self._create_simulation_view() # Create (dock) widget
        self._create_menubar() # Create menu bar
        self._create_plotview() # Create Mathplotlib (central) view
        # self._update_calendar_view()
        self._create_status_bar() # Create status bar
        self.showMaximized()


    def center(self):
        """Position window to the center."""
        qt_rectangle = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(centerpoint)
        self.move(qt_rectangle.topLeft())


    def _create_menubar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        view_menu = menu_bar.addMenu('View')
        project_menu = menu_bar.addMenu('Project')
        export_menu = menu_bar.addMenu('Export')
        settings_menu = menu_bar.addMenu('Settings')
        help_menu = menu_bar.addMenu('Help')

        self.start_action = QAction('Start', self,
        triggered=self.start_calculation)
        self.close_action = QAction('Close', self,
        triggered=self.close_window, shortcut="Ctrl+E")
        #
        self.show_simulation_view_action = self.simulation_view.toggleViewAction()
        #
        self.settings_action = QAction('Settings', self,
        triggered=self.open_settings)
        #
        self.report_bug_action = QAction('Report bug', self,
        triggered=self.report_bug)
        self.open_sharepoint_action = QAction('C3D Sharepoint', self,
        triggered=self.open_sharepoint)
        self.visit_website_action = QAction('C3D Website', self,
        triggered=self.open_company_webpage)
        self.about_action = QAction('About', self, triggered=self.about)

        file_menu.addAction(self.start_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_action)
        view_menu.addAction(self.show_simulation_view_action)
        settings_menu.addAction(self.settings_action)
        help_menu.addAction(self.report_bug_action)
        help_menu.addAction(self.open_sharepoint_action)
        help_menu.addAction(self.visit_website_action)
        help_menu.addAction(self.about_action)


    def _create_status_bar(self):
        self.statusbar = self.statusBar()


    def _create_simulation_view(self):
        self.simulation_view = QDockWidget('Simulation parameters', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.simulation_view)

        # self.isotopes_list = {}
        self.isotopes_list = {"Ra-225": 10, "Ac-225": 10}

        # Add Fields
        layout = QVBoxLayout()
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
        layout.addLayout(form_layout)

        # Add Buttons
        button_box = QHBoxLayout()
        button_accept = QPushButton("Add")
        button_accept.clicked.connect(self.accept_input)
        button_box.addWidget(button_accept)
        button_box.addStretch()
        layout.addLayout(button_box)

        # Add Listview
        layout.addWidget(QLabel("Added isotopes"))
        self.shown_iso_list_widget = QListWidget()
        for name, mass in self.isotopes_list.items():
            self.shown_iso_list_widget.addItem(f"{name} - {mass} [kg]")
        layout.addWidget(self.shown_iso_list_widget)

        layout_widget = QWidget(self)
        layout_widget.setLayout(layout)
        self.simulation_view.setWidget(layout_widget)


    def accept_input(self):
        name = self.isotope_name_cbox.currentText().strip()
        mass = self.isotope_mass.text().strip()
        self.isotopes_list.update({name: float(mass)})

        self.shown_iso_list_widget.clear()

        for name, mass in self.isotopes_list.items():
            self.shown_iso_list_widget.addItem(f"{name} - {mass} [kg]")
        print(self.isotopes_list)


    def _create_plotview(self):
        print("Plotview")


    def decay_isotope(self, isotope, original_mass, time):
        """  """
        data = self._idb[isotope].get("decays", None)
        half_life = self._idb[isotope].get("half_life", None)
        products = []

        # Stable isotope
        if data is None:
            products.append([isotope, original_mass])

        # Radioactive isotope
        else:
            # Calculate remaining mass of original isotope
            new_mass = original_mass * (2 ** (- (time / half_life) ) )
            products.append([isotope, new_mass])

            # Iterate over every decay type:
            for decay in data.values():
                # Calculate mass by the
                # mass difference multiplied by the probability factor
                products.append([decay["product"], (original_mass-new_mass)*decay["probability"]])

        return products


    def convert_time_unit(self, time_interval, time_unit):
        """  """
        if time_unit == "min":
            time_interval = time_interval/60

        if time_unit == "h":
            time_interval = time_interval/3600

        if time_unit == "d":
            time_interval = time_interval/86400

        if time_unit == "a":
            time_interval = time_interval/31556926

        return time_interval


    def create_plot_data(self, mass_distribution, time_interval, time_unit="s"):
        """  """

        i = 0
        data = {}
        time_interval = self.convert_time_unit(time_interval, time_unit)

        # Iterate over a specific mass-distribution in a given timestep
        for mix in mass_distribution:

            for isotope, mass in mix.items():
                if isotope not in data:
                    data[isotope] = {"time": [], "mass": []}
                else:
                    data[isotope]["time"].append(i*time_interval)
                    data[isotope]["mass"].append(mass)

            i += 1

        fig, ax = plt.subplots(1)

        for isotope, value in data.items():
            ax.plot(value["time"], value["mass"], label=f"{isotope}")

        ax.set_title("Radioactive decay")
        ax.set_xlabel(f"Time [{time_unit}]")
        ax.set_ylabel("Mass [kg]")
        ax.set_xlim(0, None)
        ax.set_ylim(0, None)
        ax.grid()
        ax.legend()
        fig.canvas.manager.set_window_title('Radioactive decay results')
        plt.show()


    def start_calculation(self):
        """  """
        init_mass = [deepcopy(self.isotopes_list)] # list of dictionaries
        time_interval = int(self.interval.text().strip()) # second per day: 24*60*60
        step = int(self.step_number.text().strip())
        
        i = 0
        l.info("Starting decay calculation...")
        while i <= step:

            new_mass = {}
            for isotope, mass in init_mass[-1].items():

                # Calculate decay
                products = self.decay_isotope(isotope, mass, time_interval)

                for product in products:
                    if product[0] not in new_mass:
                        new_mass[f"{product[0]}"] = product[1]
                    else:
                        new_mass[f"{product[0]}"] += product[1]

            init_mass.append(new_mass)
            i += 1

        self.create_plot_data(init_mass, time_interval, time_unit="d")


    def open_settings(self):
        print("Settings_open")


    def report_bug(self):
        print("Report bug")


    def about(self):
        """Prints program version data."""
        about_w = QMessageBox()
        about_w.setWindowTitle("About")
        about_w.setIcon(QMessageBox.Information)
        about_w.setText("Radioactive Decay Calculator App")
        about_w.setInformativeText(
        f"Program ver.:\t {SOFTWARE_VERSION}\n"
        + f"Release date:\t {RELEASE_DATE}\n"
        + "Created by:\t Wetzl Viktor"
        )
        about_w.exec_()


    def open_sharepoint(self):
        """ Opens C3D sharepoint webpage in the default browser. """
        # webbrowser.open('https://c3dhu.sharepoint.com/')


    def open_company_webpage(self):
        """ Opens C3D webpage in the default browser. """
        # webbrowser.open('https://c3d.hu/')


    def close_window(self):
        self.close()
        l.info("Main window terminated!")


### Include guard
if __name__ == '__main__':
    # Init JSON handlers:
    IDBH = jdbh.JsonDbHandler("database/isotope_database.json") # Isotope db handler
    CDBH = jdbh.JsonDbHandler("database/configuration_settings.json") # Config db handler

    # Load config. db.
    config = CDBH.load() # This is hardcoded
    # Software related data
    SOFTWARE_VERSION = (str(config["program_version_major"]) + "."
    + str(config["program_version_minor"]) + "."
    + str(config["program_version_patch"]) + "."
    + str(config["program_build"]))
    RELEASE_DATE = config["release_date"]
    l.info("%s-%s", SOFTWARE_VERSION, RELEASE_DATE)

    # Start main application
    app = QApplication([])
    app.setStyle('Fusion')
    main = MainWindow(IDBH)
    main.show()
    l.info("Main window open")
    main.center()
    app.exec()
    l.info("Program exit!")
    sys.exit()
