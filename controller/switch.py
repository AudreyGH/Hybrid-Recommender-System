from PyQt5 import QtWidgets
from controller.build import BuildApp, add_part, clear_parts, search_parts, exit_app
from controller.keycap import KeycapApp
from controller.stats import MainStatsWidget
from model.collaborative_filter import switch_factorization
from model.message import add_limit, confirm_restart, is_selected, open_file
from model.read_csv import Switch
from model.read_csv import open_csv
from view import switch


# The switch window controller
# The table is populated with switch data
class SwitchApp(switch.Ui_Form, QtWidgets.QWidget):

    def __init__(self):
        super(SwitchApp, self).__init__()
        self.setupUi(self)
        self.keycap = KeycapApp()
        self.build = BuildApp()
        self.stats = MainStatsWidget()
        self.pushButton.clicked.connect(self.add_part)
        self.pushButton_2.clicked.connect(self.show_build)
        self.pushButton_3.clicked.connect(self.start_over)
        self.pushButton_4.clicked.connect(exit_app)
        self.pushButton_5.clicked.connect(self.show_stats)
        self.pushButton_6.clicked.connect(self.open_file)

    # Add selected part to build table
    def add_part(self):
        temp = []
        name = ''
        selected_switch = []

        # If a row is selected, clear selection from other table
        if self.tableWidget.selectionModel().hasSelection():
            self.tableWidget_2.clearSelection()
            selected_switch = self.tableWidget.selectedItems()
        if self.tableWidget_2.selectionModel().hasSelection():
            self.tableWidget.clearSelection()
            selected_switch = self.tableWidget_2.selectedItems()

        # Alert user if a row has not been selected from either tables
        if not self.tableWidget.selectionModel().hasSelection() and not self.tableWidget_2.selectionModel().hasSelection():
            is_selected()
            return

        # Add switch if no switch exist in the build table
        if not search_parts('Switch'):
            for index, i in enumerate(selected_switch):
                if index == 0:
                    temp.append('N/A')
                if index <= 3:
                    name += i.text() + ' '
                if index == 4:
                    temp.append(name)
                if index >= 4:
                    temp.append(i.text())
            add_part(temp)
        # Warning message if adding more than 1 item of the same type
        else:
            add_limit()
            return
        self.close()
        self.keycap.load_table()
        self.keycap.load_table2()
        self.keycap.showMaximized()

    # Show build window
    def show_build(self):
        self.build.load_table()
        self.build.showMaximized()

    # Show Data Visualization Window
    def show_stats(self):
        self.stats.plot_svd()
        self.stats.showMaximized()

    # Close the switch window and clear the build table
    def start_over(self):
        if confirm_restart():
            self.close()
            clear_parts()
        else:
            return

    # Open CSV file of current window
    def open_file(self):
        if open_file():
            self.close()
            open_csv('switch.csv')
            clear_parts()
        else:
            return

    # Populate switch table
    def load_table(self):
        switches = Switch().load_switch()
        row = 0
        self.tableWidget.setRowCount(len(switches))

        for i in switches:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i[5]))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(i[6]))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            row += 1
        self.tableWidget.clearSelection()

    # Populate switch recommendation table
    def load_table2(self):
        switches = switch_factorization()
        row = 0
        self.tableWidget_2.setRowCount(len(switches))

        for i in switches:
            self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(i[5]))
            self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(i[6]))
            self.tableWidget_2.resizeColumnsToContents()
            self.tableWidget_2.resizeRowsToContents()
            row += 1
        self.tableWidget_2.clearSelection()
