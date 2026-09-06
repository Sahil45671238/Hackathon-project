import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = r"order_items.csv"


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
print(df.duplicated().sum())

df.to_csv("order_item_prepared.csv", index=False)
print("Saved: order_item_prepared.csv")