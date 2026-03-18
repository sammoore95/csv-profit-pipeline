# Step 1: load CSV with pandas
import pandas as pd

sales_data = pd.read_csv("data/jobs.csv")


# Step 2: Inspect CSV data 
sales_data.info()
print(sales_data.columns)
print(sales_data.head(5))


# Step 3: Transform Data
sales_data["sales_profit"] = sales_data["sales_amount"] - sales_data["cost_amount"]

print(sales_data)