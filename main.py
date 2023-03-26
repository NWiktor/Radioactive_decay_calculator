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
import webbrowser

from fpdf import FPDF
import matplotlib.pyplot as plt
from logger import MAIN_LOGGER as l
import modules.json_handler as jdbh

# pylint: disable = no-name-in-module, unused-import
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QMainWindow,
QAction, QGridLayout, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton,
QMessageBox, QFormLayout, QLineEdit, QInputDialog,
QTreeWidgetItem, QTreeWidget, QSizePolicy, QLabel, QSpacerItem)
from PyQt5.QtGui import (QFont, QPainter, QBrush, QColor, QFontMetrics)
from PyQt5.QtCore import (Qt, QRect, QSize)


def decay_isotope(isotope, original_mass, time):
    """  """
    data = database[isotope].get("decays", None)
    half_life = database[isotope].get("half_life", None)
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


def convert_time_unit(time_step, time_unit):
    """  """
    if time_unit == "min":
        time_step = time_step/60

    if time_unit == "h":
        time_step = time_step/3600

    if time_unit == "d":
        time_step = time_step/86400

    if time_unit == "a":
        time_step = time_step/31556926

    return time_step


def create_plot_data(mass_distribution, time_step, time_unit="s"):
    """  """

    i = 0
    data = {}
    time_step = convert_time_unit(time_step, time_unit)

    # Iterate over a specific mass-distribution in a given timestep
    for mix in mass_distribution:

        for isotope, mass in mix.items():
            if isotope not in data:
                data[isotope] = {"time": [], "mass": []}
            else:
                data[isotope]["time"].append(i*time_step)
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


def main_calc():
    """  """
    # list of dictionaries
    init_mass = [
    {"Ra-225": 10}#, "Ac-225": 10} # kg
    ]

    time_step = 500 # second per day: 24*60*60
    i = 0
    step = 15000

    l.info("Starting decay calculation...")
    while i <= step:

        new_mass = {}
        for isotope, mass in init_mass[-1].items():

            # Calculate decay
            products = decay_isotope(isotope, mass, time_step)

            for product in products:
                if product[0] not in new_mass:
                    new_mass[f"{product[0]}"] = product[1]
                else:
                    new_mass[f"{product[0]}"] += product[1]

        init_mass.append(new_mass)
        i += 1

    create_plot_data(init_mass, time_step, time_unit="d")


# Class and function definitions
class MainWindow(QMainWindow):
    def __init__(self, idbh):
        super().__init__(parent=None)

        # Create User object
        self._idbh = idbh

        # Create GUI
        self.setWindowTitle(f"Radioactive Decay Calculator App - {date.today()}")
        self._create_menubar() # Create menu bar
        # self._create_calendar_view() # Create calendar (central) view
        # self._update_calendar_view()
        self._create_status_bar() # Create status bar
        # self.showMaximized()


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
        settings_menu.addAction(self.settings_action)
        help_menu.addAction(self.report_bug_action)
        help_menu.addAction(self.open_sharepoint_action)
        help_menu.addAction(self.visit_website_action)
        help_menu.addAction(self.about_action)


    def _create_status_bar(self):
        self.statusbar = self.statusBar()


    def start_calculation(self):
        main_calc()


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

    # Load isotope db.
    database = IDBH.load()

    app = QApplication([])
    app.setStyle('Fusion')
    main = MainWindow(database)
    main.show()
    main.center()
    app.exec()
    l.info("Main window open")
    IDBH.dump(database)
    l.info("Program exit!")
    sys.exit()
