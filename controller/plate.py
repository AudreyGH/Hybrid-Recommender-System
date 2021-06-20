from PyQt5 import QtWidgets
from controller.build import BuildApp, add_part, clear_parts, search_parts, exit_app
from controller.case import CaseApp
from controller.stats import MainStatsWidget
from model.content_filter import similar_case
from model.message import add_limit, confirm_restart, is_selected, open_file
from model.read_csv import Plate
from model.read_csv import open_csv
from view import plate


# The plate window controller
# The table is populated with plate data
class PlateApp(plate.Ui_Form, QtWidgets.QWidget):

    def __init__(self):
        super(PlateApp, self).__init__()
        self.setupUi(self)
        self.case = CaseApp()
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
        selected_plate = []

        # If a row is selected, clear selection from other table
        if self.tableWidget.selectionModel().hasSelection():
            self.tableWidget_2.clearSelection()
            selected_plate = self.tableWidget.selectedItems()
        if self.tableWidget_2.selectionModel().hasSelection():
            self.tableWidget.clearSelection()
            selected_plate = self.tableWidget_2.selectedItems()

        # Alert user if a row has not been selected from either tables
        if not self.tableWidget.selectionModel().hasSelection() and not self.tableWidget_2.selectionModel().hasSelection():
            is_selected()
            return

        # Add plate if no plate exist in the build table
        if not search_parts('Plate'):
            for index, item in enumerate(selected_plate):
                if index == 2 or index == 3:
                    continue
                else:
                    temp.append(item.text())
            add_part(temp)
        # Warning message if adding more than 1 item of the same type
        else:
            add_limit()
            return
        self.close()
        self.case.load_table()
        self.case.load_table2(similar_case(selected_plate[1].text()))
        self.case.showMaximized()

    # Show build window
    def show_build(self):
        self.build.load_table()
        self.build.showMaximized()

    # Show Data Visualization Window
    def show_stats(self):
        self.stats.plot_knn()
        self.stats.plot_tfidf()
        self.stats.showMaximized()

    # Close the plate window and clear the build table
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
            open_csv('plate.csv')
            clear_parts()
        else:
            return

    # Populate plate table
    def load_table(self):

        plates = Plate().get_filtered()
        row = 0
        self.tableWidget.setRowCount(len(plates))

        for i in plates:
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

    # Populate plate recommendation table
    def load_table2(self, plates):
        row = 0
        self.tableWidget_2.setRowCount(len(plates))

        for i in plates:
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



