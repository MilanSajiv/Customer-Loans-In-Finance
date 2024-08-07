import pandas as pd
import matplotlib.pyplot as plt

class DataFrameInfo:  
    def __init__(self, df) -> None:
        self.df = df
    def describe(self):
        return self.df.describe()    
    def get_median(self, column=None):
        if column != None:
            print(self.df[column].median(numeric_only=True))
        else:
            print(self.df.median())
    def get_std(self, column=None):
        if column != None:
            print(self.df[column].std(numeric_only=True))
        else:
            print(self.df.std())
    def get_mean(self, column=None):
        if column != None:
            print(self.df[column].mean(numeric_only=True))
        else:
            print(self.df.mean())
    def shape(self):
        return self.df.shape
    def count_distinct_categories(self, column):
        if self.df[column].dtype == 'category':
            return self.df[column].value_counts() 
        else:
            print("This dtype is not a category dtype.\nMake sure to convert first.")
    def get_missing_values(self): 
        percent_missing = round(self.df.isnull().sum() * 100 / len(self.df), 2)
        missing_value_df = pd.DataFrame({'column_name': self.df.columns,
                                        'percent_missing': percent_missing})
        missing_value_df = missing_value_df.loc[missing_value_df["percent_missing"] != 0]
        return missing_value_df
        
class Plotter:
    def __init__(self, df):
        self.df = df
    def histogram(self, column, bins):
        plt.hist(self.df[column], bins=bins)
        plt.show()
