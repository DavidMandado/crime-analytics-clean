import pandas as pd

# ——— CONFIG ———
file_path = r"C:/Users/20232726/Desktop/me/datachallenge2_addressingcrime/Addressing-real-world-crime-and-security-problems-with-data-science/David's work folder/data/crime_fixed_data.csv"
date_col  = 'month'

# ——— LOAD DATA ———
df = pd.read_csv(file_path, parse_dates=[date_col])


# ——— PREPROCESSING ———
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
)

# ——— QUICK INSPECTION ———
print("=== df.info() ===")
print(df.info(), "\n")

print("=== df.head() ===")
print(df.head(), "\n")

print("=== Missing values per column ===")
print(df.isnull().sum(), "\n")

print("=== Descriptive statistics ===")
print(df.describe(include='all').T)
