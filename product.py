import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = r"products.csv"


df = pd.read_csv(file_path)

print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()

missing_percent = (missing / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": missing_percent.round(2)
})

print(missing_report[missing_report["Missing_Count"] > 0])

# print(df.dtypes)
# print(df.duplicated().sum())
num_cols = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")
# 3) Category ke NaN ko "unknown"
df["product_category_name"] = df["product_category_name"].fillna("unknown")

# 4) Export
df.to_csv("products_prepared.csv", index=False)
print("Saved: products_prepared.csv")
print(df.isna().sum())
