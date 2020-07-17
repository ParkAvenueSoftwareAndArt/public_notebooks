# public_notebooks

## spending_analyzer


Helper code:

  * Load CSV statements downloaded from banks or credit card companies websites and concat individual statements into combined pandas DataFrame
  * Provide mechanism to identify different statement types by known column names.
  
StatementData: 

  * Provide Adapter interface
  * Provide mechanism to add new statement types and adapter interface
  * Provide adapter implemtations for different statement types
    * parse statements into required columns. rename columns etc...
    * parse transaction descriptions or transaction category into 'AutoCategory' column
 * 

Jupyter Display & Pandas code:
  With 12+ months of data

  * Load CSVs
  * Calculate previous calendar year's monthy mean per 'AutoCategory'
  * Calculate current calendar year's monthy mean per 'AutoCategory'

   Pandas Pivot table
   * Show current calendar years monthy spending per 'AutoCategory' with means


Input
  * Bank or credit card statements in CSV format
  * Required columns: Date,Description,Amount

Output
  * Combined Pandas DataFrame with Date,Description,Amount,AutoCategory columns











