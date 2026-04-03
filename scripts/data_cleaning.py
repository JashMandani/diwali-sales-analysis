"""
data_cleaning.py
----------------
Loads the raw Diwali Sales CSV, cleans it, and saves a clean version.
Run this first before eda_analysis.py or generate_report.py.
"""

import pandas as pd
import os

# ── Paths ────────────────────────────────────────────────────────────────────
RAW_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'Diwali_Sales_Data.csv')
CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'Diwali_Sales_Clean.csv')


def load_raw(path: str) -> pd.DataFrame:
    """Load the raw CSV with latin-1 encoding."""
    df = pd.read_csv(path, encoding='latin1')
    print(f"✅ Loaded raw data: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps and return a clean DataFrame."""

    original_rows = len(df)

    # 1. Drop irrelevant columns
    df = df.drop(columns=['Status', 'unnamed1'], errors='ignore')
    print(f"  Dropped 'Status' and 'unnamed1' columns")

    # 2. Drop rows with missing Amount (only 12 rows)
    df = df.dropna(subset=['Amount'])
    dropped = original_rows - len(df)
    print(f"  Dropped {dropped} rows with missing Amount")

    # 3. Fix data types
    df['Amount']         = df['Amount'].astype(int)
    df['Marital_Status'] = df['Marital_Status'].astype(int)
    df['User_ID']        = df['User_ID'].astype(str)

    # 4. Map binary columns to readable labels
    df['Gender_Label']         = df['Gender'].map({'F': 'Female', 'M': 'Male'})
    df['Marital_Status_Label'] = df['Marital_Status'].map({0: 'Single', 1: 'Married'})

    # 5. Enforce age group ordering
    age_order = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']
    df['Age Group'] = pd.Categorical(df['Age Group'], categories=age_order, ordered=True)

    print(f"  Fixed dtypes and added readable label columns")
    print(f"\n✅ Clean dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def summarize(df: pd.DataFrame):
    """Print a quick summary of the clean data."""
    print("\n── Summary ──────────────────────────────────────")
    print(f"  Total Revenue  : ₹{df['Amount'].sum():,.0f}")
    print(f"  Total Orders   : {df['Orders'].sum():,}")
    print(f"  Unique Customers: {df['User_ID'].nunique():,}")
    print(f"  Unique Products : {df['Product_ID'].nunique():,}")
    print(f"  States covered  : {df['State'].nunique()}")
    print(f"  Zones           : {df['Zone'].nunique()}")
    print(f"  Product Cats    : {df['Product_Category'].nunique()}")
    print(f"  Occupations     : {df['Occupation'].nunique()}")
    print(f"\n  Null values after cleaning:\n{df.isnull().sum()[df.isnull().sum()>0]}")
    print("─────────────────────────────────────────────────\n")


def main():
    df_raw   = load_raw(RAW_PATH)
    df_clean = clean(df_raw)
    summarize(df_clean)
    df_clean.to_csv(CLEAN_PATH, index=False)
    print(f"✅ Clean data saved to: {CLEAN_PATH}")


if __name__ == '__main__':
    main()
