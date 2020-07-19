"""Functions and data for standardizing statements into required columns.
Add new known statement adapter functions here.
Takes data from specific instituitions and adapts into a
standardized dataFrame and adding an 'AutoCategory' column.
"""

import pandas as pd
#import helpers

# Global tuple of columns required to be produced by the Adapters
required_columns = ('Description', 'Date', 'Amount', 'AutoCategory')

# Global dictionary of known statement columns and adpater functions.
known_statements = {}

def auto_categorize_by_desctiption(data, description_categories_list):
    """Adds 'AutoCategory' column populated by matching passed in
    keyword- category pairs to the 'Description' column. If no matches
    default values for the 'AutoCategory' column is nan.

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


########################################################################
# Add new adapter functions here
########################################################################

def bank_one_adapter(data):

    """Adapt bank_one_one statement to have required columns.
    Parameters:
            data (DataFrame): Raw csv statement data.

    Returns:
            data (DataFrame): Adapted DataFrame with required columns
   """

    # Remove deposits. Deposits have null in 'Withdrawl' column.
    data = data[data['Withdrawl'].notnull()]

    data = data.rename(
        columns={'Withdrawl': 'Amount'})

    # Change expenses to postive.
    data['Amount'] = pd.to_numeric(data['Amount']) * -1

     # Get the check# from 'Check' column, it can be blank so fill
     # with -1 to allow astype() to convert the column to ints.
    column_cat = data['Check'].fillna('-1').astype(int)
    # Convert to string and replace the -1s with blanks
    column_cat = column_cat.astype(str).replace("-1", "")

     # Cat the check# and blanks column into the 'Description' column.
    data['Description'] = data['Description'].str.cat(column_cat, sep=" ")

    # List of  keywords to match from the 'Description' field and corresponding new AutoCategory
    description_categories_list = [
        ['ATM', 'Cash'],
        ['Bill Pay', 'Bills & Utilities'],
        ['Check 1158', 'Health & Wellness'],
        ['Transfer', 'Remove from DataFrame'],
        ['Withdrawl', 'Remove from DataFrame']]

     # Keyword Match 'Description' and create new 'AutoCategory' column from
     # keyword-categories list
    data = auto_categorize_by_desctiption(data, description_categories_list)

     # Remove rows marked above with category "Remove from DataFrame"
    data = data[data['AutoCategory'] != "Remove from DataFrame"]

    return data

def credit_card_one_adapter(data):
    """Adapt credit_card_one statement to have required columns.

    Parameters:
            data (DataFrame): Raw csv statement data.

    Returns:
            data (DataFrame): Adapted DataFrame with required columns
   """

    data['Category'].replace({
        "Personal": "Health Services"}, inplace=True)

    data = data.rename(
        columns={'Transaction Date': 'Date'})


     # Change expenses to postive.
    data['Amount'] = data['Amount'] * -1

     # Remove Payments and Withdrawals
    data = data[(data['Type'] != "Payment") & (data['Type'] != "Withdrawal")]

    # Keyword , Category list
    description_categories_list = [
        ['Hair Salon', 'Health & Wellness'],
        ['Online Store', 'Merchandise'],
        ['Clothing Store', 'Merchandise'],
        ['Hobby Store', 'Merchandise'],
        ['Clothing Store', 'Merchandise'],
        ['Online Music', 'Entertainment'],
        ['Online Movies', 'Entertainment'],
        ["Grocery Store", "Groceries"],
        ["Pharmacy", "Groceries"],
        ["Pizza", "Restaurants"],
        ["Restaurant", "Restaurants"],
        ["Rent", "Rent"],
        ["Theme park", "Travel"]]

    # Match 'Description' and
    # Create new 'AutoCategory' column
    data = auto_categorize_by_desctiption(data, description_categories_list)

    # If no 'AutoCategory' assigned, fill with 'Category' column
    data['AutoCategory'] = data['AutoCategory'].fillna(data['Category'])
    return data

def add_new_statement_type(data, name, adapter, columns):
    """Helper function for adding known statement dictionary entries.

    Parameters:
            data (DataFrame): Parent dictionary.
            name (str): Firendly name of entry
            adapter (funktor): Function to convert statement columns to required columns.
            columns (List): List of columns in entry. Used to identify statement.
    Returns:
            data (DataFrame): Parent dictionary appended with new entry
   """

    data[columns] = {'adapter': adapter,
                     'name': name}

    return data

# Example Credit Card
known_statements = add_new_statement_type(
    known_statements,
    'credit_card_one',
    credit_card_one_adapter,
    ('Transaction Date',
     'Post Date',
     'Description',
     'Category',
     'Type',
     'Amount'))

# Example Bank Account
known_statements = add_new_statement_type(
    known_statements,
    'bank_one',
    bank_one_adapter,
    ('Date',
     'Check',
     'Description',
     'Deposit',
     'Withdrawl',
     'Balance'))
