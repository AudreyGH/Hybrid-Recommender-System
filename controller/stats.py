import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.metrics import mean_absolute_error
from controller.build import exit_app
from model.collaborative_filter import get_original_df, get_predicted_df
from model.content_filter import get_df, get_y, get_x, get_mapk
from view import stats


# Data visualization window controller

# Matplotlib canvas figure
class StatsApp(stats.Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StatsApp, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.addWidget(self.canvas)


# Main GUI window for data visualization
class MainStatsWidget(stats.Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(MainStatsWidget, self).__init__()
        self.setupUi(self)
        self.stats = StatsApp()
        self.stats2 = StatsApp()
        self.stats3 = StatsApp()
        self.vertical_layout = QtWidgets.QVBoxLayout(self.widget)
        self.vertical_layout.addWidget(self.stats)
        self.vertical_layout2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.vertical_layout2.addWidget(self.stats2)
        self.vertical_layout3 = QtWidgets.QVBoxLayout(self.widget_5)
        self.vertical_layout3.addWidget(self.stats3)
        self.pushButton_3.clicked.connect(self.hide)
        self.pushButton_4.clicked.connect(exit_app)

    # Plots KNN data
    def plot_knn(self):
        x = get_x()
        y = get_y()
        names = []

        tuples = list(zip(x, y))
        stats_df1 = pd.DataFrame(tuples, columns=['Distance', 'Item'])

        # Retrieve only 50 Nearest Neighbors if the list contains over 50 items
        if len(stats_df1.index) > 50:
            stats_df = stats_df1.head(50)
        else:
            stats_df = stats_df1

        for i in stats_df.Item:
            names.append(i[0] + ' ' + i[1] + ' ' + i[2])

        # Set descriptions
        self.stats.axis.clear()
        self.stats.axis.set_title('Nearest Neighbor to Currently Selected Part/s', fontsize=20)
        self.stats.axis.set_xlabel('Distance', fontsize=16)
        self.stats.axis.set_ylabel('Neighbors', fontsize=16)

        # Set data and plot
        h_bars = self.stats.axis.barh(stats_df.index, stats_df.Distance)
        self.stats.axis.set_yticks(np.arange(len(stats_df.index)))
        self.stats.axis.set_yticklabels(stats_df.index)
        self.stats.axis.invert_yaxis()
        self.stats.axis.bar_label(h_bars, labels=names, padding=5)
        self.stats.axis.set_xlim(right=1.5)
        self.stats.canvas.draw()

        # Get Mean Average Precision and update stats window
        if get_mapk():
            self.label_4.setText('Mean Average Precision: ' + str(get_mapk()[0]))
        if not get_mapk():
            self.label_4.setText('')
        get_mapk().clear()

    # Plots TF-IDF data
    def plot_tfidf(self):
        df = get_df()

        # Create a dataframe of the average TF-IDF scores of words
        mean = df[0].mean(axis=0)
        tuples = list(zip(df[0].columns.values, mean))
        mean_df1 = pd.DataFrame(tuples, columns=['Words', 'Mean']).sort_values('Mean', ascending=False).reset_index(
            drop=True)

        # Retrieve only top 50 highest TDF-IDF score if list contains over 50 items
        if len(mean_df1.index) > 50:
            mean_df = mean_df1.head(50)
        else:
            mean_df = mean_df1

        names = mean_df.Words  # Bar labels
        x_ticks = mean_df.Mean[0] + 0.1  # Set max x ticks

        # Set descriptions
        self.stats2.axis.clear()
        self.stats2.axis.set_title('Term Frequency–inverse Document Frequency Values', fontsize=20)
        self.stats2.axis.set_ylabel('Words', fontsize=16)
        self.stats2.axis.set_xlabel('Mean TF-IDF Score', fontsize=16)
        self.stats2.axis.title.set_size(18)

        # Set data and plot
        h_bars = self.stats2.axis.barh(mean_df.index, mean_df.Mean)
        self.stats2.axis.set_yticks(np.arange(len(mean_df.index)))
        self.stats2.axis.set_yticklabels(mean_df.index)
        self.stats2.axis.bar_label(h_bars, labels=names, padding=5)
        self.stats2.axis.set_xlim(right=x_ticks)
        self.stats2.canvas.draw()

    # Plots SVD data
    def plot_svd(self):
        original = get_original_df()[0].head(50)
        predicted = get_predicted_df()[0].head(50)

        # Make a new dataframe containing the original ratings, predicted ratings, and their difference
        merged = pd.concat([original['Ave Rating'], predicted['Ave Rating']], axis=1, keys=['Original', 'Prediction'])
        merged['Difference'] = merged['Original'] - merged['Prediction'].astype(float)

        # Set Descriptions
        self.stats3.axis.clear()
        self.stats3.axis.set_title('Original Ratings and Predicted Ratings Difference', fontsize=20)
        self.stats3.axis.set_ylabel('Average Rating', color='b', fontsize=16)
        self.stats3.axis.set_xlabel('Products', fontsize=16)
        self.stats3.axis.title.set_size(18)

        # Get labels for bars
        # If difference is zero, label is blank
        orig_rating = merged['Original']
        error = merged['Difference']
        difference = []
        for e in error:
            if e > 0:
                difference.append('+%.1f'.format(e) % e)
            if e < 0:
                difference.append('-%.1f'.format(e) % e)
            if e == 0:
                difference.append('')

        # Plot
        bars = self.stats3.axis.bar(merged.index, orig_rating, yerr=error, capsize=2, label='Original')
        self.stats3.axis.bar_label(bars, labels=difference)
        self.stats3.axis.legend()
        self.stats3.canvas.draw()

        # Calculate Mean Absolute Error
        predicted_rating = merged['Prediction']
        mae = mean_absolute_error(orig_rating, predicted_rating)
        self.label_20.setText('\nMean Absolute Error = ' + str(mae))
