import pandas as pd
from scipy import stats
from df_info import DataFrameInfo

class DataTransformation:
    def __init__(self, df):
        self.df = df
    def dates_conversion(self, date_column):
        self.df[date_column] = pd.to_datetime(self.df[date_column], format="%b-%Y")
        return self.df
    def convert_term_float(self, term_column):
        self.df[term_column] = self.df[term_column].str.extract('(\d+)', expand=False).astype(float)
        return self.df
    
    def convert_categorical(self, cat_column):
        self.df[cat_column] = self.df[cat_column].astype('category')
        return self.df
    
    def convert_cat_to_numerical(self, category_column):
        self.df[category_column] = self.df[category_column].factorize()[0]
        self.df[category_column] = self.df[category_column] + 1
        return self.df
    
    def convert_to_float(self, column):
        self.df[column] = self.df[column].astype(float)
        return self.df

    def drop_column(self, column):
        return self.df.drop(column, axis=1, inplace=True)
    
    def impute_columns(self, column, impute_type):
        if impute_type == "median":
            self.df[column].fillna(self.df[column].median(), inplace=True)
        elif impute_type == "mean":
            self.df[column].fillna(self.df[column].median(), inplace=True)
        else:
            print("Please enter a valid imputation method.\n Either median or mean.")
        return self.df