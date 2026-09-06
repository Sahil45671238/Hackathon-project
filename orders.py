import pandas as pd

# 1) Load
df = pd.read_csv("orders.csv")

# 2) Types: string + datetime

# print(df.dtypes())
string_cols = ["order_id", "customer_id", "order_status"]
for c in string_cols:
    if c in df.columns:
        df[c] = df[c].astype("string")

datetime_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for c in datetime_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce")

# 3) Missing flags
date_cols_for_flags = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

for col in date_cols_for_flags:
    if col in df.columns:
        df[f"{col}_is_missing"] = df[col].isna().astype(int)

if set(["order_purchase_timestamp", "order_delivered_customer_date"]).issubset(df.columns):
    df["delivery_time_days"] = (
        (df["order_delivered_customer_date"] - df["order_purchase_timestamp"])
        .dt.total_seconds() / (3600 * 24)
    )

if set(["order_delivered_customer_date", "order_estimated_delivery_date"]).issubset(df.columns):
    df["delivery_delay_days"] = (
        (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"])
        .dt.total_seconds() / (3600 * 24)
    )
    df["is_late"] = (df["delivery_delay_days"] > 0).astype("Int64")  # 0/1 with NaN allowed


df.to_csv("orders_prepared.csv", index=False)
print("Saved: orders_prepared.csv")