import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = r"order_reviews.csv"


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

# Datetime conversion
df["review_creation_date"] = pd.to_datetime(df["review_creation_date"],
                                            errors="coerce")
df["review_answer_timestamp"] = pd.to_datetime(df["review_answer_timestamp"],
                                               errors="coerce")


# 4) Export cleaned reviews
df.to_csv("reviews_prepared.csv", index=False)
print("Saved: reviews_prepared.csv")
print(df.isna().sum())

