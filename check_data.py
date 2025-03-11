import pandas as pd

# Load the CSV file
df = pd.read_csv("spxl_data.csv")

print("\n===== First 5 Rows of Data =====")
print(df.head())

print("\n===== Data Types =====")
print(df.dtypes)

print("\n===== Column Names =====")
print(df.columns.tolist())

print("\n===== Missing Values =====")
print(df.isnull().sum())
