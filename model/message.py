from PyQt5.QtWidgets import QMessageBox


# A collection of message boxes
# Message boxes are used for confirmations, warnings and errors.
# The user is prompted via a message box when triggered
# The user will have to respond by clicking on a button on the message box
def is_selected():
    QMessageBox.critical(None, 'Critical Message', 'Select an item!', QMessageBox.Ok)


def add_limit():
    QMessageBox.warning(None, 'Warning', 'You can only add one of each part.', QMessageBox.Ok)


def confirm_restart():
    confirmation = QMessageBox.question(None, 'Restart Confirmation', 'Clear all selections and restart?',
                                        QMessageBox.Yes | QMessageBox.Cancel)
    if confirmation == QMessageBox.Cancel:
        return False
    if confirmation == QMessageBox.Yes:
        return True


def exit_message():
    leave = QMessageBox.question(None, 'Exit Confirmation', 'End Session?',
                                 QMessageBox.Yes | QMessageBox.Cancel)
    if leave == QMessageBox.Yes:
        return True
    if leave == QMessageBox.Cancel:
        return False


def close_window():
    close = QMessageBox.question(None, 'Close Confirmation', 'Exit application?',
                                 QMessageBox.Yes | QMessageBox.Cancel)
    if close == QMessageBox.Yes:
        return True
    if close == QMessageBox.Cancel:
        return False


def open_file():
    confirmation = QMessageBox.question(None, 'Open File Confirmation', 'Restart application and open file?',
                                        QMessageBox.Yes | QMessageBox.Cancel)
    if confirmation == QMessageBox.Cancel:
        return False
    if confirmation == QMessageBox.Yes:
        return True