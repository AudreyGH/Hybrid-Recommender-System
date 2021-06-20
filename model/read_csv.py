import csv
import os
import webbrowser
from pathlib import Path


# Classes that import data from CSV files
# The parts data are read and stored as a nested list


# Case Class
# Read case data from CSV file
# Filter data according to user input
class Case:
    filtered_cases = []

    def __init__(self):
        self.case = []

    def load_case(self, selection):
        layout = ''
        row = 0
        self.filtered_cases.clear()
        self.case.clear()

        # Load data from CSV
        a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'case.csv'))
        p = Path(a).as_posix()
        with open(p) as cases:
            data = csv.reader(cases)
            for case in data:
                self.case.append(case)

        if selection == 1:
            layout = '60%'
        if selection == 2:
            layout = '65%'
        if selection == 3:
            layout = '75%'

        for column in self.case:
            if layout in column[0]:
                self.filtered_cases.append(self.case[row])
            row += 1

    def get_filtered(self):
        return self.filtered_cases


# Keycap Class
# Read keycap data from CSV file
class Keycap:
    filtered_keycaps = []

    def __init__(self):
        self.keycap = []

    def load_keycap(self):
        self.keycap.clear()

        # Load data from CSV
        a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'keycap.csv'))
        p = Path(a).as_posix()
        with open(p) as keycaps:
            data = csv.reader(keycaps)
            next(data)

            for keycap in data:
                self.keycap.append(keycap)

        return self.keycap


# PCB Class
# Read PCB data from CSV file
# Filter data according to user input
class Pcb:
    pcb_df = []

    def __init__(self):
        self.pcb = []

    def load_board(self):
        self.pcb.clear()

        # Load data from CSV
        a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'board.csv'))
        p = Path(a).as_posix()
        with open(p) as boards:
            data = csv.reader(boards)

            for board in data:
                self.pcb.append(board)

    def get_selected(self, selection):
        layout = ''
        temp = []
        row = 0
        self.load_board()

        if selection == 1:
            layout = '60%'
        if selection == 2:
            layout = '65%'
        if selection == 3:
            layout = '75%'

        for column in self.pcb:
            if layout in column[0]:
                temp.append(self.pcb[row])
            row += 1
        return temp

    def get_pcb_df(self):
        return self.pcb_df


# Plate Class
# Read data from CSV file
# Filter data according to user input
class Plate:
    filtered_plates = []

    def __init__(self):
        self.plate = []

    def load_plate(self, selection):
        layout = ''
        row = 0
        self.filtered_plates.clear()
        self.plate.clear()

        # Load data from CSV
        a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'plate.csv'))
        p = Path(a).as_posix()
        with open(p) as plates:
            data = csv.reader(plates)

            for plate in data:
                self.plate.append(plate)

        if selection == 1:
            layout = '60%'
        if selection == 2:
            layout = '65%'
        if selection == 3:
            layout = '75%'

        for column in self.plate:
            if layout in column[0]:
                self.filtered_plates.append(self.plate[row])
            row += 1

    def get_filtered(self):
        return self.filtered_plates


# Switch class
# Read data from CSV file
class Switch:
    filtered_switches = []

    def __init__(self):
        self.switch = []

    def load_switch(self):
        self.switch.clear()

        # Load data from CSV
        a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'switch.csv'))
        p = Path(a).as_posix()
        with open(p) as switches:
            data = csv.reader(switches)
            next(data)

            for switch in data:
                self.switch.append(switch)

        return self.switch


def open_csv(file):
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), file))
    print(path)
    webbrowser.open(os.path.realpath(path))
