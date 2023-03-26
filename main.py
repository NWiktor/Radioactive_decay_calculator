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

import uuid
import sys
import os
from fpdf import FPDF
import math as m
import matplotlib.pyplot as plt
# import numpy as np

# pylint: disable = no-name-in-module
# Third party imports
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QMainWindow,
QAction, QGridLayout, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton,
QMessageBox, QFormLayout, QLineEdit, QInputDialog,
QTreeWidgetItem, QTreeWidget, QSizePolicy, QLabel, QSpacerItem)
from PyQt5.QtGui import (QFont, QPainter, QBrush, QColor, QFontMetrics)
from PyQt5.QtCore import (Qt, QRect, QSize)

# Global variables
RELEASE_DATE = "2023-03-25"

# class Isotope:

# 	def __init__(name, proton_number, neutron_number):
# 		self.name = f"{name}-{proton_number}"
# 		self.proton_number = proton_number
# 		self.neutron_number = neutron_number
# 		self.decay_type = None
# 		self.half_life = None


# class Decay:

# 	def __init__():
# 		pass


database = {
	"Ra-225": {"half_life": 1_287_360, "product": "Ac-238"},
	"Ac-238": {"half_life": 860_000, "product": "Fr-221"},
	"Fr-221": {"half_life": 288, "product": "At-217"}, #multiple product (!)
	"At-217": {"half_life": 0.032, "product": "Bi-213"},
	"Bi-213": {"half_life": 2_790, "product": "Po-213"},
	"Po-213": {"half_life": 3.72e-6, "product": "Pb-209"},
	"Pb-209": {"half_life": 11_700, "product": "Bi-209"},
	"Bi-209": {"half_life": 59_918_400e+19, "product": "Ti-205"},
	"Ti-205": {"half_life": None, "product": None}
	}


def decay(isotope, original_mass, time):

	data = database[isotope]
	products = []

	if data["half_life"] == None: #Stable isotope
		products.append([isotope, original_mass])
	
	else:
		new_mass = original_mass * (2 ** (- (time / data["half_life"]) ) )
		products.append([isotope, new_mass])
		products.append([data["product"], (original_mass-new_mass)])
	
	return products


def create_plot_data(mass_distribution, time_step):

	i = 0
	time = []
	data = {}

	for d in mass_distribution:

		for element, mass in d.items():
			if element not in data.keys():
				data[element] = {}
				data[element]["time"] = []
				data[element]["mass"] = []
			else:
				data[element]["time"].append(i*time_step)
				data[element]["mass"].append(mass)

		i += 1

	for element in data.keys():
		plt.plot(data[element]["time"], data[element]["mass"], label=f"{element}")

	plt.title("Radiactive decay")
	plt.legend()
	plt.show()


def main():
	#list of dictionaries
	init_mass = [
	{"Ra-225": 10, "Ac-238": 10} # kg
	]

	time_step = 100 # second per day: 24*60*60
	i = 0
	step = 500

	print("Starting calculation...")
	while (i <= step):

		print(f"Step {i}")
		new_mass = {}
		for isotope, mass in init_mass[-1].items():
			
			# Calculate decay
			products = decay(isotope, mass, time_step)
			
			for product in products:
				if product[0] not in new_mass.keys():
					new_mass[f"{product[0]}"] = product[1]
				else:
					new_mass[f"{product[0]}"] += product[1]

		init_mass.append(new_mass)
		i += 1

	create_plot_data(init_mass, time_step)


### Include guard
if __name__ == '__main__':
	main()
    # app = QApplication([])
    # app.setStyle('Fusion')
    # main = MainWindow()
    # main.show()
    # main.center()
    # app.exec()
    # sys.exit()
