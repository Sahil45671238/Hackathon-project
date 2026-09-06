import pandas as pd
from sqlalchemy import create_engine

# MySQL connection details yahan apne hisaab se daalo
user = "root"          # apna user
password = "45671238"  # apna password
host = "localhost"     # ya 127.0.0.1
database = "olist_db"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

import pandas as pd

files_and_tables = {
    "order_item_prepared.csv": "order_items_prepared",
    "order_payments_prepared.csv": "order_payments_prepared",
    "reviews_prepared.csv": "reviews_prepared",
    "customers.csv": "customers",
    "products_prepared.csv": "products_prepared",
    "seller_prepared.csv": "sellers_prepared",
    "geolocation_prepared.csv": "geolocation_prepared",
    "orders_prepared.csv": "orders_prepared",
}

for file, table in files_and_tables.items():
    df = pd.read_csv(file)
    df.to_sql(table, con=engine, if_exists="replace", index=False)
    print(f"{table} loaded")