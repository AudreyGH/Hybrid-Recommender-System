from PyQt5 import QtWidgets
from controller.build import BuildApp, add_part, clear_parts, search_parts, exit_app
from controller.stats import MainStatsWidget
from model.collaborative_filter import keycap_factorization
from model.content_filter import similar_keycap
from model.message import add_limit, confirm_restart, is_selected, open_file
from model.read_csv import Keycap
from model.read_csv import open_csv
from view import keycap


# The keycap window controller
# The table is populated with keycap data
class KeycapApp(keycap.Ui_Form, QtWidgets.QWidget):

    def __init__(self):
        super(KeycapApp, self).__init__()
        self.setupUi(self)
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
        selected_keycap = []

        # If a row is selected, clear selection from other table
        if self.tableWidget.selectionModel().hasSelection():
            self.tableWidget_2.clearSelection()
            selected_keycap = self.tableWidget.selectedItems()
        if self.tableWidget_2.selectionModel().hasSelection():
            self.tableWidget.clearSelection()
            selected_keycap = self.tableWidget_2.selectedItems()

        # Alert user if a row has not been selected from either tables
        if not self.tableWidget.selectionModel().hasSelection() and not self.tableWidget_2.selectionModel().hasSelection():
            is_selected()
            return

        # Add keycaps if no keycaps exist in the build table
        if not search_parts('Keycap'):
            for index, i in enumerate(selected_keycap):
                if index == 0:
                    temp.append('N/A')
                if index >= 1:
                    name += i.text() + '/'
                if index == 3:
                    name += i.text()
                    temp.append(name)
                if index == 4:
                    continue
                if index >= 5:
                    temp.append(i.text())
            add_part(temp)
        # Warning message if adding more than 1 item of the same type
        else:
            add_limit()
            return
        self.close()
        self.build.load_table()
        self.build.showMaximized()

    # Show build window
    def show_build(self):
        self.build.load_table()
        self.build.showMaximized()

    # Show Data Visualization Window
    def show_stats(self):
        self.stats.plot_knn()
        self.stats.plot_tfidf()
        self.stats.plot_svd()
        self.stats.showMaximized()

    # Close the keycap window and clear the build table
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
            open_csv('keycap.csv')
            clear_parts()
        else:
            return

    # Populate keycap table
    def load_table(self):
        keycaps = Keycap().load_keycap()
        row = 0
        self.tableWidget.setRowCount(len(keycaps))

        for i in keycaps:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i[5]))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(i[6]))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(i[7]))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            row += 1
        self.tableWidget.clearSelection()

    # Populate keycap table
    def load_table2(self):
        keycaps = keycap_factorization(similar_keycap())
        row = 0
        self.tableWidget_2.setRowCount(len(keycaps))

        for i in keycaps:
            self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(i[5]))
            self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(i[6]))
            self.tableWidget_2.setItem(row, 7, QtWidgets.QTableWidgetItem(i[7]))
            self.tableWidget_2.resizeColumnsToContents()
            self.tableWidget_2.resizeRowsToContents()
            row += 1
        self.tableWidget_2.clearSelection()
