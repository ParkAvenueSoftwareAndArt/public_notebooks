# public_notebooks

## spending_analyzer [spending_analyzer/spending_analyzer.ipynb](https://github.com/ParkAvenueSoftwareAndArt/public_notebooks/blob/master/spending_analyzer/spending_analyzer.ipynb).


Jupyter, Python and Pandas spending view and analyzer. Load and combine statements downloaded from banks and credit card companies. Autocategorize from transaction description with user created keyword/category tables. Further filter,group,calculate and pivot data in Jupyter display.

  * Load CSV statements into combined pandas DataFrame
  * Provide mechanism to identify different statement types by known column names.
  * Provide Adapter interface
  * Provide mechanism to add new statement types and adapter interface
  * Provide adapter implemtations for different statement types
    * parse statements into required columns. rename columns etc...
    * parse transaction descriptions or transaction category into 'AutoCategory' column
  * With 12+ months of data Calculate previous calendar year's monthy mean per 'AutoCategory'
  * Calculate current calendar year's monthy mean per 'AutoCategory'
  * Pandas Pivot table, show current calendar years monthy spending per 'AutoCategory' with mean columns

Input
  * Bank or credit card statements in CSV format
  * Required columns: Date,Description,Amount

Output
  * Combined Pandas DataFrame with required output columns: Date,Description,Amount,AutoCategory
  * Jupyter displays of Pandas DataFrames
