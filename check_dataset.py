import pandas as pd

df = pd.read_csv("data/processed/mimic_cxr_processed.csv")

print("=" * 60)
print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nFirst row:")
print(df.iloc[0])
