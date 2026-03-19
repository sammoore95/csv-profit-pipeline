# Load CSV with Pandas
from tabulate import tabulate
import pandas as pd

job_data = pd.read_csv("data/jobs_practice_2.csv")

# Inspect Data in Jupyter Notebook

# Change datatype to date for date columns
date_cols = ["order_date", "quoted_ship_date", "actual_ship_date"]
job_data[date_cols] = job_data[date_cols].apply(pd.to_datetime, errors="coerce")

# total_Cost
job_data["total_cost"] = job_data["material_cost"] + job_data["labor_cost"] + job_data["freight_cost"]

# net_revenue
job_data["net_revenue"] = job_data["revenue"] * (1 - job_data["discount_pct"] / 100)

# profit
job_data["profit"] = job_data["net_revenue"] - job_data["total_cost"]

# profit_margin_pct
job_data["profit_margin_pct"] = (job_data["profit"] / job_data["net_revenue"]) * 100
valid_margin = (job_data["profit_margin_pct"] > 0) & (job_data["status"] != "Cancelled")
job_data.loc[~valid_margin, "profit_margin_pct"] = pd.NA

# cost_per_unit
job_data["cost_per_unit"] = job_data["total_cost"] / job_data["units_completed"]

# On time flag
job_data.loc[job_data["actual_ship_date"].isnull(), "on_time_flag"] = pd.NA
job_data.loc[job_data["actual_ship_date"] <= job_data["quoted_ship_date"], "on_time_flag"] = "Y"
job_data.loc[job_data["actual_ship_date"] > job_data["quoted_ship_date"], "on_time_flag"] = "N"

# late days
job_data.loc[job_data["on_time_flag"].isna(), "late_days"] = pd.NA
job_data.loc[job_data["on_time_flag"] == "Y", "late_days"] = 0
job_data.loc[job_data["on_time_flag"] == "N", "late_days"] = (job_data["actual_ship_date"] - job_data["quoted_ship_date"]).dt.days

# rework flag
job_data.loc[job_data["rework_hours"] > 5, "rework_flag"] = "Y"
job_data.loc[job_data["rework_hours"] <= 5, "rework_flag"] = "N"