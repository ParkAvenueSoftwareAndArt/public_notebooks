"""Functions loading and processing csv files"""

import pandas as pd

from StatementData import known_statements
from StatementData import required_columns


def auto_categorize_by_desctiption(data, description_categories_list):
    """Adds 'AutoCategory' column populated by matching passed in keyword- category pairs to the 'Description' column. If no matches default values for the 'AutoCategory' column is nan.

    Parameters:
            data (DataFrame): Parent dictionary with 'Description' column.
            description_categories_list (List): List of keyword-category pairs.

    Returns:
            data (DataFrame): Parent dictionary appended with 'AutoCategory'
            columns
   """

    df_categories = pd.DataFrame(description_categories_list,
                                 columns=['Keyword', 'AutoCategory'])

    # Add category column filled with nan
    if 'AutoCategory' not in data:
        data['AutoCategory'] = pd.np.nan

    # Iterate through keyword-categories list
    for index, row in df_categories.iterrows():
        # Get all rows containing keyword substring
        matches = pd.DataFrame(data[
            (data['Description'].str.contains(row['Keyword'], case=False))])
        if len(matches) > 0:
            # Set matching AutoCategory row on keyword matching rows and
            # restore to main DataFrame
            matches['AutoCategory'] = row['AutoCategory']
            data.update(matches)


    return data

def load_file(file_path, statments):
    """Load and process

    Parameters:
            file_path (str): Path to csv file.
            statments (List): Known statement Adapters

    Returns:
            data (DataFrame): Adapted DataFrame with required columns
   """
    df_all_columns = pd.DataFrame()

    #get columns list from file.
    df_columns = tuple(pd.read_csv(file_path, nrows=0).columns.values)
    name = statments.get(df_columns)

    if not name:
     print("File columns do not match any known type. Not loading")
    else:
        # Load file
        csv = pd.read_csv(file_path)
        if len(csv) == 0:
            print("read_csv returned empty file", name["name"], " For file")
            print(file_path)
        else:
            print("    Statement Adapter type:", name["name"])
            #Process file via file specific adapter
            df_all_columns = name["adapter"](csv)

    return df_all_columns

def load_csvs(file_list):
    """Load and process

    Parameters:
            file_list (str): Paths to csv files.

    Returns:
            data (DataFrame): Combined adapted DataFrames with required columns
   """
    return load_file_list(
        file_list,
        known_statements,
        required_columns)


def load_file_list(file_list, file_processors, required_columns):
    """Load and process a list of csv file paths

    Parameters:
            file_list (str): Paths to csv files.
            file_processors (List): Known statement Adapters
            required_columns (List): Used to check output of Adapters

     Returns:
            data (DataFrame): Combined adapted DataFrames with required columns
    """

def load_file_list(file_list,file_processors,required_columns):
    files_read = []
    combined = pd.DataFrame()
    for file_path in file_list:
        print("loading:", file_path)
        df_all_columns = load_file(file_path, file_processors)
        diff = tuple(set(required_columns).difference(df_all_columns.columns))
        if len(diff) > 0:
            print("File  does not contain ", diff, "required columns. Not loading")
            print(file_path)
        else:
            # Sucessful load. Add data to list
            files_read.extend([df_all_columns])

    if len(files_read) > 0:
        # Concat list of all datas into final Dataframe
         combined = pd.concat(files_read, ignore_index=False, sort=False)
    else:
         print("No files loaded. Exit!")

    # File wide category adjustments and column clean up

    # If 'AutoCategory' nan, assign to 'None'
    combined['AutoCategory'] = combined['AutoCategory'].fillna('None')

     # Limit to columns this analyzer will be using.
    # Discard other stray columns.
    combined = combined[list(required_columns)]

    return combined

def filter_by_date(data,start_date,end_date):
    """Return data between two dates

    Parameters:
            data (DataFrame): Any data with a 'Date' column.
            start_date (DateTime): Inclusive
            end_date (DateTime): Inclusive

    Returns:
            data (DataFrame): Data between and including start_date and end_date
    """
    df=data[(data['Date'] >= start_date) &
            (data['Date'] <= end_date)]
    if not len(df):
        print("warning empty data frame after filter operation")

    return df


def xirr(transactions):
    """Calculate annualized return

    Parameters:
            transactions (list): .

    Returns:
            guess-1 (float): annualized return
    """
    years = [(ta[0] - transactions[0][0]).days / 365.0 for ta in transactions]
    #print("years",years)
    residual = 1
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000.0
    a = (abs(residual) > epsilon)
    while a & (limit > 0):
        limit -= 1
        residual = 0.0
        for i, ta in enumerate(transactions):
            residual = ta[1] / pow(guess, years[i])

        if (abs(residual) > epsilon):
            if residual > 0:
                guess = step
            else:
                guess -= step
                step /= 2.0

        a = (abs(residual) > epsilon)

    return guess-1
