from PyQt5 import QtWidgets
from controller.build import BuildApp, add_part, clear_parts, search_parts, exit_app
from controller.plate import PlateApp
from model.content_filter import similar_plate
from model.message import add_limit, confirm_restart, is_selected, open_file
from model.read_csv import open_csv
from view import pcb


# The PCB widget controller
# The table is populated with PCB data.
class PcbApp(pcb.Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(PcbApp, self).__init__()
        self.setupUi(self)
        self.plate = PlateApp()
        self.build = BuildApp()
        self.pushButton.clicked.connect(self.add_part)
        self.pushButton_2.clicked.connect(self.show_build)
        self.pushButton_3.clicked.connect(self.start_over)
        self.pushButton_4.clicked.connect(exit_app)
        self.pushButton_6.clicked.connect(self.open_file)

    # Add selected part to build table
    def add_part(self):
        temp = []
        selected_pcb = []

        # If a row is selected, clear selection from other table
        if self.tableWidget.selectionModel().hasSelection():
            self.tableWidget_2.clearSelection()
            selected_pcb = self.tableWidget.selectedItems()
        if self.tableWidget_2.selectionModel().hasSelection():
            self.tableWidget.clearSelection()
            selected_pcb = self.tableWidget_2.selectedItems()

        # Alert user if a row has not been selected from either tables
        if not self.tableWidget.selectionModel().hasSelection() and not self.tableWidget_2.selectionModel().hasSelection():
            is_selected()
            return

        # Add PCB if no PCB exist in the build table
        if not search_parts('PCB'):
            for index, item in enumerate(selected_pcb):
                if index == 4:
                    continue
                else:
                    temp.append(item.text())
            add_part(temp)
            self.close()
            self.plate.load_table()
            self.plate.load_table2(similar_plate(selected_pcb[1].text()))
            self.plate.showMaximized()
        # Warning message if adding more than 1 item of the same type
        # Not needed if code is working properly
        else:
            add_limit()
            return

    # Show build window
    def show_build(self):
        self.build.load_table()
        self.build.showMaximized()

    # Close PCB window and clear the build table
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
            open_csv('board.csv')
            clear_parts()
        else:
            return

    # Populate PCB table
    def load_table(self, layout):
        boards = layout
        row = 0
        self.tableWidget.setRowCount(len(boards))

        for i in boards:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i[5]))
            row += 1
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
        self.tableWidget.clearSelection()

    # Populate PCB recommendation table
    def load_table2(self, boards):
        row = 0
        self.tableWidget_2.setRowCount(len(boards))

        for n in boards:
            self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(n[0]))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(n[1]))
            self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(n[2]))
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(n[3]))
            self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(n[4]))
            self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(n[5]))
            row += 1
            self.tableWidget_2.resizeColumnsToContents()
            self.tableWidget_2.resizeRowsToContents()
        self.tableWidget_2.clearSelection()
