import pandas as pd
from PyQt5 import QtWidgets
from view import main_menu, pcb
from controller import pcb
from model.read_csv import Case, Keycap, Pcb, Plate, Switch
from controller.build import clear_parts, exit_app
from model.message import close_window
from model.content_filter import sort_pcb
import sys


# The main window controller
# The user can click one of three pushButtons to move on to the next window.
# The user will choose between 60%, 65%, and 75% keyboard layouts.
# Initializes the layout for all other parts to guarantee compatibility
# Layout compatibility only matters to PCB, plate, and case
class MyQtApp(main_menu.Ui_MainWindow, QtWidgets.QMainWindow):
    pcb_df = []

    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.pcb = pcb.PcbApp()
        self.center()
        self.showMaximized()
        self.pushButton.clicked.connect(self.clicked)
        self.pushButton_2.clicked.connect(self.clicked2)
        self.pushButton_3.clicked.connect(self.clicked3)
        self.pushButton_4.clicked.connect(exit_app)

    # Centers widget on the user's desktop
    def center(self):
        fr = self.frameGeometry()
        cn = QtWidgets.QDesktopWidget().availableGeometry().center()
        fr.moveCenter(cn)
        self.move(fr.topLeft())

    # Populate and show the 60% PCB window/widget
    # Clears the build table before populating
    def clicked(self):
        clear_parts()
        Plate().load_plate(1)
        Case().load_case(1)
        self.pcb.load_table(Pcb().get_selected(1))
        self.pcb_df = pd.DataFrame(Pcb().get_selected(1))
        self.pcb.load_table2(sort_pcb(self.pcb_df))
        self.pcb.showMaximized()

    # Populate and show the 65% PCB window/widget
    # Clear the build table before populating
    def clicked2(self):
        clear_parts()
        Plate().load_plate(2)
        Case().load_case(2)
        self.pcb.load_table(Pcb().get_selected(2))
        self.pcb_df = pd.DataFrame(Pcb().get_selected(2))
        self.pcb.load_table2(sort_pcb(self.pcb_df))
        self.pcb.showMaximized()

    # Populate and show 75% PCB window/widget
    # Clears the build table before populating
    def clicked3(self):
        clear_parts()
        Plate().load_plate(3)
        Case().load_case(3)
        self.pcb.load_table(Pcb().get_selected(3))
        self.pcb_df = pd.DataFrame(Pcb().get_selected(3))
        self.pcb.load_table2(sort_pcb(self.pcb_df))
        self.pcb.showMaximized()

    # Detect when window is closed manually and ask the user to confirm
    def closeEvent(self, event):
        if close_window():
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MyQtApp()
    main.show()
    app.exec_()
