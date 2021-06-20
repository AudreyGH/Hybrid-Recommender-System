from PyQt5 import QtWidgets
from view import build
from model.message import add_limit, confirm_restart, exit_message, close_window, is_selected

all_parts = []  # filtered parts used to populate the build table


# The build widget controller
# The table is populated with data added by user in other windows
class BuildApp(build.Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(BuildApp, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.hide)
        self.pushButton_4.clicked.connect(exit_app)

    # Load the build table
    def load_table(self):
        parts = get_parts()
        self.clear_table()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(get_parts()))
        row = 0

        for i in parts:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(i[4]))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            row += 1
        # self.lcdNumber.display(add_price())
        self.label_3.setText('$' + str(add_price()))

    # Clear the build table
    def clear_table(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)


# Add part to all_parts
def add_part(item):
    layout = item[0]
    name = item[1]
    rating = item[2]
    price = item[3]
    part = item[4]

    items = [layout, name, rating, price, part]
    all_parts.append(items)


# Remove item from all_parts
def remove_part(item):
    all_parts.remove(item)


# Getter for all_parts
def get_parts():
    return all_parts


# Clear contents of all_parts
def clear_parts():
    all_parts.clear()


# Search fifth column of all_parts for a match
def search_parts(item):
    if int(len(all_parts)) == 0:
        return False
    for search in all_parts:
        if search[4] == item:
            return True
    return False


# Returns sum of prices
def add_price():
    total = 0
    for i in all_parts:
        total += float(i[3])
    return '{:.2f}'.format(total)


# Asks user to continue or cancel when the window is closed
def exit_app():
    if exit_message():
        exit()
    else:
        return
