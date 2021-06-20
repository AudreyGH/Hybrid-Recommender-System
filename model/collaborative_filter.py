import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from model.content_filter import sort_keycaps

# Changes the pandas setting of the dataframe to display all the contents of the table
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.expand_frame_repr', False)


# Makes a recommendation based on all users' ratings using singular value decomposition (SVD)
def switch_factorization():
    # Import data from csv file
    a = os.path.normpath(os.path.join(os.path.dirname(__file__), 'switch.csv'))
    p = Path(a).as_posix()
    with open(p) as switch:
        switches = pd.read_csv(switch)

    # Change pandas setting to show the hundredths place of floats
    pd.options.display.float_format = "{:,.2f}".format

    # Reshape dataframe from item table to ratings table
    # Make 'Users' the index and y axis
    # Each column is a distinct product
    # Origin = rating of one user
    # There is definitely a more efficient way to do this
    melted = switches.melt(id_vars=['Brand', 'Series', 'Model', 'Action', 'Ave Rating', 'Price', 'Part'],
                           var_name='Users', value_name='User Rating')
    sorted_df = melted.sort_values(['Brand', 'Series', 'Model']).reset_index(drop=True)
    new_df = sorted_df.set_index('Users').reset_index()
    pivot_df = new_df.pivot_table(index='Users', columns=['Brand', 'Series', 'Model', 'Action',
                                                          'Ave Rating', 'Price', 'Part'])

    # Convert dataframe to numpy array and normalize ratings matrix
    pivot_matrix = np.asmatrix(pivot_df)
    ratings_mean = np.mean(pivot_matrix, axis=1)
    ratings_demean = pivot_matrix - ratings_mean.reshape(-1, 1)

    # Singular value decomposition of matrix
    U, sigma, Vt = svds(ratings_demean, k=3)
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt) + ratings_mean.reshape(-1, 1)


    # Create a dataframe from rating predictions and reshape to the format used by the table widget
    prediction_df = pd.DataFrame(predicted_ratings, columns=pivot_df.columns, index=pivot_df.index.transpose())
    unstacked_df = prediction_df.stack([1, 2, 3, 4, 5, 6, 7]).reset_index()
    column_names = ['Brand', 'Series', 'Model', 'Action', 'Ave Rating', 'Price', 'Part']
    unstacked_user = unstacked_df.set_index(['Users'] + column_names).unstack('Users')
    normal_df = unstacked_user.xs('User Rating', axis=1, drop_level=True).reset_index()

    # Get average of ratings, round to required decimal format and convert floats to string
    normal_df['Ave Rating'] = normal_df[['User1', 'User2', 'User3', 'User4']].mean(
        axis=1)  # Average of user ratings per item
    rounded_df = normal_df.round({'Ave Rating': 1, 'Price': 2})  # Round rating and price
    rounded_df['Ave Rating'] = rounded_df['Ave Rating'].astype('str')  # Average rating to string datatype
    rounded_df['Price'] = rounded_df['Price'].apply(lambda x: "{:.2f}".format(x))  # Format price to have trailing zeros

    # Prepare original and predicted dataframes for MAE calculation in the stats window
    get_original_df().clear()
    get_predicted_df().clear()
    set_original_df(switches.sort_values(['Brand', 'Series', 'Model']).reset_index(drop=True))
    set_predicted_df(rounded_df)

    return sort_keycaps(rounded_df)


# Makes a recommendation based on all users' ratings using singular value decomposition (SVD)
def keycap_factorization(keycaps):
    k = 3

    # Change pandas setting to show the hundredths place of floats
    pd.options.display.float_format = "{:,.2f}".format

    # Convert keycaps list to dataframe
    data = pd.DataFrame(keycaps)
    data.rename(columns={0: 'Profile', 1: 'Name', 2: 'Material', 3: 'Color/Design Name', 4: 'Backlit',
                         5: 'Ave Rating', 6: 'Price', 7: 'Part', 8: 'User1', 9: 'User2', 10: 'User3',
                         11: 'User4'}, inplace=True)

    # Return dataframe if there is only one item
    if len(keycaps) <= 3:
        k = len(keycaps) - 1
    if len(keycaps) == 1:
        return sort_keycaps(data)

    # Change numbers that are strings into floats
    data[['Ave Rating', 'Price', 'User1', 'User2', 'User3', 'User4']] = data[
        ['Ave Rating', 'Price', 'User1', 'User2', 'User3', 'User4']].astype(float)

    # Reshape dataframe from item table to ratings table
    # Make 'Users' the index and y axis
    # Each column is a distinct product
    # Origin = rating of one user
    # There is definitely a more efficient way to do this
    melted = data.melt(
        id_vars=['Profile', 'Name', 'Material', 'Color/Design Name', 'Backlit', 'Ave Rating', 'Price', 'Part'],
        var_name='Users', value_name='User Rating')
    sorted_df = melted.sort_values(['Profile', 'Name', 'Material']).reset_index(drop=True)
    new_df = sorted_df.set_index('Users').reset_index()
    pivot_df = new_df.pivot_table(index='Users', columns=['Profile', 'Name', 'Material', 'Color/Design Name', 'Backlit',
                                                          'Ave Rating', 'Price', 'Part'])

    # Convert dataframe to numpy array and normalize ratings matrix
    pivot_matrix = np.asmatrix(pivot_df)
    ratings_mean = np.mean(pivot_matrix, axis=1)
    ratings_demean = pivot_matrix - ratings_mean.reshape(-1, 1)

    # Singular value decomposition of matrix
    # k must be adjusted if there are less than 4 items
    # k must be between 1 and min(A.shape)
    # min(A.shape) = 4 = total number of users
    U, sigma, Vt = svds(ratings_demean, k=k)
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt) + ratings_mean.reshape(-1, 1)

    # Create a dataframe from rating predictions and reshape to the format used by the table widget
    prediction_df = pd.DataFrame(predicted_ratings, columns=pivot_df.columns, index=pivot_df.index.transpose())
    unstacked_df = prediction_df.stack([1, 2, 3, 4, 5, 6, 7, 8]).reset_index()
    column_names = ['Profile', 'Name', 'Material', 'Color/Design Name', 'Backlit', 'Ave Rating', 'Price', 'Part']
    unstacked_user = unstacked_df.set_index(['Users'] + column_names).unstack('Users')
    normal_df = unstacked_user.xs('User Rating', axis=1, drop_level=True).reset_index()

    # Get average of ratings, round to required decimal format and convert floats to string
    normal_df['Ave Rating'] = normal_df[['User1', 'User2', 'User3', 'User4']].mean(
        axis=1)  # Average of user ratings per item
    rounded_df = normal_df.round({'Ave Rating': 1, 'Price': 2})  # Round rating and price
    rounded_df['Ave Rating'] = rounded_df['Ave Rating'].astype('str')  # Average rating to string datatype
    rounded_df['Price'] = rounded_df['Price'].apply(
        lambda x: "{:.2f}".format(x))  # Format price to have trailing zeros up to 2 decimal places

    # Prepare original and predicted dataframes for MAE calculation in the stats window
    get_original_df().clear()
    get_predicted_df().clear()
    set_original_df(data.sort_values(['Profile', 'Name', 'Material']).reset_index(drop=True))
    set_predicted_df(rounded_df)

    return sort_keycaps(rounded_df)


# Setters and getters for variables needed to calculate MAE in the stats window
original_df = []
predict_df = []


def set_original_df(df):
    original_df.append(df)


def set_predicted_df(df):
    predict_df.append(df)


def get_original_df():
    return original_df


def get_predicted_df():
    return predict_df
