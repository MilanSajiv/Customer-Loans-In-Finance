import numpy as np
import scipy.stats as stats

class SkewTransform:
    def __init__(self, df):
        self.df = df    
    def identify_skewed_columns(self, threshold=2):
        numerical_columns = self.df.select_dtypes(include=[np.number]).columns
        skewness = self.df[numerical_columns].apply(lambda n: n.skew())
        skewed_columns = skewness[abs(skewness) > threshold].index.tolist()
        return skewed_columns
    def transform_log(self, threshold=2):
        skewed_columns = self.identify_skewed_columns(threshold)
        for column in skewed_columns: 
            self.df[column] = self.df[column].map(lambda i: np.log1p(i) if i > 0 else 0)
