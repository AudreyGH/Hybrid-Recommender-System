import sys
from PyQt5 import QtWidgets
from controller import main_window

print('\nWelcome to the KBDFans Parts Recommender System!\n')
print('The purpose of this application is to demonstrate some of the most '
      'common filtering methods used to recommend products in e-commerce.\n')
print('Types of filters:')
print('1. A simple filter that recommends the highest rated products.')
print('2. A content-based filter that uses Natural Language Processing (NLP) and K-Nearest Neighbors algorithm (KNN).')
print('3. A collaborative filter using Singular Value Decomposition (SVD) of a matrix (matrix factorization).')
print('4. A hybrid filter using a combination of simple, content-based and collaborative filters.\n')
print('Filters used in each window:')
print('PCB window: Simple filter.')
print('Plate window: Simple filter and content-based filter.')
print('Case window: Simple filter and content-based filter.')
print('Switch window: Simple filter and collaborative filter.')
print('Keycap window: All filters.')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = main_window.MyQtApp()
    main.show()
    sys.exit(app.exec_())
