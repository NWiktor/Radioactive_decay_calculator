# -*- coding: utf-8 -*-#
# !/usr/bin/python3
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
# import webbrowser

from fpdf import FPDF
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
# pylint: disable = no-name-in-module, unused-import
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QDesktopWidget,
                             QMessageBox, QDockWidget)
# from PyQt5.QtGui import (QFont, QPainter, QBrush, QColor, QFontMetrics)
from PyQt5.QtCore import Qt

from logger import MAIN_LOGGER as l
import modules.json_handler as jdbh
from gui.simulation_widget import SimulationWidget
from gui.create_isotope_window import CreateIsotopeWindow, ChooseIsotopeWindow


# Class and function definitions
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self, idbh):
        super().__init__(parent=None)

        # Load isotope db.
        self._idbh = idbh
        self.isotope_database = self._idbh.load()

        # Create GUI
        self.setWindowTitle(
                f"Radioactive Decay Calculator App - {date.today()}"
        )
        self._create_simulation_view()  # Create (dock) widget
        self._create_menubar()  # Create menu bar
        self._create_plotview()  # Create Mathplotlib (central) view
        self._create_status_bar()  # Create status bar
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
        database_menu = menu_bar.addMenu('Database')
        export_menu = menu_bar.addMenu('Export')
        settings_menu = menu_bar.addMenu('Settings')
        help_menu = menu_bar.addMenu('Help')

        self.start_action = QAction(
                'Start', self, triggered=self.start_calculation,
                shortcut="Ctrl+S"
        )
        self.close_action = QAction(
                'Close', self, triggered=self.close_window, shortcut="Ctrl+X"
        )
        self.show_simulation_view_action = (
            self.simulation_view.toggleViewAction())
        self.clear_plot_action = QAction(
                'Clear plot', self, triggered=self._clear_plotview
        )
        self.add_entry_action = QAction(
                'Add isotope', self, triggered=self.add_entry, shortcut="Ctrl+A"
        )
        self.edit_entry_action = QAction(
                'Edit isotope', self, triggered=self.edit_entry,
                shortcut="Ctrl+E"
        )
        self.settings_action = QAction(
                'Settings', self, triggered=self.open_settings
        )
        self.report_bug_action = QAction(
                'Report bug', self, triggered=self.report_bug
        )
        self.open_sharepoint_action = QAction(
                'C3D Sharepoint', self, triggered=self.open_sharepoint
        )
        self.visit_website_action = QAction(
                'C3D Website', self, triggered=self.open_company_webpage
        )
        self.about_action = QAction('About', self, triggered=self.about)

        file_menu.addAction(self.start_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_action)
        view_menu.addAction(self.show_simulation_view_action)
        view_menu.addAction(self.clear_plot_action)
        database_menu.addAction(self.add_entry_action)
        database_menu.addAction(self.edit_entry_action)
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
        self.sim_widget = SimulationWidget(self.isotope_database)
        self.simulation_view.setWidget(self.sim_widget)

    def _create_plotview(self):
        self.graph = MplCanvas(self, width=5, height=4, dpi=100)
        self.graph.axes.set_title("Radioactive decay")
        self.graph.axes.set_xlabel("Time [s]")
        self.graph.axes.set_ylabel("Mass [kg]")
        self.graph.axes.set_xlim(0, None)
        self.graph.axes.set_ylim(0, None)
        self.graph.axes.grid()
        self.setCentralWidget(self.graph)

    def _clear_plotview(self):
        self.graph.axes.cla()  # Clear existing curves
        self.graph.axes.set_title("Radioactive decay")
        self.graph.axes.set_xlabel("Time [s]")
        self.graph.axes.set_ylabel("Mass [kg]")
        self.graph.axes.set_xlim(0, None)
        self.graph.axes.set_ylim(0, None)
        self.graph.axes.grid()
        self.graph.draw()
        self.graph.flush_events()

    def edit_entry(self):
        """  """
        while True:
            choose_isotope_w = ChooseIsotopeWindow(self.isotope_database.keys())
            choose_isotope_w.exec_()

            if choose_isotope_w.results is not None:
                iid = choose_isotope_w.results
                self.add_entry(self.isotope_database[iid])
            else:
                break

    def add_entry(self, default_data=None):
        """  """
        # NOTE: When called by QAction, argument value is 'False'
        if default_data is False:
            default_data = None
        create_new_isotope_w = CreateIsotopeWindow(default_data)
        create_new_isotope_w.exec_()

        # Process results
        if create_new_isotope_w.results is not None:
            iid = create_new_isotope_w.results["short_id"]
            self.isotope_database.update({iid: create_new_isotope_w.results})
            self.save_database()

        else:
            l.info("Add entry aborted by user")

    def decay_isotope(self, isotope, original_mass, time):
        """  """
        data = self.isotope_database[isotope].get("decays", None)
        half_life = self.isotope_database[isotope].get("half_life", None)
        products = []

        # Stable isotope
        if data is None:
            products.append([isotope, original_mass])

        # Radioactive isotope
        else:
            # Calculate remaining mass of original isotope
            new_mass = original_mass * (2 ** (- (time / half_life)))
            products.append([isotope, new_mass])

            # Iterate over every decay type:
            for decay in data.values():
                # Calculate mass by the
                # mass difference multiplied by the probability factor
                products.append(
                        [decay["product"],
                         (original_mass-new_mass) * decay["probability"]]
                )

        return products

    def convert_time_unit(self, time_interval, time_unit):
        """  """
        if time_unit == "min":
            time_interval = time_interval / 60

        if time_unit == "h":
            time_interval = time_interval / 3600

        if time_unit == "d":
            time_interval = time_interval / 86400

        if time_unit == "a":
            time_interval = time_interval / 31556926

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

        # Generate plot:
        self.graph.axes.cla()  # Clear existing curves

        # Generate new data plots
        for isotope, value in data.items():
            self.graph.axes.plot(
                    value["time"], value["mass"], label=f"{isotope}"
            )

        # Set axis parameters
        self.graph.axes.set_title("Radioactive decay")
        self.graph.axes.set_xlabel(f"Time [{time_unit}]")
        self.graph.axes.set_ylabel("Mass [kg]")
        self.graph.axes.set_xlim(0, None)
        self.graph.axes.set_ylim(0, None)
        self.graph.axes.grid()
        self.graph.axes.legend()
        self.graph.draw()
        self.graph.flush_events()

    def start_calculation(self):
        """  """
        init_mass, time_interval, step = (
            self.sim_widget.get_simulation_parameters())
        init_mass = [init_mass]  # list of dictionaries
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
        about_w.setInformativeText(f"Program ver.:\t {SOFTWARE_VERSION}\n"
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

    def save_database(self):
        self._idbh.dump(self.isotope_database)

    def close_window(self):
        self.save_database()
        self.close()
        l.info("Main window terminated!")


# Include guard
if __name__ == '__main__':
    # Init JSON handlers:
    IDBH = jdbh.JsonDbHandler("database/isotope_database.json")
    CDBH = jdbh.JsonDbHandler("database/configuration_settings.json")

    # Load config. db.
    config = CDBH.load()  # This is hardcoded
    # Software related data
    SOFTWARE_VERSION = (
            str(config["program_version_major"]) + "."
            + str(config["program_version_minor"]) + "."
            + str(config["program_version_patch"]) + "."
            + str(config["program_build"])
    )
    RELEASE_DATE = config["release_date"]
    l.info("%s-%s", SOFTWARE_VERSION, RELEASE_DATE)

    # Start main application
    app = QApplication([])
    app.setStyle('Fusion')
    main = MainWindow(IDBH)
    main.show()
    l.info("Main window open")
    # main.center()
    app.exec()
    l.info("Program exit!")
    sys.exit()
