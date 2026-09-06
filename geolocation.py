import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = r"geolocation.csv"

df = pd.read_csv(file_path)

print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()

missing_percent = (missing / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": missing_percent.round(2)
})

print(missing_report[missing_report["Missing_Count"] > 0])

print(df.dtypes)

geo_prepared = df.drop_duplicates(
    subset=[
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ]
).reset_index(drop=True)

print("Original rows:", len(df))
print("After removing duplicates:", len(geo_prepared))


geo_prepared.to_csv("geolocation_prepared.csv", index=False)
print("Saved: geolocation_prepared.csv")