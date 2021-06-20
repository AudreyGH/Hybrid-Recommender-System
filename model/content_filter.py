import ml_metrics as metrics
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from controller.build import get_parts
from model.read_csv import Plate, Case, Keycap

# Changes the pandas setting of the dataframe to display all the contents of the table
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.expand_frame_repr', False)

# Variables needed for data visualization and evaluation metrics
x = []
y = []
df = []
mapk = []


# Find plates that are similar to the selected PCB
# Returns a sorted and filtered nested list of plates
def similar_plate(query):
    recommended_plates = []  # container for recommended items
    input_word = pd.DataFrame([query])  # item input as a pandas dataframe

    # Define the TFIDF vectorizer and set it to clean data by removing stop words when called
    vec = TfidfVectorizer(stop_words='english')

    selected_layout = pd.DataFrame(Plate().get_filtered())  # Convert dataset to pandas dataframe
    features = vec.fit_transform(selected_layout[1])  # Create normalized vectors by applying vectorizer to dataset
    input_features = vec.transform(input_word[0])  # Get the names of features

    # Instantiate nearest neighbor object and train
    neighbors = len(selected_layout)  # number of neighbors based on number of items in dataset

    # X_train, X_test, y_train, y_test = train_test_split()
    knn = NearestNeighbors(n_neighbors=neighbors, metric='cosine')
    knn.fit(features)

    # Retrieve data for TF-IDF data visualization
    tfidf_df = pd.DataFrame(features.toarray(), columns=vec.get_feature_names())
    df.clear()
    add_df(tfidf_df)

    # Find nearest neighbors
    D, N = knn.kneighbors(input_features, return_distance=True)

    # Add nearest neighbors(most similar items) to recommended list and retrieve data for visualization
    temp = []
    x.clear()
    y.clear()
    for distance, index in zip(D[0], N[0]):
        item = selected_layout.loc[index].tolist()
        add_x(distance)
        add_y([item[1], item[2], item[3]])
        if distance < 1:
            recommended_plates.append(item)
            temp.append([distance, item[1], item[2], item[3], item[4]])
    nearest = pd.DataFrame(temp)
    nearest.rename(columns={0: 'Distance', 1: 'Name', 2: 'Material', 3: 'Color/Design Name', 4: 'Average Rating'},
                   inplace=True)
    if len(temp) > 0:
        print(
            '***********************************************************************************************************')
        print('   Nearest Neighbors(Plates):')
        print('   Previous selection: ', get_parts()[0][1])
        print(
            '***********************************************************************************************************')
        print(nearest)
        print(
            '***********************************************************************************************************')

    # If no similar items are found, retrieve top 10 rated from dataset
    if len(recommended_plates) == 0:
        sorted_list = sort_plate(Plate().get_filtered())
        print(
            '***********************************************************************************************************')
        print('   No matches found. Top five rated items will be recommended')
        print(
            '***********************************************************************************************************')
    else:
        # Get Mean Average Precision of KNN
        # actual = list of list of elements that are to be predicted (order doesn't matter in the lists)
        # predicted = A list of lists of predicted elements (order matters in the lists)
        # k = The maximum number of predicted elements
        actual = Plate().get_filtered()
        predicted = recommended_plates
        k = len(predicted)
        mapk.clear()
        add_mapk(metrics.mapk(actual, predicted, k))

        # Get top five nearest neighbor and sort by rating
        dataframe = pd.DataFrame(recommended_plates)
        plate_data = dataframe.head().sort_values([4], ascending=False)
        sorted_list = plate_data.values.tolist()

    return sorted_list


# Find cases that are similar to the selected items
# Returns a sorted and filtered nested list of cases
def similar_case(query):
    recommended = []
    input_word = pd.DataFrame([query])

    # Define the TFIDF vectorizer and set it to clean data by removing stop words when called
    vec = TfidfVectorizer(stop_words='english')
    # Convert dataset to pandas dataframe
    selected_layout = pd.DataFrame(Case().get_filtered())
    # Create normalized vectors by applying vectorizer to dataset
    features = vec.fit_transform(selected_layout[1])
    # Get the names of features
    input_features = vec.transform(input_word[0])

    # Instantiate nearest neighbor object and train
    neighbors = len(selected_layout)  # number of neighbors based on number of items in dataset
    knn = NearestNeighbors(n_neighbors=neighbors, metric='cosine')
    knn.fit(features)

    # Retrieve data for TF-IDF data visualization
    tfidf_df = pd.DataFrame(features.toarray(), columns=vec.get_feature_names())
    df.clear()
    add_df(tfidf_df)

    # Find nearest neighbors
    D, N = knn.kneighbors(input_features, return_distance=True)

    # Add nearest neighbors(most similar items) to recommended list and retrieve data for visualization
    temp = []
    x.clear()
    y.clear()
    for distance, index in zip(D[0], N[0]):
        item = selected_layout.loc[index].tolist()
        add_x(distance)
        add_y([item[1], item[2], item[3], item[4]])
        if distance < 1:
            recommended.append(item)
            temp.append([distance, item[1], item[2], item[3], item[4]])
    nearest = pd.DataFrame(temp)
    nearest.rename(columns={0: 'Distance', 1: 'Name', 2: 'Material', 3: 'Color/Design Name', 4: 'Average Rating'},
                   inplace=True)
    if len(temp) > 0:
        print(
            '***********************************************************************************************************')
        print('   Nearest Neighbors(Cases):')
        print('   Previous selections: ', end=' ')
        print(get_parts()[0][1], get_parts()[1][1], sep=', ')
        print(
            '***********************************************************************************************************')
        print(nearest)
        print(
            '***********************************************************************************************************')

    # Sort recommended cases by rating in descending order and retrieve top 5 rated
    # Retrieve 5 highest rated cases from list of all cases if no similar items are found
    if len(recommended) == 0:
        sorted_list = sort_cases(Case().get_filtered())
        print(
            '***********************************************************************************************************')
        print('   No matches found. Top five rated items will be recommended')
        print(
            '***********************************************************************************************************')

    else:
        # Get Mean Average Precision of KNN
        # actual = list of list of elements that are to be predicted (order doesn't matter in the lists)
        # predicted = A list of lists of predicted elements (order matters in the lists)
        # k = The maximum number of predicted elements
        actual = Case().get_filtered()
        predicted = recommended
        k = len(predicted)
        mapk.clear()
        add_mapk(metrics.mapk(actual, predicted, k))

        # Get top five nearest neighbor and sort by rating
        dataframe = pd.DataFrame(recommended)
        case_data = dataframe.head().sort_values([4], ascending=False)
        sorted_list = case_data.values.tolist()

    return sorted_list


# Find keycaps that are similar to selected items
# Returns a sorted recommended nested list of keycaps
def similar_keycap():
    recommended = []
    words_list = []
    query = get_parts()

    # Join words of previously selected items and convert to pandas dataframe
    # Switches are ignored since they have zero similarity with other products
    if len(query) > 0:
        for index, i in enumerate(query):
            if index < 3:
                words_list.append(i[1])
        joined_words = ' '.join(words_list)
        keycaps_list = []
        # Convert list of words to pandas dataframe
        for i in Keycap().load_keycap():
            keycaps_list.append(i)
        input_word = pd.DataFrame([joined_words])

        # Define the TFIDF vectorizer and set it to clean data by removing stop words when called
        vec = TfidfVectorizer(stop_words='english')
        # Convert dataset to pandas dataframe
        selected_layout = pd.DataFrame(keycaps_list)
        # Create normalized vectors by applying vectorizer to dataset
        features = vec.fit_transform(selected_layout[1] + ' ' + selected_layout[2] + ' ' + selected_layout[3])
        # Get the names of features
        input_features = vec.transform(input_word[0])

        # Instantiate nearest neighbor object and train
        neighbors = len(selected_layout)  # number of neighbors based on number of items in dataset
        knn = NearestNeighbors(n_neighbors=neighbors, metric='cosine')
        knn.fit(features)

        # Retrieve data for TF-IDF data visualization
        tfidf_df = pd.DataFrame(features.toarray(), columns=vec.get_feature_names())
        df.clear()
        add_df(tfidf_df)

        # Find nearest neighbors
        D, N = knn.kneighbors(input_features, return_distance=True)

        # Add nearest neighbors(most similar items) to recommended list and retrieve data for visualization
        temp = []
        x.clear()
        y.clear()
        for distance, index in zip(D[0], N[0]):
            item = selected_layout.loc[index].tolist()
            add_x(distance)
            add_y([item[1], item[2], item[3], item[4]])

            if distance < 1:
                recommended.append(item)
                temp.append([distance, item[0], item[1], item[2], item[3], item[5]])

        nearest = pd.DataFrame(temp)
        nearest.rename(columns={0: 'Distance', 1: 'Profile', 2: 'Name', 3: 'Material', 4: 'Color/Design Name',
                                5: 'Ave Rating'}, inplace=True)
        if len(temp) > 0:
            print(
                '***********************************************************************************************************')
            print('   Nearest Neighbors(Keycaps):')
            print('   Previous selections: ', end=' ')
            print(get_parts()[0][1], get_parts()[1][1], get_parts()[2][1], sep=', ')
            print(
                '***********************************************************************************************************')
            print(nearest)
            print(
                '***********************************************************************************************************')

        # Sort recommended keycaps by rating in descending order
        # Retrieve 5 highest rated keycaps from list of all keycaps if no similar items are found
        if len(recommended) == 0:
            sorted_list = sort_keycaps(Keycap().load_keycap())
            print(
                '***********************************************************************************************************')
            print('   No matches found. User ratings will be used to generate recommendations')
            print(
                '***********************************************************************************************************')
        else:
            # Get Mean Average Precision of KNN
            # actual = list of list of elements that are to be predicted (order doesn't matter in the lists)
            # predicted = A list of lists of predicted elements (order matters in the lists)
            # k = The maximum number of predicted elements
            actual = keycaps_list
            predicted = recommended
            k = len(predicted)
            mapk.clear()
            add_mapk(metrics.mapk(actual, predicted, k))

            # Get top five nearest neighbor and sort by rating
            dataframe = pd.DataFrame(recommended)
            keycap_data = dataframe.head().sort_values([5], ascending=False)
            sorted_list = keycap_data.values.tolist()

        return sorted_list


# Sort by rating and return top 3
# Dataset is too small to recommend a top 5
def sort_pcb(pcb):
    pcb_data = pcb.sort_values([2], ascending=False).head(3)
    sorted_list = pcb_data.values.tolist()

    return sorted_list


# Sort by rating and return top 5 plates
def sort_plate(plate):
    plate_df = pd.DataFrame(plate)
    plate_data = plate_df.sort_values([4], ascending=False).head()
    sorted_list = plate_data.values.tolist()

    return sorted_list


# Sort by rating and return top 5 cases
def sort_cases(case):
    case_df = pd.DataFrame(case)
    case_data = case_df.sort_values([4], ascending=False).head()
    sorted_list = case_data.values.tolist()

    return sorted_list


# Sort by rating and return top 5 switches
def sort_switches(switches):
    switch_data = switches.sort_values(['Ave Rating'], ascending=False).head()
    sorted_list = switch_data.values.tolist()

    return sorted_list


# Sort by rating and return top 5 keycaps
def sort_keycaps(keycaps):
    keycap_data = keycaps.sort_values(['Ave Rating'], ascending=False).head()
    sorted_list = keycap_data.values.tolist()

    return sorted_list


# Setters and getters for data needed in visualization and evaluation metrics in the stats window
def add_x(a):
    x.append(a)


def add_y(a):
    y.append(a)


def add_df(a):
    df.append(a)


def add_mapk(a):
    mapk.append(a)


def get_x():
    return x


def get_y():
    return y


def get_df():
    return df


def get_mapk():
    return mapk
