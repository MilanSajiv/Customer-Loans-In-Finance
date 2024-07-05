import pandas as pd
from transform import DataTransformation
from df_info import DataFrameInfo, Plotter
import missingno as msno
from skew import SkewTransform
import matplotlib.pyplot as plt

def load_csv(data_csv):
    df = pd.read_csv(data_csv)
    return df
data_csv = 'data.csv'
df = load_csv(data_csv)

transformer  = DataTransformation(df)
df_info = DataFrameInfo(df)
df_plot = Plotter(df)

msno.bar(df)

transformer.drop_column([ "mths_since_last_delinq", "mths_since_last_record", "next_payment_date", "mths_since_last_major_derog"])
df_plot.histogram('funded_amount', 20)

df["funded_amount"] = df["funded_amount"].fillna(df["loan_amount"])
term_mode = df["term"].mode().iloc[0]

df["term"].fillna(term_mode, inplace=True)
df = df.dropna(subset=['last_payment_date', 'last_credit_pull_date',
       'collections_12_mths_ex_med'])
df_info = DataFrameInfo(df)
df_plot = Plotter(df)

df_info.get_missing_values()

df_plot = Plotter(df)
df_plot.histogram('int_rate', 20)

skew_df = df['int_rate'].skew()
print(skew_df)

df['int_rate'].mean()
df["int_rate"] = df["int_rate"].fillna(df["int_rate"].mean())
df['int_rate'].head(50)

print(df.hist(figsize=(20,15)))

df[['loan_amount', 'funded_amount', 'funded_amount_inv', 'instalment', 'open_accounts', 'total_accounts','out_prncp','out_prncp_inv', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']].skew(numeric_only=False)

transformed_df1 = SkewTransform(df)
transformed_df = transformed_df1
transformed_df.transform_log()

skew_df = df.skew(numeric_only=True).to_frame().reset_index()
skew_df = skew_df.loc[abs(skew_df[0]) >= 0.5]
skew_df

df[['loan_amount', 'funded_amount', 'funded_amount_inv', 'instalment',
         'open_accounts', 'total_accounts', 'out_prncp', 'out_prncp_inv', 
        'total_payment', 'total_payment_inv', 'total_rec_prncp',
        'total_rec_int', 'last_payment_amount']].hist(figsize=(20,15))

df[['loan_amount', 'funded_amount', 'funded_amount_inv', 'instalment', 'open_accounts', 'total_accounts','out_prncp','out_prncp_inv', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']].skew(numeric_only=False)

columns = ['loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc', 'dti', 'delinq_2yrs', 'inq_last_6mths', 'open_accounts', 'total_accounts', 'out_prncp', 'out_prncp_inv', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee','last_payment_amount', 'collections_12_mths_ex_med', 'policy_code']

fig, axes = plt.subplots(nrows=8, ncols=3, figsize=(10, 40))
axes = axes.flatten()

for idx, column in enumerate(columns):
    df.boxplot(column=column, ax=axes[idx])
    axes[idx].set_title(column)

plt.tight_layout()
plt.show()

import pandas as pd
def remove_outliers_for_column(df, column, threshold=2):
    z_scores = (df[column] - df[column].mean()) / df[column].std()
    outliers = z_scores.abs() > threshold
    df_outliers = df[outliers]
    return df_outliers

df_outliers = remove_outliers_for_column(df, 'total_accounts')
df_outliers = remove_outliers_for_column(df, 'inq_last_6mths')

skew_df = df_outliers[["total_accounts", "inq_last_6mths"]].skew(numeric_only=True).to_frame().reset_index()
#skew_df = skew_df.loc[abs(skew_df[0]) >= 1]
skew_df

df['loan_status'].value_counts()

charged_off_loans = df[df['loan_status'] == 'Charged Off']
charged_off_percentage = (charged_off_loans.shape[0] / df.shape[0]) * 100
total_amount_paid_charged_off = charged_off_loans['total_payment'].sum()

print(f"Percentage of charged-off loans historically: {charged_off_percentage:.2f}%")
print(f"Total amount paid towards charged-off loans: £{total_amount_paid_charged_off:.2f}")

total_payments_made = (df["total_payment"].sum() /df["funded_amount"].sum()) * 100
total_payments_investor = (df["total_payment"].sum() /df["funded_amount_inv"].sum()) * 100
print(total_payments_made)
print(total_payments_investor)