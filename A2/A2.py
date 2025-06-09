"""
This module provides tools for: data cleaning, investigating time and memory usage of algorithms.

Classes:
    CleanerClass: A class containing methods for cleaning Pandas DataFrames.
    TimeAndMemory: A class containing methods for investigating time and memory usage of algorithms. 

Methods in CleanerClass:
    - split_header()
    - col_order_sort(col_order, col_to_sort=None)
    - nan_count()
    - to_numeric(cols)
    - no_adjustment(col_pair1, col_pair2=None)
    - drop_missing_adjustment(col_pair1, col_pair2)
    - count_removed_rows(df1, df2)
    - rm_zero_rows(col_to_ignore=None)
    - rm_empty_rows(col_to_ignore=None)
    - rm_unmatched_signs(col1, col2, col3, col4)
    - replace_missing_values(group, cols)
    - diy_describe()
    - rm_duplicates()

Methods in TimeAndMemory:
    - mat_mult(size)
    - mat_mult_np(size)
    - sort_ints(length)
    - substring_inv(length)
    - python_find_inv(length)
    - random_str(length)
    - substring_check(string, substring)
    - save_results(name, func_df)
    - investigate(function, name, step_size=10)
    - calc_sf(name, relationship, var_type='time')
    - normalise(var1, var2)
    - plot_specification(x, y, s_comp, title, xlabel, ylabel, label='Investigation', s_comp_label='comparison')
    - extract_vars(name)
    - plots(name, variable, exp_rel)
    - plot_memory_bar(name, name2=None)
    - log_plot(name, variable)
    - calc_residuals(measured_vals, scaled_vals)
    - plot_residuals(variable, methods=None)

Dependencies:
    - pandas
    - numpy
    - matplotlib
    - gc
    - psutil
    - os

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import psutil
import os


class CleanerClass:

    """This class implements data cleaning functions.

    Attributes
    ---------
    df (DataFrame): The DataFrame that will be cleaned.
    """

    def __init__(self, df):
        """Initialise the CleanerClass with the input DataFrame."""
        self.df = df


    def split_cols(self, separator):
    
        """
        Splits the first column of the DataFrame into multiple columns at the specified 
        string separator and updates the DataFrame in place.

        This method splits the first column into multiple columns based on specified separator 
        string and updates the DataFrame by replacing the original structure with the expanded one. 
        The resulting columns are named using the values from the first row of the original DataFrame 
        as headers.
        If the number of resulting columns does not match the expected number (determined by the 
        initial header row), an exception is raised. After splitting, the method prints:
        - The number of columns in the original DataFrame.
        - The number of columns created.
        - The total number of rows in the updated DataFrame.

        Parameters:
            separator (str): The string used to split the DataFrame. 
        
        Returns:
            self: The updated CleanerClass object with the modified DataFrame. 

        Raises:
            ValueError: If the number of resulting columns does not match the expected number, or
            if the separator character does not exist in header column. 

        Example:
            df = pd.read_csv('example.csv')
            cleaner = CleanerClass(df)
            cleaner.split_header()
        """
        
        col_header = self.df.columns[0]
        expected_cols = col_header.count(separator) + 1
        
        # Check if the separator appears in the first column
        if not self.df[col_header].str.contains(separator, na=False).any():
            raise ValueError(f"The separator '{separator}' does not exist in the first column, so the DataFrame cannot be split.")
        else:
            # Extract col names
            col_names = self.df.columns[0].split(separator)
            # Split at the separator character
            df_split = self.df[self.df.columns[0]].str.split(separator, expand=True)
            # Rename columns 
            df_split.columns = col_names

        # Check the DataFrame was split as expected
        if(expected_cols != len(df_split.columns)):
            raise ValueError(f"Expected columns: {expected_cols}, Actual columns: {len(df_split.columns)}") 

        # Tell user the results
        print(f"Header split completed.\nOriginal number of columns: {len(self.df.columns)}, New number of columns: {len(df_split.columns)} \nNumber of rows: {self.df.shape[0]}")

        # Update self.df for future use
        self.df = df_split
        
        return self
        

    def col_order_sort(self, col_order, col_to_sort=None):
    
        """
        Reorders the columns of the DataFrame based on the specified column order, and sorts
        on a specified column.

        The method checks if all specified columns exist in 'self.df', and if the specified 
        column to sort on exists. If both checks are passed the desired column order is set 
        and the rows of the DataFrame are sorted in ascending order. 

        Parameters:
            col_order (list): List of column names in the desired order.
            col_to_sort (str): The column to sort in ascending order (optional, default=None).

        Returns:
            self: The updated CleanerClass object with the reordered DataFrame.
    
        Raises:
            ValueError: If any column names in col_order or col_to_sort do not exist in 
            the DataFrame.

        Example:
            >>> df = pd.read_csv('example.csv')
            >>> cleaner = CleanerClass(df)
            >>> cleaner.col_order_sort(['Level', 'A', 'B'], 'Level')
        
        """
        # Check if all columns in col_order exist in the DataFrame
        missing_cols = [col for col in col_order if col not in self.df.columns]

        # Re-order columns
        if missing_cols:
            raise ValueError(f"The following columns are not in the DataFrame: {missing_cols}")
        else:
            self.df = self.df[col_order]

        # Sort on specified column
        if col_to_sort:
            if col_to_sort in self.df.columns:
                self.df = self.df.sort_values(by=col_to_sort, ascending=True).reset_index(drop=True)
            else:
                raise ValueError(f"Given column to sort on, '{col_to_sort}', does not exist in DataFrame.")
    
        return self


    def nan_count(self):

        """
        The method counts the number of NaN values within each column of the DataFrame.

        The method count the number of NaN values within each column of the self.df DataFrame.
        It calculates this as a percentage, rounded to 2 decimal places, and prints the count 
        and percentage for the user. 

        Returns:
            None: Prints results to screen but does not return a value.

        Example:
            >>> df = pd.read_csv('example.csv')
            >>> cleaner = CleanerClass(df)
            >>> cleaner.nan_count()
                # Number of NaN values per column:
                X             0
                Y             4
                dtype: int64

                # Percentage of NaN values per column:
                X             0.00
                Y             25.00
                dtype: float64 
                
        """

        # Calculate counts and percentages
        total_row_count = self.df.shape[0]
        nan_count = self.df.isna().sum()
        nan_percentage = round((nan_count / total_row_count) * 100, 2)

        # Print diagnostics
        print(f"Number of NaN values per column:\n{nan_count}\n\nPercentage of NaN values per column: \n{nan_percentage}")

        return None


    def to_numeric(self, cols):
        
        """
        Converts all columns within the DataFrame to numeric data types.

        The method converts all columns within the original DataFrame to be of numeric data 
        types. If there are any errors, such as those from missing values, the method coerces 
        these to NaN. The method then calculates the percentage of NaN values within each row 
        of the DataFrame, printing these on screen. The method updates the DataFrame in place,
        replacing the original DataFrame with the new numeric DataFrame. 

        Parameters:
            cols (list): A list of column names to be converted to numeric data types.

        Raises:
            ValueError: If any column in 'cols' does not exist in the 'self.df' DataFrame. 

        Returns:
            self: The updated CleanerClass object with the modified DataFrame.

        Example:
            df = pd.read_csv('example2.csv')
            cleaner = CleanerClass(df)
            cleaner.to_numeric()

        """

        # Check all cols given exist in df
        missing_cols = [col for col in cols if col not in self.df.columns]

        # Validate specified columns
        if missing_cols:
            raise ValueError(f"The following columns are not in the DataFrame: {missing_cols}.")
        
        # Convert to numeric
        self.df = self.df[cols].apply(pd.to_numeric, errors='coerce')

        # Count NaN values
        self.nan_count()

        return self

    def no_adjustment(self, col_pair1, col_pair2=None):

        """
        The method checks the number of rows with missing data in pairs of adjusted columns.

        The method extracts the number of rows from 'self.df' that have values in the first 
        column from 'col_pair1' but not in the second column from 'col_pair1'. It then prints
        the number of rows in 'self.df' with values in the first column from 'col_pair1' but
        not the second. If an argument is given for col_pair2, the same is done for this pair 
        of columns. This method is used to gain a better understanding of the spread of missing 
        values in a DataFrame. 

        Parameters:
            col_pair1 (tuple): The first tuple of column pairs to check for missing values.
            col_pair2 (tuple): The second tuple of column pairs to check for missing values 
            (optional).

        Raises:
            TypeError: If col_pairs are not of type 'tuple'.
            ValueError: If col_pairs are not of length 2.

        Returns:
            None: The method prints information to the screen but does not return a value.

        Example:
            df = pd.read_csv('example2.csv')
            cleaner = CleanerClass(df)
            cleaner.no_adjustment(['T3', 'T3adjusted'], ['T4', 'T4adjusted'])
            >>>> Rows with T3 but no T3adjusted: 2
            >>>> Rows with T4 but no T4adjusted: 5
        """

        # Validation checks
        if not (isinstance(col_pair1, tuple) or isinstance(col_pair2, tuple)):
            raise TypeError(f"'{col_pair1}' and '{col_pair2}' must tuples.")

        if len(col_pair1) != 2 or (col_pair2 and len(col_pair2) != 2):
            raise ValueError(f"Column pairs must be of length two.")

        # Calculate missingness for first pair
        no_pair1_adjusted = self.df[self.df[col_pair1[0]].notna() & self.df[col_pair1[1]].isna()].shape[0]
        print(f"Rows with {col_pair1[0]} but no {col_pair1[1]}: {no_pair1_adjusted}")

        # Calculate missingness for second pair
        if col_pair2:
            no_pair2_adjusted = self.df[self.df[col_pair2[0]].notna() & self.df[col_pair2[1]].isna()].shape[0]
            print(f"Rows with {col_pair2[0]} but no {col_pair2[1]}: {no_pair2_adjusted}")

        return None


    def drop_missing_adjustment(self, col_pair1, col_pair2):

        """
        The method removes rows form the DataFrame where one column in a pair has a value but 
        the other is missing.

        The method uses the column pairs provided as inputs ('col_pair1', 'col_pair2'). It 
        identifies rows where:
            1. The first column in the first pair has a non-missing value, but the second column 
            in the first pair is missing.
            2. The first column in the second pair has a non-missing value, but the second column 
            in the second pair is missing.

        Rows that satisfy these conditions are removed from the DataFrame. The filtered
        DataFrame replaces 'self.df' and its index values are reset. The method prints the number 
        of rows removed using the 'count_removed_rows' method.

        Parameters:
            col_pair1 (tuple): A tuple containing the first pair of column names.
            col_pair2 (tuple): A tuple containing the second pair of column names.

        Returns:
            self: The updated CleanerClass object with rows removed.

        Raises:
            TypeError: If col_pairs are not of type 'tuple'.
            ValueError: If col_pairs are not of length 2.
            ValueError: If the specified columns do not exist in the DataFrame. 

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.drop_missing_adjustment(('T3', 'T3adjusted'), ('T4', 'T4adjusted'))
                # Number of rows removed from DataFrame: 1
                # Percentage of rows removed from DataFrame: 0.05

        """

        # Validation checks
        if not (isinstance(col_pair1, tuple) or isinstance(col_pair2, tuple)):
            raise TypeError(f"'{col_pair1}' and '{col_pair2}' must tuples.")

        if len(col_pair1) != 2 or len(col_pair2) != 2:
            raise ValueError(f"Column pairs must be of length two.")

        combined_cols = col_pair1 + col_pair2
        for col in combined_cols:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' does not exist in the DataFrame.")

        # Filter DataFrame based on column pairs
        no_p1_adjusted = self.df[col_pair1[0]].notna() & self.df[col_pair1[1]].isna()
        no_p2_adjusted = self.df[col_pair2[0]].notna() & self.df[col_pair2[1]].isna()
        combined = no_p1_adjusted | no_p2_adjusted

        # Apply generated mask
        filtered_df = self.df[~combined]

        # Print results and update df in place
        print(self.count_removed_rows(self.df, filtered_df))
        self.df = filtered_df.reset_index(drop=True)
        return self


    def count_removed_rows(self, df1, df2):

        """
        A helper function that counts the number of rows that have been removed from df1. 

        The method caculates the number of rows in df1, and df2. It assumes df1 is larger 
        than df2 and calculates the difference between the two DataFrames, printing the 
        result on screen.

        Parameters:
            df1 (DataFrame): The first DataFrame to count the size of.
            df2 (DataFrame): The second DataFrame to count the size of. 

        Raises:
            TypeError: If 'df1' and 'df2' are not Pandas DataFrames.
            ValueError: If 'df2' is larger than 'df1'. 

        Returns:
            A string containing the number of rows removed. 

        Example:
            >>> df = pd.read_csv('example3.csv')
            >>> cleaner = CleanerClass(df)
            >>> cleaner.count_removed_rows(df1, df2)
                Number of rows removed from DataFrame: 5
                Percentage of rows removed: 2.05%
                
        """
        # Validation checks
        if not isinstance(df1, pd.DataFrame) or isinstance(df2, pd.DataFrame):
            TypeError("Both 'df1' and 'df2' must be Pandas DataFrames.")
        
        df1_len = len(df1)
        df2_len = len(df2)
        
        if df1_len < df2_len:
            raise ValueError(f"Expected {df1} to be larger than {df2}. {df1} has {original_len} rows and {df2} has {new_len} rows.")

        # Calculate difference
        removed_rows = df1_len - df2_len
        perc_removed = round((removed_rows / df1_len) * 100, 2)

        return f"Number of rows removed from DataFrame: {removed_rows}\nPercentage of rows removed: {perc_removed}\n"


    
    def rm_empty_rows(self, col_to_ignore=None):
        """
        Removes rows where all values are NaN.

        The method removes rows where all values are missing (NaN). The method can take one 
        optional parameter, that specifies if a specific column should be excluded from the
        check. This is helpful if there is a categorical column that is filled for each 
        observation in the DataFrame. After removing rows from the DataFrame that have all
        missing data, the method 'count_removed_rows()' is used to inform the user of changes 
        to the DataFrame. The DataFrame is updated in place, and the index is reset. 

        Parameters:
            col_to_ignore (str): A specific column to ignore when checking for missing
            data (optional, default=None).

        Raises:
            ValueError: If 'col_to_ignore' does not exist in 'self.df'.
            TypeError: If 'col_to_ignore' is not a string.

        Returns:
            self: The updated CleanerClass object.

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.rm_empty_rows(col_to_ignore='Level
                Number of rows removed from DataFrame: 10
                Percentage of rows removed: 10.50%

        """

        # Validation checks
        if col_to_ignore:
            if col_to_ignore not in self.df.columns:
                raise ValueError(f"{col_to_ignore}' does not exist in the DataFrame.")
            elif not isinstance(col_to_ignore, str):
                raise TypeError(f"'{col_to_ignore}' must be of type string.")
            else: 
                # Set up columns to check
                col_subset = [col for col in self.df.columns if col != col_to_ignore]
        else:
            col_subset = self.df.columns

        # Drop rows with all missing values and reset index
        no_nan_rows = self.df.dropna(how="all", subset=col_subset)
        no_nan_rows = no_nan_rows.reset_index(drop=True)

        # Tell user how many rows were removed
        print(self.count_removed_rows(self.df, no_nan_rows))

        # Update self.df inplace
        self.df = no_nan_rows
        
        return self

    def rm_zero_rows(self, col_to_ignore=None):

        """
        The method removes any rows where all values are zero.

        The method removes rows where all values are zero. The method can take one optional 
        parameter, that specifies if a specific column should be excluded from the check.
        This is helpful if there is a categorical column that is filled for each observation 
        in the DataFrame, or has a different meaning to numerical data in other columns. The 
        method creates a Boolean mask to filter the DataFrame, where the mask specifies is a
        row contains all zero values or not. After removing rows from the DataFrame that have 
        all zero data, the method 'count_removed_rows' is used to inform the user of changes to 
        the DataFrame. The DataFrame is updated in place, and the index is reset. 

        Parameters:
            col_to_ignore (str): A specific column to ignore when checking for all zero
            rows (optional). 

        Raises:
           ValueError: If 'col_to_ignore' does not exist in 'self.df'.
           TypeError: If 'col_to_ignore' is not a string.

        Returns:
            self: The updated CleanerClass object.

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.rm_empty_rows(col_to_ignore='Level')
                Number of rows removed from DataFrame: 5
                Percentage of rows removed: 5.00%

        """
        # Validation checks
        if col_to_ignore:
            if col_to_ignore not in self.df.columns:
                raise ValueError(f"{col_to_ignore}' does not exist in the DataFrame.")
            elif not isinstance(col_to_ignore, str):
                raise TypeError(f"'{col_to_ignore}' must be of type string.")
            else:
                temp_df = self.df.drop(col_to_ignore, axis=1)
        else:
            temp_df = self.df

        # Create a Boolean mask   
        mask = (temp_df !=0).any(axis=1)
        df_no_zeros = self.df[mask]
        df_new = df_no_zeros.reset_index(drop=True)

        # Print results 
        print(self.count_removed_rows(self.df, df_new))
        self.df = df_new

        return self



    def rm_unmatched_signs(self, col1, col2, col3, col4):

        """
        This method removes any rows in the DataFrame where the specified pairs of columns 
        do not have matching signs.

        The method checks the specified column pairs (col1, col3) and (col2, col4) in the
        DataFrame 'self.df'. It filters rows where the values in 'col1' and 'col3' have 
        opposite signs, or where the values in 'col2' and 'col4' have oppostie signs. Any 
        rows that satisfy this criteria are dropped from the DataFrame. The DataFrame
        'self.df' is updated in place and the index is reset. The method also prints the
        number of rows removed, using the 'count_removed_rows' method.

        Parameters:
            col1 (str): The name of the first column in the first pair.
            col2 (str): The name of the first column in the second pair.
            col3 (str): The name of the second column in the first pair.
            col4 (str): The name of the second column in the second pair.
        
        Returns:
            self: The updated CleanerClass object.

        Raises:
            ValueError: If any of the specified column names do not exist in the DataFrame. 

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.remove_unmatched_signs('T3', 'T3adjusted', 'T4', 'T4adjusted')
                Number of rows removed from DataFrame: `5
                Percentage of rows removed: 25.75%

        """

        # Check all specified columns exist
        for col in [col1, col2, col3, col4]:
            if col not in self.df.columns:
                raise ValueError(f"'{col}' not in 'self.df'.")

        # Filter df to remove unmatched rows
        df_filtered = self.df[~(((self.df[col1] > 0) & (self.df[col3] < 0)) |
                       ((self.df[col1] < 0) & (self.df[col3] > 0)) |
                       ((self.df[col2] > 0) & (self.df[col4] < 0)) |
                       ((self.df[col2] < 0) & (self.df[col4] > 0)))]

        print(self.count_removed_rows(self.df, df_filtered))
        self.df = df_filtered.reset_index(drop=True)

        return self


    def replace_missing_values(self, group, cols):

        """
        The method replaces any missing values in the specified 'cols' with the average
        values for their specific 'group'.

        The method loops through the columns in 'cols' and calculates the column mean, 
        'col_mean', after grouping by the specified 'group'. This ensures the calculated 
        means are group specific, rather than column means, reducing potential bias. The 
        means are imputed in place, so that 'self.df' contains the imputed values. 

        Parameters:
            group (str): The specified column to group by.
            cols (list): A list of columns to impute mean values into. 

        Raises:
            TypeError: If 'group' is not a string, or 'cols' is not a list.
            ValueError: If 'group' does not exist in 'self.df'.
            ValueError: If all columns in 'cols' do not exist in 'self.df'.

        Returns:
            self: The updated CleanerClass object.

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.remove_unmatched_signs('Level', ['T3', 'T4'])
                Missing values in columns Length and Width were replaced by the average values 
                for their specific level.

        """

        # Validation checks
        if not (isinstance(group, str) or isinstance(cols, list)):
            raise TypeError(f"'{group}' must be a string, and '{cols}' must be a list.")

        if group not in self.df.columns:
            raise ValueError(f"'{group}' does not exist in 'self.df'.")

        for col in cols:
            if col not in self.df.columns:
                raise ValueError(f"'{col}' not in 'self.df'.")

        # Compute means at group and column level
        for col in cols:
            col_mean = self.df.groupby(group)[col].transform('mean')
            self.df[col] = self.df[col].fillna(col_mean)

        # Print results to screen
        print(f"Missing values in columns {[cols[0]]} and {[cols[1]]} were replaced by the average values for their specific level.")
        return self



    def diy_describe(self):

        """
        The method generates a DataFrame of summary statistics for 'self.df'.

        This method computes descriptive statistics for 'self.df'. This includes:
            - Aggregates: count, mean, standard deviation, minimum, maximum, and variance.
            These are calculated using the Pandas DataFrame method '.agg'. 
            - Quantiles: 25th, 50th (median), and 75th percentiles, calculated using the 
            Pandas DataFrame method '.quantile'.
            - IQR (interquartile range): The difference between the 7th and 25th percentile, 
            extracting the percentiles from the quantiles df using the '.loc' method. 
            - Skewness: A measure of asymmetry in the distribution of the values. This 
            is calculated using the Pandas DataFrame '.skew' method.
            - Range: The difference between the maximum and minimum values. Calculated 
            using the Pandas DataFrame '.min' and '.max' methods.
            - Missingness: The count of missing values per column. Calculated using the 
            Pandas DataFrame method '.isna'.

        Parameters:
            None.

        Raises:
            TypeError: If 'self.df' is not a Pandas DataFrame or if it contains non-numeric columns.
            
        Returns:
            joined_descriptors (pd.DataFrame): A DataFrame containing the calculated 
            descriptive statistics.

        Example:
            >>> cleaner = CleanerClass(df)
            >>> cleaner.diy_describe()

        """

        # Validation checks
        if not isinstance(self.df, pd.DataFrame):
            raise TypeError(f"'{self.df}' must be a Pandas DataFrame.")

        if not self.df.select_dtypes(include=['number']).shape[1] == self.df.shape[1]:
            raise TypeError(f"All columns in 'self.df' must be numeric data types.")
            
        # Calculate statistics
        aggregates = self.df.agg(['count', 'mean', 'std', 'min', 'max', 'var'])
        quantiles = self.df.quantile([0.25, 0.5, 0.75])
        iqr = quantiles.loc[0.75] - quantiles.loc[0.25]
        skew = self.df.skew()
        missingness = self.df.isna().sum()
        d_range = self.df.max() - self.df.min()

        # Convert to DataFrame
        iqr_df = iqr.to_frame().T
        skew_df = skew.to_frame().T
        missingness_df = missingness.to_frame().T
        range_df = d_range.to_frame().T

        # Rename indices
        iqr_df.index = ['IQR']
        skew_df.index = ['skewness']
        missingness_df.index = ['missing_values']
        range_df.index = ['range']

        # Rename indices
        joined_descriptors = pd.concat([aggregates, quantiles, range_df, iqr_df, skew_df, missingness_df])

        return joined_descriptors

    def rm_duplicates(self):

        """ 
        The method checks for and removes duplicates from the DataFrame.

        This method identifies duplicate rows in the 'self.df' DataFrame using the 
        'pandas.DataFrame.duplicated()' method.It then removes these duplicates using the 
        'pandas.DataFrame.drop_duplicates()' method, keeping the first occurrence of each row 
        only. 
        After the duplicate rows are removed the DataFrame's index is reset. If any duplicate
        rows were found, they are printed before being removed.

        Parameters:
            None.

        Raises:
            TypeError: If 'self.df' is not a Pandas DataFrame.

        Returns:
            self: The updated CleanerClass object.

        Example:
            >>> cleaner = CleanerClass(df)
            >>> df__no_duplicates = cleaner.rm_duplicates()
            >>> print(df_no_duplicates)
            The following duplicate rows were found and removed:
                col1 col2
            10     1    2
            The resulting DataFrame has 100 rows.

        """

        # Validation checks
        if not isinstance(self.df, pd.DataFrame):
            raise TypeError(f"'self.df' must be a Pandas DataFrame.")

        # Create a DataFrame that contains any duplicated rows
        duplicates = self.df[self.df.duplicated()]

        if len(duplicates) > 0:
            print("The following duplicate rows were found and removed:")
            print(duplicates)
            self.df.drop_duplicates(inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            print(f"The resulting DataFrame has {len(self.df)} rows.")
            return self
            
        elif len(duplicates) == 0:
            print("There are no duplicates within the DataFrame.")
            return self
            




#####################################################################################################
#####################################################################################################
#####################################################################################################
  
class TimeAndMemory:

    """This class implements functions that investigate the time and memory usage of algorithms.

    Attributes
    ---------
    results (dict): A dictionary to store the results of time and memory investigations.
    residuals (dict): A dictionary to store the residuals between a scaled chart and the 
    measured values.
    self.results (dict): A dictionary to store the results from running an investigation
    into time and memory usage. 
    """

    def __init__(self):
        """Initialise the TimeAndMemory with an empty results dictionary."""
        self.results = {}
        self.residuals = {}

        # Hard code results for use in submission
        self.results['mat_mult'] = pd.DataFrame({
            'Size': [15.0, 30.0, 45.0, 60.0, 75.0, 90.0, 105.0, 120.0, 135.0, 150.0],
            'Time (s)': [0.007217, 0.079013, 0.262462, 0.661467, 1.452451, 2.369175, 3.473095, 5.244003, 7.414388, 10.134657],
            'Memory (bytes)': [69632.0, 77824.0, 118784.0, 147456.0, 200704.0, 241664.0, 430080.0, 483328.0, 544768.0, 610304.0]
})

        self.results['mat_mult_np'] = pd.DataFrame({
            'Size': [500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0],
            'Time (s)': [0.030703, 0.121913, 0.309546, 0.597226, 0.994957, 1.622734, 2.379991, 3.268138, 4.443916, 5.982008],
            'Memory (bytes)': [2097152.0, 5853184.0, 8491008.0, 9031680.0, 10604544.0, 12177408.0, 13692928.0, 15065088.0, 16896000.0, 18468864.0]
})
        
        self.results['sort_ints'] = pd.DataFrame({
            'Size': [400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000],
            'Time (s)': [0.082925, 0.200214, 0.451068, 0.997305, 1.469594, 3.735391, 4.827899, 6.239969, 8.044682, 9.797529],
            'Memory (bytes)': [40960, 40960, 40960, 40960, 40960, 40960, 57344, 57344, 57344, 77824]
        })
        
        self.results['substring_inv'] = pd.DataFrame({
            'Size': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
            'Time (s)': [0.001513, 0.002078, 0.003120, 0.004072, 0.005971, 0.007802, 0.008427, 0.009420, 0.010666, 0.011602],
            'Memory (bytes)': [163840, 299008, 413696, 528384, 638976, 733184, 901120, 995328, 1175552, 1269760]
        })
        
        self.results['python_find_inv'] = pd.DataFrame({
            'Size': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
            'Time (s)': [0.002591, 0.002223, 0.004204, 0.006453, 0.004950, 0.005067, 0.009603, 0.009444, 0.007722, 0.008916],
            'Memory (bytes)': [163840, 307200, 425984, 532480, 679936, 798720, 888832, 999424, 1142784, 1282048]
        })
     

    """Methods defined here:"""

    def mat_mult_np(self, size):

        """
        The method multiplies two randomly generated matrices of size 'size x size', using the
        NumPy method '.dot()'.

        The method generates two matrices:
        - 'intA': A matrix containing integer values, randomly generated in the range [-500, 50000].
        - 'fltA': A matrix containing floating-point values, randomly generated in the range [0, 1].
        The two matrices are then multiplied together, using NumPys '.dot()' method. The matrices 
        'intA', 'fltA', and 'result' are deleted after they are created to reduce memory being used
        and improve accuracy of future investigations. 

        Parameters: 
            size (int): An integer specifying the size of an n x n matrix to be multiplied.

        Raises:
            TypeError: If 'size' is not an integer. 

        Returns:
            None: The method does not return anything, as matrix multiplication is done as part 
            of wider research into algorithm efficiency.

        Example:
            >>> tam = TimeAndMemory()
            >>> tam.mat_mult_np(10)
            # This will multiply two randomly generated 10 x 10 matrices.
        """
        # Validation checks
        if not isinstance(size, int):
            raise TypeError(f"'{int}' must be an integer.")

        # Generate matrices
        intA = np.random.randint(-500, 50000, (size, size))
        fltA = np.random.rand(size, size)
        
        result = np.dot(intA, fltA)

        # Delete matrices to improve memory reliability
        del intA, fltA, result
   

    def mat_mult(self, size):

        """
        The method multiplies two matrices using nested for loops. 

        The method generates two matrices:
        - 'intA': A matrix containing integer values, randomly generated in the range [-500, 50000].
        - 'fltA': A matrix containing floating-point values, randomly generated in the range [0, 1].
        It then initialises a results matrix of size 'size x size' with zero-values. 

        The resulting matrix is computed by using three nested for loops. The outer loop iterates
        over the rows of the result matrix, the middle loop iterates over the colunms of the result 
        matrix, and the inner loop computes the product of corresponding elements from 'intA' and 
        'fltA'. The matrices 'intA', 'fltA', and 'result' are deleted after they are created to 
        reduce memory being used and improve accuracy of future investigations. 

        Parameters: 
            size (int): An integer specifying the size of an n x n matrix to be multiplied.

        Returns:
            None: The method does not return anything, as matrix multiplication is done as part
            of wider research into algorithm efficiency.

        Example:
            >>> tam = TimeAndMemory()
            >>> tam.mat_mult(10)
            # This will multiply two randomly generated 10 x 10 matrices.
        """
        # Generate matrices
        intA = np.random.randint(-500, 50000, (size, size))
        fltA = np.random.rand(size, size)

        # Initialise the result matrix
        result = np.zeros((size, size))

        # Use nested loops for multiplication
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    result[i][j] += intA[j][k] * fltA[k][j]

        # Delete matrices to improve memory reliability
        del intA, fltA, result
      
        
    def sort_ints(self, length):

        """
        The method implements an inefficient sorting algorithm (Selection Sort).

        Generates a NumPy array of random integers (range: 0-10,000) of the specified length. It sorts 
        the array in ascending order using Selection Sort. Selection Sort finds the smallest element 
        and moves it into its correct position iteratively. The sorted array is not returned to reduce
        memory usage and allow better memory tracking during investigations.

        Parameters:
            length (int): An integer specifying the length of a NumPy array to be sorted. Must be a 
            positive integer.

        Returns:
            None: This method does not return a value. 

        Raises:
            TypeError: If 'length' is not an integer.
            ValueError: If 'length' is not <=0.

        Example
            >>> tam = TimeAndMemory()
            >>> tam.sort_ints(5)
            
        """

        # Data validation
        if not isinstance(length, int):
            raise TypeError(f"Expected 'length' to be an integer, but got {type(length).__name__}.")

        if length <= 0:
            raise ValueError("'length' must be a positive integer.")
        
        # Generates an array to be sorted
        values = np.random.randint(0, 10000, length)

        # Selection Sort
        for i in range(length - 1):  
            min_index = i  
            for j in range(i + 1, length):  
                if values[j] < values[min_index]:  
                    min_index = j  

            # Swap the found smallest element with the element at index i
            values[i], values[min_index] = values[min_index], values[i]

        # Delete values to reduce memory usage
        del values
        
        
    def random_str(self, length):
        """
        Generate a random string of a specified length.

        This method creates a random string composed of lowercase letters
        (a-z) and spaces. The string is generated by randomly selecting
        characters from the specified set, using Numpy's 'random.choice'
        method.

        Parameters:
            length (int): The desired length of the random string.

        Raises:
            TypeError: If 'length' is not an integer.

        Returns:
            random_str (str): A randomly generated string of the specified length.

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.random_str(10)
            'aqaow pbry' 
        """

        if not isinstance(length, int):
            raise TypeError(f"'{length}' must be an integer.")
            
        # Set possible characters
        characters = "abcdefghijklmnopqrstuvwxyz "

        # Choose from characters randomly
        random_str = ''.join(np.random.choice(list(characters), size = length))

        return random_str
        
    
    def substring_check(self, string, substring):
        """
        The method checks is a substring is present within a specified string.

        This method iterates through the main string to determine whether
        the specified substring exists within it. It compares slices of the
        string to the given substring.
    
        Parameters:
            string (str): The main string in which to search for the substring.
            substring (str): The substring to check for within the main string.

        Raises:
            ValueError: If string or substring are empty strings, or are not strings.

        Returns:
            bool: True if the substring is found in the main string, False otherwise.

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.substring_check("good morning", "good")
            True
            """

        # Validation checks
        if not isinstance(string, str) or not isinstance(substring, str):
            raise ValueError("Both 'string' and 'substring' must be of type 'str'.")

        if string == "" or substring == "":
            raise ValueError("Both 'string' and 'substring' must be non-empty.")

        # Handle case where substring is longer than string
        if len(substring) > len(string):
            return False

        # Loop through the main string, comparing slices of the same length as the substring
        for i in range(len(string) - len(substring) + 1):
            if string[i : i + len(substring)] == substring:
                return True
        return False

    def substring_inv(self, length):

        """
        The method generates a random string and substring, then checks for the substring in the 
        main string.

        This method creates a random string of a specified length and a random
        substring whose length is 10% of the main string's length. It then checks
        if the substring exists within the main string using the 'substring_check()'
        method.

        Parameters:
            length (int): The desired length of the main string.

        Raises:
            TypeError: If length is not an integer.

        Returns:
            None: This method does not return a value.

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.substring_inv(100)
            # Performs a check.
        """

        # Validation checks
        if not isinstance(length, int):
            raise TypeError(f"'{length}' must be an integer.")

        # Generate string and substring
        string = self.random_str(length)
        substring_length = int(length * 0.1)
        substring = self.random_str(substring_length)

        # Perform check
        self.substring_check(string, substring)


    def python_find_inv(self, length):
        """
        Generate a random string and substring, then check for the substring's in the main 
        string using Python's 'find()' method.

        This method creates a random string of a specified length and a random
        substring whose length is 10% of the main string's length. It then uses
        the 'find()' method to check if the substring exists within the main string.

        Parameters:
            length (int): The desired length of the main string.

        Returns:
            None: This method does not return a value.

        Raises:
            TypeError: If length is not an integer.

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.python_find_inv(100)
            # Performs a check.

        """

        # Validation checks
        if not isinstance(length, int):
            raise TypeError(f"'{length}' must be an integer.")

        # Generate string and substring
        string = self.random_str(length)
        substring_length = int(length * 0.1)
        substring = self.random_str(substring_length)

        # Perform search
        string.find(substring)


    def save_results(self, name, func_df):

        """This method saves the results of an investigation to the 'self.results' dictionary.

        This method adds or updates entries to the 'self.results' dictionary with the provided 
        DataFrame. The 'name' parameter specifies the key of the dictionary. The name must match the 
        name of an algorithm in the TimeAndMemory class.

        Parameters:
            name (str): The name of the method being investigated (e.g. 'mat_mult')
            func_df (DataFrame): The results of the investigation to be stored.

        Returns:
            None: This method does not return a value. It updates the 'self.results' dictionary in place. 

        Raises:
            ValueError: If 'name' is not a recognised method name.

        Example:
            >>> tam = TimeAndMemory()
            >>> tam.results_df
        """

        # Update self.results
        if name in {'mat_mult', 'mat_mult_np', 'sort_ints', 'substring_inv', 'python_find_inv'}:
            self.results[name] = func_df
        else:
            ValueError('Name is not recognised.')



    def investigate(self, function, name, step_size = 10, submission=False):

        """This method gathers utility information of a given function by measuring its performance 
        on difference sized inputs, or uses hardcoded results if specified. 

        This method measures time taken and memory used by a specified function. It captures these 
        variables for varying sized inputs, which may be a matrix, list, or string size depending on 
        the function called. It uses garbage collection to clear memory usage before any function is 
        called. The method loops through different input sizes based on the parameter 'step_size'.
        A for loop is used to iterate through the different sized input parameters for the specified 
        function. The results are stored in a Pandas DataFrame in the 'self.results' attribute for 
        future analysis. If the method has the 'submission' parameter set to True, pre-recorded 
        results are returned, and new measurements are not taken. The pre-recorded results are 
        results that were run in a clean environment, rather than being run after consecutive calls to
        the 'investigate' method. This makes them reliable and valuable for analysis. 

        Parameters:
            function (callable): The specific function that is being investigated.
            name (str): The name that results will be saved under, within the 'self.results' 
            dictionary. 
            step_size (int, optional): The quantity to increase size by. Default is 10. 
            submission (bool, optional): If True, previously hardcoded results are used. Default is 
            False.  

        Returns:
            func_df (pd.DataFrame): A DataFrame containing the input sizes, time, and memory 
            measurements, or hardcoded results if specified. 

        Example:
            >>> tam = TimeAndMemory()
            >>> def dummy_function(size):
            ...     return [i**2 for i in range(size)]
            >>> tam.investigate(dummy_function, name='dummy_func', step_size=50)
            >>> tam.results['dummy_func']
               Size   Time (s)  Memory (bytes)
            0   50.0  0.002341         65536.0
            1  100.0  0.004872         69632.0
            2  150.0  0.007189         73728.0
            3  200.0  0.009964         77824.0
            4  250.0  0.013286         81920.0
            5  300.0  0.017234         86016.0
            6  350.0  0.021798         90112.0
            7  400.0  0.026989         94208.0
            8  450.0  0.032806         98304.0
            9  500.0  0.039250        102400.0

        """

        # Check for a live run or if pre-saved results should be used
        if submission:
            # Check if hard-coded results exist
            if name in self.results:
                return self.results[name]
            else:
                raise ValueError(f"No hardcoded results found for '{name}'.")

        # If submission is set to False, implement investigate method

        # Set seed for reproducibility
        np.random.seed(1303)
        
        # Initialise arrays for results
        resTime = np.zeros(10)
        resSpace = np.zeros(10)
        var_size = np.zeros(10)

        # Clear memory
        gc.collect()

        # Capture base ram
        process = psutil.Process(os.getpid())
        baseRam = process.memory_info().rss 

        # Disable garbage collection, and capture measurements
        gc.disable()
        for i in range(1, 11):
            size = i * step_size
            var_size[i - 1] = size

            start = time.time()
            function(size)
            end = time.time()

            # Capture memory after function call
            ram = process.memory_info().rss  
            resTime[i - 1] = end - start
            resSpace[i - 1] = ram - baseRam  

        # Re-enable garbage collection, and force clear
        gc.enable()
        gc.collect()

        # Store results in DataFrame
        func_df = pd.DataFrame({
            'Size': var_size,
            'Time (s)': resTime,
            'Memory (bytes)': resSpace
        })

        self.save_results(name, func_df)
        return func_df


    def calc_sf(self, name, relationship, var_type='time'):

        """The method calculates a scaling factor for a given variable based on its relationship to 
        the dependent variable. 

        This method uses results from the 'investigate()' method to calculate a scaling factor, which 
        serves as a constant to adjust a theoretical relationship (e.g. cubic, quadratic, or linear)
        so that it can be compared against measured data points. The scaling factor is calculated 
        by taking the difference between consecutive input sizes and their corresponding
        measured values.  

        For each pair of consecutive data points, the scaling factor is calculated using 
        the formula:
        scaling_factor = measured_value2 / ((size2 / size1) ** exponent * measured_value1)

        Where:
        -'size1' and 'size2' represent the consecutive input sizes.
        - 'var1' and 'var2' correspond to the measured time or memory data for those input sizes.
        - 'exponent' is determined by the specified 'relationship'.

        The method skips iterations where division by zero occurs or where consecutive 
        measurements are identical. The average of all valid scaling factors is then returned.

        Parameters:
            name (str): The name of a key from the 'self.results' dictionary.
            relationship (str): The relationship being used to scale a variable by. 
            var_type (str): The type of investigation being conducted (e.g. 'time' or 'memory')

        Returns:
            avg_scale_factor (float): The calculated average scale factor.

        Raises:
            ValueError: If 'name' is not a key in the 'self.results' dictionary.
            ValueError: If 'var_type' is not 'time' or 'memory'
            ValueError: If 'relationship' is not 'cubic', 'quadratic' or 'linear'.

        Example:
            >>> tam = TimeAndMemory()
            >>> tam.results['example_func'] = pd.DataFrame({
            ...     'Size': [10, 20, 30, 40],
            ...     'Time (s)': [0.5, 2.0, 4.5, 8.0],
            ...     'Memory (bytes)': [1024, 2048, 3072, 4096]
            ... })
            >>> avg_scale_factor = tam.calc_sf(name='example_func', relationship='quadratic', 
            var_type='time')
                Number of values used to calculate scaling factor: 7
                The scaling factor used is 0.983781

        """

        # Validation checks
        if name in self.results:
            results_df = self.results[name]
        else:
            raise ValueError(f"Results for '{name}' have not been generated")

        if var_type == 'time':
            variable = pd.Series(results_df['Time (s)'])
        elif var_type == 'memory':
            variable = pd.Series(results_df['Memory (bytes)'])
        else:
           raise ValueError("Var_type must be either 'time' or 'memory'.")

        size = pd.Series(results_df['Size'])

        # Set exponent value based on inputs
        if relationship == 'cubic':
            exp = 3
        elif relationship == 'quadratic':
            exp = 2
        elif relationship == 'linear':
            exp = 1
        else:
            raise ValueError("Relationship must be either cubic, quadratic, or linear.")

        scale_factors = []

        # Perform scale factor calculations
        for i in range(1, len(size)):
            size1 = size.iloc[i-1]
            size2 = size.iloc[i]
            var1 = variable.iloc[i-1]
            var2 = variable.iloc[i]

            # Handle division by zero - skip
            if size1 == 0 or var1 == 0:
                print("Division by zero error, skipping this iteration")
                continue
            if var1 == var2:
                print("Consecutive measurements are identical, skipping this iteration")
                continue
    
            c = var2 / ((size2/size1) ** exp * var1)

            # Add scale factor to list
            scale_factors.append(c)

        print(f"Number of values used to calculate scaling factor: {len(scale_factors)}")
        avg_scale_factor = np.mean(scale_factors)
        print(f"The scaling factor used is: {avg_scale_factor}")

        return avg_scale_factor


    def normalise(self, var1, var2):

        """This method normalises two variables to a range between 0 and 1. 

        This method takes two variables (arrays) and normalises their values so that the maximum in 
        each variable becomes 1. Normalisation is performed on each element of the array, dividing 
        each value by the maximum value from its array. This is to aid interpretability of results,
        particularly helpful for comparing trends rather than absolute figures.

        Parameters: 
            var1 (array): The first array to be normalised.
            var2 (array): The second array to be normalised. 

        Raises:
            ValueError: If 'var1' or 'var2' are non empty, or have a max value of 0.

        Returns:
            tuple: A tuple containing the two normalised variables (var1, var2), each with a maximum
            value of 1. 

        Example:
            >>> tam = TimeAndMemory()
            >>> var1 = [1, 2, 3, 4]
            >>> var2 = [10, 20, 30, 40]
            >>> norm_var1, norm_var2 = tam.normalise(var1, var2)
            >>> print(norm_var1)  
            [0.25, 0.5, 0.75, 1.0]
            >>> print(norm_var2)  
            [0.25, 0.5, 0.75, 1.0]
        """

        # Validation checks
        if max(var1) == 0 or max(var2) == 0:
            raise ValueError("Cannot normalise an array with a maximum value of 0.")

        if len(var1) == 0 or len(var2) == 0:
            raise ValueError("Input arrays must not be empty.")

        # Normalise
        var1 = np.array(var1) / max(var1)
        var2 = np.array(var2) / max(var2)

        return var1, var2
            

    def plot_specification(self, x, y, s_comp, title, xlabel, ylabel, label='Investigation', s_comp_label='comparison'):

        """This method plots a line graph, using the specification provided.

        This method creates a line graph with two data lines. The first represents the 
        main measured data and the other a scaled graph for comparison. It gives the chart 
        a title, axis labels, and a legend to identify the plotted lines.

    Parameters:
        x (array or list): The data for the x-axis.
        y (array or list): The data for the y-axis corresponding to the measured data.
        s_comp (array-like): The data for the y-axis corresponding to the scaled theoretical graph.
        title (str): The title of the graph.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        label (str, optional): The label for the first line chart in the legend. Default is 
        'Investigation'.
        s_comp_label (str, optional): The label for the scaled line chart series in the legend. 
        Default is 'comparison'.

        Returns:
            None.

        Example:
            Example:
                >>> x = [1, 2, 3, 4, 5]
                >>> y = [2, 4, 6, 8, 10]
                >>> s_comp = [1.5, 3, 4.5, 6, 7.5]
                >>> title = "Example Plot"
                >>> xlabel = "X-axis"
                >>> ylabel = "Y-axis"
                >>> demo = CleanerClass()
                >>> demo.plot_specification(x, y, s_comp, title, xlabel, ylabel)
        """

        plt.figure(figsize=(5, 3.5)) 
        plt.plot(x, y, label=label)
        plt.plot(x, s_comp, label=s_comp_label, color='red')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.show()


    def extract_vars(self, name):

        """The method extracts size, time and memory data from the 'self.results' dictionary.

        Parameters:
            name (str): The key to look up in the 'self.results' dictionary.

        Returns:
            size, resTime, resSpace (tuple): Tuples containing arrays size, resTime, resSpace

        Raises:
            KeyError: If 'name' does not exist as a key in the 'self.results' dictionary. 

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.results = {
                    "example_func": pd.DataFrame({
                        "Size": [1000, 2000, 3000],
                        "Time (s)": [0.5, 1.2, 2.0],
                        "Memory (bytes)": [5000, 12000, 20000]
                    })
                }
            >>> size, resTime, resSpace = demo.extract_vars("example_func")
            >>> print(size)      # Output: [1000, 2000, 3000]
            >>> print(resTime)   # Output: [0.5, 1.2, 2.0]
            >>> print(resSpace)  # Output: [5000, 12000, 20000]
        """

        # Validation checks
        if name not in self.results:
            raise KeyError(f"'{name}' not found in 'self.results'. This suggests an invalid 'name' or the results have not been generated.")

        # Extract variables from results
        size = self.results[name]['Size']
        resTime = self.results[name]['Time (s)']
        resSpace = self.results[name]['Memory (bytes)']
      
        return size, resTime, resSpace    
            
    
    def plots(self, name, variable, exp_rel):

        """This method plots results from an investigation against their expected trend.

        Plots the results of an investigation, comparing observed and expected trends 
        for either time or memory usage. This method calculates residuals using the method 
        'calc_residuals', normalises the data using 'normalise', and computes a scaling factor using 
        'calc_sf' to enable comparison with a scaled polynomial model.

        Parameters:
            name (str): The name of the algorithm being analysed.
            variable (str): Specifies whether to analyse 'time' or 'memory' results.
                - Must be set to either 'time' or 'memory'.
            exp_rel (str): The expected relationship between input size and the variable being 
                plotted. Must be one of the following:
                - 'cubic': Assumes a cubic polynomial trend.
                - 'quadratic': Assumes a quadratic polynomial trend.
                - 'linear': Assumes a linear polynomial trend.

        Raises:
            ValueError: If 'variable' is not set to 'time' or 'memory', or if 'exp_rel' is not 
                one of 'cubic', 'quadratic', or 'linear'.

        Returns:
            None: Outputs plots directly, but prints residuals and scaling factor information for 
            the selected variable.

        Example:
            To plot normalised time measurements against a quadratic model:
            >>> demo = TimeAndMemory()
            >>> demo.plots(name="investigation1", variable="time", exp_rel="quadratic")
        """

        # Extract variables
        size, resTime, resSpace = self.extract_vars(name)

        size = pd.Series(size)
        time = pd.Series(resTime)
        resSpace = pd.Series(resSpace)

        # Set exponent
        if exp_rel == 'cubic':
            exp = 3
        elif exp_rel == 'quadratic':
            exp = 2
        elif exp_rel == 'linear':
            exp = 1
        else:
            raise ValueError("Expected relationship must be 'cubic', 'quadratic', or 'linear'.")

        if variable == 'time':

            # Caclulate scaling factor, and comparison line
            sf = self.calc_sf(name, exp_rel, var_type=variable)
            comp = sf * (size ** exp)
            comp, resTime = self.normalise(comp, resTime)

            # Calculate residuals
            residuals = self.calc_residuals(resTime, comp)
            self.residuals[(name, variable)] = residuals
            print(f"Time residuals: {residuals}")

            # Plot
            self.plot_specification(
                size, resTime, comp, 
                f'Time taken for {name}', 
                xlabel='Matrix size (n)', 
                ylabel='Normalised time (0, 1)', 
                label='Measured time', 
                s_comp_label=f'Scaled {exp_rel} polynomial')

        elif variable == 'memory':

            # Caclulate scaling factor, and comparison line
            sf = self.calc_sf(name, exp_rel, var_type=variable)
            comp = sf * (size ** exp)
            comp, resSpace = self.normalise(comp, resSpace)
            
            # Calculate residuals
            residuals = self.calc_residuals(resSpace, comp)
            self.residuals[(name, variable)] = residuals
            print(f"Memory residuals: {residuals}")

            # Plot
            self.plot_specification(
                size, resSpace, comp,
                f'Space used for {name}', 
                xlabel='Matrix size (n)', 
                ylabel='Normalised memory (0, 1)', 
                label='Measured memory', 
                s_comp_label=f'Scaled {exp_rel} polynomial')

        else:
            raise ValueError("Variable must either be set to 'time' or 'memory'.")


    def plot_memory_bar(self, name, name2=None):
        """
        This method creates a bar chart to visualise memory usage of one or two algorithms.

        This method genertes a bar chart to display the memory usage of an algorithm (given by 'name'
        ). If a second algorithm, 'name2', is given the memory used by each are plotted side by side
        for comparison. 

        Parameters:
            name (str): The name of the algorithm whose memory usage is being plotted.
            name2 (str, optional): The name of of a second algorithm for comparison. If None,
            only the memory usage of the first algorithm is plotted.

        Raises:
            KeyError: If name or name2 not in 'self.results'.

        Returns:
            None: Displays the bar chart.

        Example:
            To plot memory usage of an investigation:
            >>> demo = TimeAndMemory()
            >>> demo.plots(name="investigation1")

        """

        # Validation checks
        if name not in self.results:
            raise KeyError(f"'{name}' not found in 'self.results'. This suggests an invalid 'name' or the results have not been generated.")

        if name2 and name2 not in self.results:
            raise KeyError(f"'{name2}' not found in 'self.results'. This suggests an invalid 'name2' or the results have not been generated.")

        # Extract size and memory usage
        size, resTime, resSpace = self.extract_vars(name)
        
        size = pd.Series(size)
        resSpace = pd.Series(resSpace)

        # Set formatting
        bar_width = 200  
        positions = size - (bar_width / 2) 

        # Create bar chart
        plt.bar(positions, resSpace, width=bar_width, color='#3776ab', label=name)

        if name2 is not None:
            size2, resTime2, resSpace2 = self.extract_vars(name2)
            resSpace2 = pd.Series(resSpace2)
            plt.bar(positions + bar_width, resSpace2, width=bar_width, color='#ffa500', label=name2)

        # Labels and title 
        plt.xlabel('Input Size (n)')
        plt.ylabel('Memory Usage (bytes)')
        plt.title(f'Memory Usage for {name} {f'and {name2}' if name2 else ''}')
        plt.xticks(size)
        plt.legend()

        # Show plot
        plt.show()
    
    def log_plot(self, name, variable):

        """
        This method creates a log-log plot to analyse the relationship between a variable and the 
        size of an input to a function, and fits a line to the data. 

        The method extracts size, time, or memory data from 'self.results' using the 'extract_vars' 
        method. It takes logs of either time or memory data, and size, depending on the specifed 
        'variable', and plots the results. It then fits a straight line graph using linear regression 
        using the NumPy 'np.polyfit'. This straight line is plotted as a best-fit line on the plot, 
        highlighing the slope of the straight line in the legend. 

        Parameters:
            name (str): The key to look up in the 'self.results' dictionary.
            variable (str): The variable to plot against size. Must be either 'time' or 'memory'.

        Raises:
            KeyError: If 'name' is not found in 'self.results'.
            ValueError: If 'variable' is not 'time' or 'memory'.
            
        Returns:
            None. A log plot is displayed but nothing is returned. 

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.results['investigation1'] = pd.DataFrame({
            ...     'Size': [100, 200, 300, 400, 500],
            ...     'Time (s)': [0.1, 0.4, 0.9, 1.6, 2.5],
            ...     'Memory (bytes)': [10240, 20480, 30720, 40960, 51200]
            ... })
            >>> demo.log_plot(name='investigation1', variable='memory')
  
        """

        # Validation checks
        if name not in self.results:
            raise KeyError(f"'{name}' not in 'self.results'.")

        if variable != 'time' and variable != 'memory':
            raise ValueError(f"'{variable}' must be either 'time' or 'memory'.")
        
        # Extract variables
        size, resTime, resSpace = self.extract_vars(name)

        # Fit log models
        if variable == 'time':
            log_var = np.log(resTime)
        elif variable == 'memory':
            log_var = np.log(resSpace)

        log_size = np.log(size)

        # Find coefficients
        coefficients = np.polyfit(log_size, log_var, 1)

        self.plot_specification(log_size, log_var, 
                                log_size*coefficients[0] + coefficients[1],
                                f'Log({variable}) and log(size)', 
                                xlabel='log(size)', 
                                ylabel=f'log({variable})', 
                                label='Measured data', 
                                s_comp_label=f'Best fit with slope: {round(coefficients[0], 2)}')


    def calc_residuals(self, measured_vals, scaled_vals):

        """The method calculates residuals by substracting 'scaled_vals' from 'measured_vals'.

        Parameters:
            measured_vals (array): An array of measured data points.
            scaled_vals (array): An array of scaled data points.

        Returns:
            residuals (np.ndarray): An array of residuals.

        Raises:
            TypeError: If 'measured_vals' or 'scaled_vals' are not iterable.
            ValueError: If 'measured_vals' or 'scaled_vals' are empty.

        Example:
            >>> measured = [5, 10, 15]
            >>> scaled = [4, 9, 14]
            >>> tam = TimeAndMemory()
            >>> tam.calc_residuals(measured, scaled)
            array([1, 1, 1])

        """

        # Validation checks
        if not isinstance(measured_vals, (list, np.ndarray)) or not isinstance(scaled_vals, (list, np.ndarray)):
            raise TypeError(f"Both 'measured_vals' and 'scaled_vals' must be lists or numpy arrays.")
            
        if len(measured_vals) == 0 or len(scaled_vals) == 0:
            raise ValueError("Input arrays must not be empty.")
        
        # Set given data to NumPy arrays
        measured_vals = np.array(measured_vals)
        scaled_vals = np.array(scaled_vals)

        # Calculate residuals
        residuals = measured_vals - scaled_vals

        return residuals

    def plot_residuals(self, variable, methods=None):

        """The method plots residuals for one or two methods related to a given variable.

        This method plots the residuals from a plot of some measured variable (either time
        or memory) and a scaled polynomial graph. If multiple methods are specified their residuals
        are plotted on the same chart for comparison. The method must be called after the 'plot' 
        method has been used, as it draws on the residuals generated in this method.

        Parameters:
            variable (str): The variable for which residuals are being analysed and plotted.
            methods (list or str, optional): A single method (as a string) or multiple methods
            (as a list of strings) whose residuals are to be plotted. 

        Raises:
            ValueError: If no methods are provided.
            KeyError: If residuals for the specified method and variable are not found.

        Returns:
            None: The method shows a plot, but does not return a value.

        Example:
            >>> demo = TimeAndMemory()
            >>> demo.plot_residuals('time',  methods=['substring_inv', 'python_find_inv'])
            # Plots residuals for 'method1' and variable 'input_size'
        
        """

        # Validation checks
        if methods is None:
            raise ValueError("Please provide at least one method to plot residuals.")

        if isinstance(methods, str):
            methods = [methods]

        if len(methods) == 1:
        # Original functionality for a single method
            method = methods[0]
            if (method, variable) in self.residuals:
                residuals = self.residuals[(method, variable)]
            else:
                raise KeyError(f"Residuals not found for method '{method}' and variable '{variable}'")

            # Set indices for the residuals and zero reference line
            x = np.arange(len(residuals))  
            s_comp = np.zeros_like(x)  

            # Use plot_specification to create the plot
            self.plot_specification(
                x, residuals, s_comp,
                title=f'Residuals for {name} ({variable})',
                xlabel='Index of Residual',
                ylabel='Residuals',
                label='Residuals',
                s_comp_label='Zero Reference Line'
            )
            print(f"The mean residual is {np.mean(residuals)}")
        else:
            
            # Functionality for multiple methods
            plt.figure(figsize=(5, 3.5))
        
            for method in methods:
                if (method, variable) in self.residuals:
                    residuals = self.residuals[(method, variable)]
                else:
                    raise KeyError(f"Residuals not found for method '{method}' and variable '{variable}'")

                # Set indices for the residuals and zero reference line
                x = np.arange(len(residuals)) 
                plt.plot(x, residuals, label=f'Residuals for {method}')  

            # Add zero reference line
            plt.axhline(0, color='black', linestyle='--', label='Zero reference line')

            # Set up plot details
            plt.title(f'Residuals Comparison for {variable}', fontsize=14)
            plt.xlabel('Index of Residual')
            plt.ylabel('Residuals')
            plt.legend()
            plt.show()
            
