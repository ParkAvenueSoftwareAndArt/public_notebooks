"""Functions loading and processing csv files"""

import pandas as pd

from statement_adapters import known_statements
from statement_adapters import required_columns

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


def load_file_list(file_list, file_processors, required):
    """Load and process a list of csv file paths

    Parameters:
            file_list (str): Paths to csv files.
            file_processors (List): Known statement Adapters
            required_columns (List): Used to check output of Adapters

     Returns:
            data (DataFrame): Combined adapted DataFrames with required columns
    """
    files_read = []
    combined = pd.DataFrame()
    for file_path in file_list:
        print("loading:", file_path)
        df_all_columns = load_file(file_path, file_processors)
        diff = tuple(set(required).difference(df_all_columns.columns))
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
    combined = combined[list(required)]

    return combined

def filter_by_date(data, start_date, end_date):
    """Return data between two dates

    Parameters:
            data (DataFrame): Any data with a 'Date' column.
            start_date (DateTime): Inclusive
            end_date (DateTime): Inclusive

    Returns:
            data (DataFrame): Data between and including start_date and end_date
    """
    return_df = data[(data['Date'] >= start_date) &
                     (data['Date'] <= end_date)]
    if not len(return_df) > 0:
        print("warning empty data frame after filter operation")

    return return_df
